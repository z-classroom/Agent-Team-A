from .memory import Memory
from .policies import PolicyEngine
from .llm_provider import LLMProvider

class Agent:
    def __init__(self, cfg, policies, prompts, logger):
        # Stage 2: Initialize Memory with a persistent path from config
        self.memory = Memory(
            max_messages=cfg.get("memory", {}).get("max_messages", 12),
            storage_path=cfg.get("memory", {}).get("file_path", "logs/history.json")
        )
        self.policy_engine = PolicyEngine(policies)
        self.llm = LLMProvider.from_env_or_config(cfg)
        self.prompts = prompts
        self.logger = logger

    def _build_system_prompt(self) -> str:
        # Stage 2: Added 'Instructional Context' to help the AI remember its mission
        return f"{self.prompts['system']}\n\nSTYLE RULES: {self.prompts['style']}".strip()

    def respond(self, user_text: str) -> str:
        # 1. Policy check (The 'Trust' layer)
        policy = self.policy_engine.evaluate(user_text)
        self.logger.info(f"USER: {user_text} | POLICY: {policy.action}")

        # 2. Context Retrieval (Stage 2 improvement)
        # We now pass the loaded history to the LLM
        history = self.memory.messages()
        
        mode = "refusal" if policy.action == "REFUSE" else "normal"
        
        # 3. Generate response with full context
        reply = self.llm.complete(
            system=self._build_system_prompt(),
            messages=history,
            user=user_text,
            refusal_prompt=self.prompts["refusal"],
            mode=mode
        )
        
        # 4. Update the persistent JSON file
        self.memory.add(user_text, reply)
        self.logger.info(f"ASSISTANT: {reply}")
        return reply

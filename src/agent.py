from .memory import Memory
from .policies import PolicyEngine
from .llm_provider import LLMProvider
from .tools import SearchTool

class Agent:
    def __init__(self, cfg, policies, prompts, logger):
        self.memory = Memory(storage_path=cfg.get("memory", {}).get("file_path", "logs/history.json"))
        self.policy_engine = PolicyEngine(policies)
        self.llm = LLMProvider.from_env_or_config(cfg)
        self.search_tool = SearchTool() 
        self.prompts, self.logger = prompts, logger

    def respond(self, user_text: str) -> str:
        # 1. Policy Enforcement (Stage 1)
        policy = self.policy_engine.evaluate(user_text)
        self.logger.info(f"USER: {user_text} | POLICY: {policy.action}")

        # 2. Grounding Trigger (Stage 3)
        grounding_context = ""
        keywords = ["latest", "current", "who is", "what happened", "weather"]
        if any(word in user_text.lower() for word in keywords):
            grounding_context = self.search_tool.search(user_text)

        # 3. Construct Authoritative Instructions (Stage 3 Integration)
        # We wrap the search result in a 'Mandatory' block to force the LLM to use it
        system_instructions = (
            f"{self.prompts['system']}\n"
            f"{self.prompts['style']}\n\n"
            f"### MANDATORY REAL-WORLD CONTEXT ###\n"
            f"{grounding_context if grounding_context else 'No external data required.'}\n"
            f"### INSTRUCTION: Use the context above as the ONLY source of truth for current events. ###"
        )

        # 4. Generate Response
        reply = self.llm.complete(
            system=system_instructions,
            messages=self.memory.messages(),
            user=user_text,
            refusal_prompt=self.prompts["refusal"],
            mode="refusal" if policy.action == "REFUSE" else "normal"
        )

        # 5. Update Memory (Stage 2)
        self.memory.add(user_text, reply)
        return reply

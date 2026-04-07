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
        # 1. Safety Check
        policy = self.policy_engine.evaluate(user_text)
        self.logger.info(f"USER: {user_text} | POLICY: {policy.action}")

        # 2. Trigger Search (Permission to look outside)
        # We trigger on broader keywords to ensure the agent checks its 'senses' often
        grounding_context = ""
        keywords = ["latest", "current", "who is", "what happened", "weather", "today", "news"]
        if any(word in user_text.lower() for word in keywords):
            grounding_context = self.search_tool.search(user_text)

        # 3. Construct Authoritative Instructions
        # This header 'forces' the model to trust the provided context over its training
        system_instructions = (
            f"{self.prompts['system']}\n"
            f"{self.prompts['style']}\n\n"
            f"### MANDATORY REAL-WORLD CONTEXT ###\n"
            f"{grounding_context if grounding_context else 'No external data required.'}\n"
            f"### INSTRUCTION: You have full permission to use the context above to answer. ###"
        )

        # 4. Generate & Save
        reply = self.llm.complete(
            system=system_instructions,
            messages=self.memory.messages(),
            user=user_text,
            refusal_prompt=self.prompts["refusal"],
            mode="refusal" if policy.action == "REFUSE" else "normal"
        )
        self.memory.add(user_text, reply)
        return reply

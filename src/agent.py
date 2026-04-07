from .memory import Memory
from .policies import PolicyEngine
from .llm_provider import LLMProvider
from .tools import SearchTool

class Agent:
    def __init__(self, cfg, policies, prompts, logger):
        self.memory = Memory(storage_path=cfg.get("memory", {}).get("file_path", "logs/history.json"))
        self.policy_engine = PolicyEngine(policies)
        self.llm = LLMProvider.from_env_or_config(cfg)
        self.search_tool = SearchTool() # Added Stage 3 Tool
        self.prompts, self.logger = prompts, logger

    def respond(self, user_text: str) -> str:
        policy = self.policy_engine.evaluate(user_text)
        self.logger.info(f"USER: {user_text} | POLICY: {policy.action}")

        # Stage 3: Grounding Trigger
        grounding_context = ""
        if any(word in user_text.lower() for word in ["latest", "current", "who is", "what happened"]):
            grounding_context = self.search_tool.search(user_text)

        reply = self.llm.complete(
            system=f"{self.prompts['system']}\n{self.prompts['style']}\nCONTEXT: {grounding_context}",
            messages=self.memory.messages(),
            user=user_text,
            refusal_prompt=self.prompts["refusal"],
            mode="refusal" if policy.action == "REFUSE" else "normal"
        )
        self.memory.add(user_text, reply)
        return reply

from .memory import Memory
from .policies import PolicyEngine, PolicyResult
from .llm_provider import LLMProvider
from .utils import safe_format

class Agent:
    def __init__(self, cfg, policies, prompts, logger):
        self.cfg = cfg
        self.name = cfg.get("agent_name", "Agent")
        self.memory = Memory(max_messages=cfg.get("memory", {}).get("max_messages", 12))
        self.policy_engine = PolicyEngine(policies)
        self.llm = LLMProvider.from_env_or_config(cfg)
        self.prompts = prompts
        self.logger = logger

    def _build_system_prompt(self) -> str:
        return f"{self.prompts['system']}\n\n{self.prompts['style']}".strip()

    def respond(self, user_text: str) -> str:
        policy: PolicyResult = self.policy_engine.evaluate(user_text)
        self.logger.info("USER: %s | POLICY: %s", user_text, policy.action)

        mode = "refusal" if policy.action == "REFUSE" else "normal"
        reply = self.llm.complete(
            system=self._build_system_prompt(),
            messages=self.memory.messages(),
            user=user_text,
            refusal_prompt=self.prompts["refusal"],
            mode=mode
        )
        self.memory.add(user_text, reply)
        self.logger.info("ASSISTANT: %s", reply)
        return reply
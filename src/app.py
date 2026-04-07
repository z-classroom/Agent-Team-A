from dotenv import load_dotenv
from .agent import Agent
from .logger import build_logger
from .utils import load_yaml, load_text

def main() -> None:
    load_dotenv()
    cfg = load_yaml("config/agent.yaml")
    policies = load_yaml("config/Agent Team A policies.yaml")
    logger = build_logger(cfg["logging"]["path"], cfg["logging"]["level"])
    prompts = {
        "system": load_text("prompts/system.md"),
        "style": load_text("prompts/style.md"),
        "refusal": load_text("prompts/refusal.md"),
    }
    agent = Agent(cfg=cfg, policies=policies, prompts=prompts, logger=logger)
    print(f"\n{cfg['agent_name']} (v{cfg['version']}) — DeepSeek Local Engine Active.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"exit", "quit"}: break
        print(f"\n{cfg['agent_name']}: {agent.respond(user)}\n")

if __name__ == "__main__":
    main()
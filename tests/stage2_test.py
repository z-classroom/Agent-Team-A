import time
from src.agent import Agent
from src.utils import load_yaml, load_text
from src.logger import build_logger

def run_persistence_test():
    cfg = load_yaml("config/agent.yaml")
    policies = load_yaml("config/Agent Team A policies.yaml")
    logger = build_logger(cfg["logging"]["path"])
    prompts = {
        "system": load_text("prompts/system.md"),
        "style": load_text("prompts/style.md"),
        "refusal": load_text("prompts/refusal.md"),
    }
    
    print("\n--- STAGE 2: PERSISTENCE TEST START ---")
    
    # Session 1: The agent learns your name
    agent1 = Agent(cfg, policies, prompts, logger)
    print("\n[SESSION 1]")
    print(f"User: My name is Noor and I am studying Algorithmic Mediation.")
    print(f"Agent: {agent1.respond('My name is Noor and I am studying Algorithmic Mediation.')}")
    
    print("\n--- SHUTTING DOWN AGENT (SIMULATING RESTART) ---")
    del agent1
    time.sleep(2)
    
    # Session 2: A new instance tries to remember you
    agent2 = Agent(cfg, policies, prompts, logger)
    print("\n[SESSION 2]")
    print(f"User: Do you remember my name and what I am studying?")
    # If Stage 2 is working, it will say 'Noor' and 'Algorithmic Mediation'
    print(f"Agent: {agent2.respond('Do you remember my name and what I am studying?')}")
    
    print("\n--- STAGE 2 TEST COMPLETE ---")

if __name__ == "__main__":
    run_persistence_test()

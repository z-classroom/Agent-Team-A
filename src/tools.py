import os
import datetime
from typing import List, Dict

class SearchTool:
    def __init__(self):
        """
        Initializes the Search Tool for Team A.
        For Stage 3, this simulates a connection to an external search API 
        to build Cognitive Trust through grounding.
        """
        self.enabled = True

    def search(self, query: str) -> str:
        """
        Simulates an external search to ground the agent in real-world facts.
        """
        # Create an audit timestamp for transparency and trust
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log the tool execution to the terminal for debugging
        print(f"--- [TOOL] EXECUTE SEARCH AT {timestamp}: {query} ---")
        
        query_lower = query.lower()
        
        # --- SIMULATED SEARCH RESULTS (STAGE 3 TEST CASES) ---
        
        # Case 1: Jersey City Weather
        if "weather" in query_lower and "07306" in query_lower:
            return f"Current Weather in Jersey City (07306) on {timestamp}: 52°F, Partly Cloudy, Humidity 45%, Winds 10mph."
        
        # Case 2: Algorithmic Mediation Research
        if "leader" in query_lower and "algorithmic mediation" in query_lower:
            return ("As of 2026, leadership in Algorithmic Mediation research is decentralized, "
                    "with major contributions from the Oxford Internet Institute, Stanford HAI, "
                    "and the Berkman Klein Center for Internet & Society.")

        # Default fallback for other queries
        return f"Search result for '{query}': Grounded facts retrieved successfully on {timestamp}."

    def get_tool_definition(self) -> Dict:
        """
        Returns the metadata definition for the LLM to understand how to call this tool.
        """
        return {
            "name": "google_search",
            "description": "Use this tool to verify facts, check the weather, or find real-time information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The specific search query to look up."
                    }
                },
                "required": ["query"]
            }
        }

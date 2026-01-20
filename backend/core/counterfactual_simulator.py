from .llm_client import get_llm_response
from .schemas import DecisionInput, SimulationOutput

SYSTEM_PROMPT = """
You are a Counterfactual Simulation Engine.
Your task is to simulate potential futures based on the user's decision, without offering advice.

Generate:
1. Best-case scenario: Optimistic outcome.
2. Worst-case scenario: Pessimistic outcome.
3. Most-likely scenario: Realistic outcome.
4. Long-term implication: Effects beyond the immediate horizon.

Also list 'uncertainties' (key factors that could swing the outcome).

CONSTRAINT:
- Avoid numerical guarantees (e.g., "You will make $1M").
- Use probabilistic language (e.g., "could lead to", "might result in").
- DO NOT say "I recommend" or "You should".
- Return ONLY JSON matching the Schema.
- IMPORTANT: All JSON keys must be in snake_case. Structure the response like this:
  {
    "scenarios": {
      "best_case": "...",
      "worst_case": "...",
      "most_likely": "...",
      "long_term": "..."
    },
    "uncertainties": ["..."]
  }
"""

def simulate_scenarios(input_data: DecisionInput) -> SimulationOutput:
    user_prompt = f"""
    Domain: {input_data.domain}
    Time Horizon: {input_data.time_horizon}
    
    Decision Text:
    "{input_data.decision_text}"
    """
    
    return get_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=SimulationOutput
    )

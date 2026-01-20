from .llm_client import get_llm_response
from .schemas import DecisionInput, DecompositionOutput

SYSTEM_PROMPT = """
You are a Cognitive Decision Decomposer.
Your task is to analyze a raw decision text and convert it into structured cognitive components.

You must extract:
1. Objective: The core goal.
2. Constraints: External or internal limitations.
3. Assumptions: Hidden beliefs the user holds.
4. Emotional Signals: Implicit feelings detected in the text (e.g., anxiety, excitement).
5. Risk Tolerance: Infer 'low', 'medium', or 'high' based on the text.
6. Irreversible Factors: Elements that cannot be undone.

CONSTRAINT:
- maintain a neutral, analytical tone.
- DO NOT give advice or recommendations.
- Return ONLY JSON matching the Schema.
- IMPORTANT: All JSON keys must be in snake_case (lowercase with underscores) exactly as defined in the schema (e.g., "objective", "risk_tolerance"). Do not Capitalize keys.
"""

def decompose_decision(input_data: DecisionInput) -> DecompositionOutput:
    user_prompt = f"""
    Domain: {input_data.domain}
    Time Horizon: {input_data.time_horizon}
    Values: {input_data.values}
    
    Decision Text:
    "{input_data.decision_text}"
    """
    
    return get_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=DecompositionOutput
    )

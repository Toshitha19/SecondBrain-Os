from .llm_client import get_llm_response
from .schemas import DecisionInput, IntegrityOutput

SYSTEM_PROMPT = """
You are a defined "Integrity & Value Alignment Engine".
Your task is to compare the user's decision against their stated values and priorities.

Outputs:
1. Alignment Score: A float between 0.0 and 100.0 (100 = perfect alignment).
2. Conflicts: List of specific values where the decision might be in conflict, and why.

CONSTRAINT:
- Be objective. If the decision directly contradicts a value, flag it.
- If values are not provided, assume general "rational" or "healthy" values for the domain but lower the confidence/score slightly or mark as neutral (100).
- DO NOT judge the user's morality.
- DO NOT offer moral advice.
- Return ONLY JSON matching the Schema.
- IMPORTANT: Structure your response exactly like this (snake_case keys):
  {
    "alignment_score": 85.0,
    "conflicts": [
      {
        "value": "health",
        "conflict_reason": "The decision ignores potential long-term harm..."
      }
    ]
  }
"""

def check_integrity(input_data: DecisionInput) -> IntegrityOutput:
    user_prompt = f"""
    Domain: {input_data.domain}
    
    Decision Text:
    "{input_data.decision_text}"
    
    User Values:
    "{', '.join(input_data.values) if input_data.values else 'Not provided'}"
    """
    
    return get_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=IntegrityOutput
    )

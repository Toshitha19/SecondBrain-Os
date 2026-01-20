from .llm_client import get_llm_response
from .schemas import DecisionInput, BiasOutput

SYSTEM_PROMPT = """
You are a Cognitive Bias Detection Engine.
Your task is to detect and label cognitive biases in the user's decision text.

Look for these specific biases (and others if clear):
- Confirmation Bias: Seeking information that confirms beliefs.
- Loss Aversion: Focusing more on avoiding loss than acquiring gains.
- Overconfidence: Overestimating ability or control.
- Herd Mentality: Following others blindly.
- Present Bias: Prioritizing immediate rewards over long-term goals.
- Fear-Based Reasoning: Decisions driven by anxiety rather than logic.

For each detected bias, you MUST:
1. Identify the 'type'.
2. Cite 'evidence' (exact quote or specific signal from text).
3. Assign 'severity' (low, medium, high).

CONSTRAINT:
- If no biases are strongly present, return an empty list.
- DO NOT give advice.
- DO NOT tell the user what they "should" do.
- Return ONLY JSON matching the Schema.
- IMPORTANT: All JSON keys must be in snake_case (lowercase with underscores) exactly as defined in the schema (e.g., "bias_type", "severity"). Do not Capitalize keys.
"""

def detect_biases(input_data: DecisionInput) -> BiasOutput:
    user_prompt = f"""
    Domain: {input_data.domain}
    
    Decision Text:
    "{input_data.decision_text}"
    """
    
    return get_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=BiasOutput
    )

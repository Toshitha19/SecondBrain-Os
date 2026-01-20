from typing import Optional
from .llm_client import get_llm_response
from .schemas import (
    DecisionInput, DecompositionOutput, BiasOutput, 
    SimulationOutput, IntegrityOutput, ReportOutput
)

SYSTEM_PROMPT = """
You are a Decision Integrity Report Generator.
Your task is to synthesize the analysis from other modules into a final audit report.

Inputs:
- Decomposition
- Bias Analysis
- Scenarios
- Integrity Check

Outputs:
1. Risk Score (0-100): Composite risk based on irreversible factors, worst-case scenarios, and biases.
2. Bias Score (0-100): Representing the level of cognitive distortion (100 = clean, 0 = heavily biased). note: this is inverse of bias severity.
3. Alignment Score (0-100): Directly from Integrity Check.
4. Key Assumptions: Summarize top 3 critical assumptions.
5. Missing Information: What crucial data is the user not seeing?
6. Reflection Questions: 3-5 deep questions to prompt user self-reflection.

CONSTRAINT:
- The Reflection Questions MUST be questions. 
- NO statements of advice.
- NO "You should focus on...". instead ask "Have you considered...?"
- Return ONLY JSON matching the Schema.
- IMPORTANT: All JSON keys must be in snake_case (lowercase with underscores) exactly as defined in the schema (e.g., "risk_score", "key_assumptions"). Do not Capitalize keys.
"""

def generate_report(
    input_data: DecisionInput,
    decomposition: DecompositionOutput,
    bias: BiasOutput,
    simulation: SimulationOutput,
    integrity: IntegrityOutput
) -> ReportOutput:
    
    # We pass the full context to the LLM to synthesize the final scores and questions
    user_prompt = f"""
    Decision: "{input_data.decision_text}"
    
    Decomposition: {decomposition.model_dump_json()}
    Biases Detected: {bias.model_dump_json()}
    Simulation: {simulation.model_dump_json()}
    Integrity: {integrity.model_dump_json()}
    """
    
    report = get_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_model=ReportOutput
    )
    
    # Attach detailed parts for the frontend to render if needed (optional)
    report.decomposition = decomposition
    report.bias_analysis = bias
    report.simulation = simulation
    report.integrity_analysis = integrity
    
    return report

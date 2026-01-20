from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class DecisionInput(BaseModel):
    decision_text: str
    domain: str = Field(..., description="finance | career | health | general")
    time_horizon: str = Field(..., description="short | medium | long")
    values: Optional[List[str]] = Field(default_factory=list, description="User's core values or priorities")

class DecompositionOutput(BaseModel):
    objective: str
    constraints: List[str]
    assumptions: List[str]
    emotional_signals: List[str]
    risk_tolerance: str = Field(..., description="low|medium|high")
    irreversible_factors: List[str]

class BiasEvidence(BaseModel):
    bias_type: str
    evidence: str
    severity: str = Field(..., description="low|medium|high")

class BiasOutput(BaseModel):
    biases: List[BiasEvidence]

class Scenarios(BaseModel):
    best_case: str
    worst_case: str
    most_likely: str
    long_term: str

class SimulationOutput(BaseModel):
    scenarios: Scenarios
    uncertainties: List[str]

class IntegrityConflict(BaseModel):
    value: str
    conflict_reason: str

class IntegrityOutput(BaseModel):
    alignment_score: float = Field(..., ge=0, le=100)
    conflicts: List[IntegrityConflict]

class ReportOutput(BaseModel):
    risk_score: float = Field(..., ge=0, le=100)
    bias_score: float = Field(..., ge=0, le=100)
    alignment_score: float = Field(..., ge=0, le=100)
    key_assumptions: List[str]
    missing_information: List[str]
    reflection_questions: List[str]
    # Detailed module outputs for context if needed
    decomposition: Optional[DecompositionOutput] = None
    bias_analysis: Optional[BiasOutput] = None
    simulation: Optional[SimulationOutput] = None
    integrity_analysis: Optional[IntegrityOutput] = None

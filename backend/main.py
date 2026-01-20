from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from backend.core.schemas import DecisionInput, ReportOutput
from backend.core.decision_decomposer import decompose_decision
from backend.core.bias_detector import detect_biases
from backend.core.counterfactual_simulator import simulate_scenarios
from backend.core.integrity_checker import check_integrity
from backend.core.report_generator import generate_report

app = FastAPI(title="SecondBrain OS API", version="1.0.0")

@app.post("/audit", response_model=ReportOutput)
async def audit_decision(input_data: DecisionInput):
    try:
        # Check for empty decision
        if not input_data.decision_text.strip():
            raise HTTPException(status_code=400, detail="Decision text cannot be empty.")

        # 1. Decompose
        decomposition = decompose_decision(input_data)
        
        # 2. Detect Biases
        biases = detect_biases(input_data)
        
        # 3. Simulate
        simulation = simulate_scenarios(input_data)
        
        # 4. Check Integrity
        integrity = check_integrity(input_data)
        
        # 5. Generate Final Report
        report = generate_report(
            input_data, 
            decomposition, 
            biases, 
            simulation, 
            integrity
        )
        
        return report

    except Exception as e:
        # In production, log the full error
        print(f"Error processing decision: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

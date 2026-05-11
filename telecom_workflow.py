from typing import TypedDict
    - LOW_RISK
    - MEDIUM_RISK
    - HIGH_RISK

    Return ONLY the classification.
    """

    response = llm.invoke(prompt)

    state["fraud_risk"] = response.content.strip()

    return state


# -----------------------------
# STEP 3 — FINAL ACTIVATION DECISION
# -----------------------------
def activation_decision_node(state: TelecomState) -> TelecomState:

    risk = state["fraud_risk"]

    if risk == "LOW_RISK":
        state["final_decision"] = "SIM Activated"

    elif risk == "MEDIUM_RISK":
        state["final_decision"] = "Manual Review"

    else:
        state["final_decision"] = "Reject Application"

    return state


# -----------------------------
# BUILD LANGGRAPH WORKFLOW
# -----------------------------
telecom_graph = StateGraph(TelecomState)

telecom_graph.add_node("kyc_verification", kyc_verification_tool)
telecom_graph.add_node("fraud_detection", fraud_detection_node)
telecom_graph.add_node("activation_decision", activation_decision_node)

telecom_graph.set_entry_point("kyc_verification")

telecom_graph.add_edge("kyc_verification", "fraud_detection")
telecom_graph.add_edge("fraud_detection", "activation_decision")
telecom_graph.add_edge("activation_decision", END)

telecom_workflow = telecom_graph.compile()


# -----------------------------
# EXECUTION
# -----------------------------
if __name__ == "__main__":

    telecom_input = {
        "customer_name": "Rahul Sharma",
        "aadhaar_status": "VALID",
        "pan_status": "VALID",
        "location": "Delhi",
        "previous_sim_requests": 1
    }

    result = telecom_workflow.invoke(telecom_input)

    print("
=== Telecom Workflow Output ===")
    print(result)

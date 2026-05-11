from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


# -----------------------------
# STATE DEFINITION
# -----------------------------
class HealthcareState(TypedDict):
    patient_name: str
    age: int
    fever: float
    oxygen_level: int
    heart_rate: int
    symptom_duration_days: int
    existing_conditions: str

    severity_level: str
    priority_level: str
    consultation_assignment: str


# -----------------------------
# STEP 1 — SYMPTOM SEVERITY TOOL
# -----------------------------
def symptom_severity_tool(state: HealthcareState) -> HealthcareState:

    oxygen = state["oxygen_level"]
    fever = state["fever"]
    heart_rate = state["heart_rate"]
    duration = state["symptom_duration_days"]

    if oxygen < 90 or heart_rate > 130:
        state["severity_level"] = "CRITICAL"

    elif fever > 101 or duration > 5:
        state["severity_level"] = "MODERATE"

    else:
        state["severity_level"] = "STABLE"

    return state


# -----------------------------
# STEP 2 — GEMINI PRIORITIZATION
# -----------------------------
def medical_prioritization_node(state: HealthcareState) -> HealthcareState:

    prompt = f"""
    You are a hospital medical prioritization AI.

    Analyze the following patient details:

    Severity Level: {state['severity_level']}
    Patient Age: {state['age']}
    print(result)

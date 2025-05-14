from pydantic import BaseModel
from agents import Agent

class ClarifyingQuestions(BaseModel):
    questions: list[str]
    """Three clarifying questions to better understand the user's query."""

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=(
        "You are a research assistant. Your task is to ask 3 clarifying questions that help refine and understand "
        "a research query better. These should help make the query more specific, contextual, or actionable."
    ),
    model="gpt-4o-mini",
    output_type=ClarifyingQuestions,
)
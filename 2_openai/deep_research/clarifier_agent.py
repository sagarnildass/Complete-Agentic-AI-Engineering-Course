from agents import Agent

CLARIFIER_INSTRUCTIONS = (
    "Given a research query, generate 3 clarifying questions that would help you better understand the user's intent. "
    "Be concise and specific. Output as a list of 3 questions."
)

clarifier_agent = Agent(
    name="ClarifierAgent",
    instructions=CLARIFIER_INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=list[str],
) 
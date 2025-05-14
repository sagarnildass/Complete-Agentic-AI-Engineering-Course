# deep_research.py

import gradio as gr
from dotenv import load_dotenv
from clarifier_agent import clarifier_agent, ClarifyingQuestions
from research_manager import ResearchManagerAgent
from agents import Runner

load_dotenv(override=True)

# Step 1: Generate clarifying questions
async def get_clarifying_questions(query):
    result = await Runner.run(clarifier_agent, input=query)
    return result.final_output.questions  # List of 3 strings

# Step 2: Run research with original questions + user answers
async def run_full_pipeline(query, q1, q2, q3, a1, a2, a3):
    questions = [q1, q2, q3]
    answers = [a1, a2, a3]
    async for chunk in ResearchManagerAgent().run(query, questions, answers):
        yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research Agent")

    query = gr.Textbox(label="Research topic")

    get_questions_btn = gr.Button("🔍 Get Clarifying Questions", variant="primary")

    # Question display (readonly)
    clar_q1 = gr.Textbox(label="Clarifying Question 1", interactive=False)
    clar_q2 = gr.Textbox(label="Clarifying Question 2", interactive=False)
    clar_q3 = gr.Textbox(label="Clarifying Question 3", interactive=False)

    # Answer inputs
    answer_1 = gr.Textbox(label="Your Answer to Q1")
    answer_2 = gr.Textbox(label="Your Answer to Q2")
    answer_3 = gr.Textbox(label="Your Answer to Q3")

    submit_answers_btn = gr.Button("✅ Submit Answers & Run")
    report = gr.Markdown(label="Report")

    # Step 1: Show clarifying questions
    get_questions_btn.click(
        fn=get_clarifying_questions,
        inputs=query,
        outputs=[clar_q1, clar_q2, clar_q3]
    )

    # Step 2: Submit answers and run
    submit_answers_btn.click(
        fn=run_full_pipeline,
        inputs=[query, clar_q1, clar_q2, clar_q3, answer_1, answer_2, answer_3],
        outputs=report
    )

ui.launch(inbrowser=True)

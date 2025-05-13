import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager
import time
from collections import defaultdict
from datetime import datetime
import logging

load_dotenv(override=True)

# --- Rate Limiter with Daily Quota ---
class RateLimiter:
    # allows 2 requests per minute
    def __init__(self, max_requests=2, time_window=60, daily_quota=10):
        self.max_requests = max_requests
        self.time_window = time_window  # seconds
        self.request_history = defaultdict(list)
        self.daily_quota = daily_quota
        self.daily_counts = defaultdict(lambda: {'date': self._today(), 'count': 0})

    def _today(self):
        return datetime.utcnow().strftime('%Y-%m-%d')

    def is_rate_limited(self, user_id):
        current_time = time.time()
        self.request_history[user_id] = [
            t for t in self.request_history[user_id]
            if current_time - t < self.time_window
        ]
        if len(self.request_history[user_id]) >= self.max_requests:
            return True
        self.request_history[user_id].append(current_time)
        return False

    def is_quota_exceeded(self, user_id):
        today = self._today()
        user_quota = self.daily_counts[user_id]
        if user_quota['date'] != today:
            user_quota['date'] = today
            user_quota['count'] = 0
        if user_quota['count'] >= self.daily_quota:
            return True
        user_quota['count'] += 1
        self.daily_counts[user_id] = user_quota
        return False

rate_limiter = RateLimiter(max_requests=2, time_window=60, daily_quota=10)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

async def get_user_id(request: gr.Request = None):
    user_id = "default_user"
    if request is not None:
        try:
            forwarded_for = request.headers.get("X-Forwarded-For")
            cloudflare_ip = request.headers.get("Cf-Connecting-IP")
            if forwarded_for:
                user_id = forwarded_for.split(",")[0].strip()
            elif cloudflare_ip:
                user_id = cloudflare_ip
            else:
                user_id = getattr(request.client, 'host', 'default_user')
        except Exception:
            user_id = "default_user"
    logger.debug(f"User ID: {user_id}")
    return user_id

async def get_clarifying_questions(query, request: gr.Request = None):
    user_id = await get_user_id(request)
    if rate_limiter.is_rate_limited(user_id):
        return None, ["You are sending requests too quickly. Please wait a minute."]
    if rate_limiter.is_quota_exceeded(user_id):
        return None, ["You have reached your daily research quota. Please try again tomorrow."]
    manager = ResearchManager()
    async for chunk in manager.run(query):
        if isinstance(chunk, dict) and "clarifying_questions" in chunk:
            return chunk["clarifying_questions"], None
    return None, ["Failed to generate clarifying questions."]

async def run_research(query, clarifications, request: gr.Request = None):
    user_id = await get_user_id(request)
    if rate_limiter.is_rate_limited(user_id):
        yield "You are sending requests too quickly. Please wait a minute."
        return
    if rate_limiter.is_quota_exceeded(user_id):
        yield "You have reached your daily research quota. Please try again tomorrow."
        return
    manager = ResearchManager()
    # Pass clarifications to the research workflow
    async for chunk in manager.run(query, clarifications):
        if not isinstance(chunk, dict):
            yield chunk

with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    state = gr.State()
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    ask_button = gr.Button("Get Clarifying Questions", variant="primary")
    clarifying_questions = gr.Markdown(visible=False)
    clarification_inputs = [gr.Textbox(label=f"Clarification {i+1}", visible=False) for i in range(3)]
    submit_clarifications = gr.Button("Submit Clarifications", visible=False)
    report = gr.Markdown(label="Report")

    def show_questions(questions):
        if questions:
            return gr.update(visible=True, value="\n".join([f"**Q{i+1}:** {q}" for i, q in enumerate(questions)])), [gr.update(visible=True) for _ in range(3)], gr.update(visible=True)
        else:
            return gr.update(visible=False), [gr.update(visible=False) for _ in range(3)], gr.update(visible=False)

    async def handle_query(query, request: gr.Request = None):
        questions, errors = await get_clarifying_questions(query, request)
        if errors:
            return "\n".join(errors), ["", "", ""], gr.update(visible=False), *[gr.update(visible=False, interactive=False) for _ in range(3)], gr.update(visible=False)
        return "\n".join([f"**Q{i+1}:** {q}" for i, q in enumerate(questions)]), questions, gr.update(visible=True), *[gr.update(visible=True, interactive=True) for _ in range(3)], gr.update(visible=True)

    ask_button.click(
        handle_query,
        inputs=[query_textbox],
        outputs=[clarifying_questions, state, clarifying_questions, *clarification_inputs, submit_clarifications],
        api_name="get_clarifying_questions"
    )

    async def handle_clarifications(query, clar1, clar2, clar3, request: gr.Request = None):
        clarifications = [clar1, clar2, clar3]
        async for chunk in run_research(query, clarifications, request):
            yield chunk

    submit_clarifications.click(
        handle_clarifications,
        inputs=[query_textbox, *clarification_inputs],
        outputs=report,
        api_name="run_research"
    )


    query_textbox.submit(
        handle_query,
        inputs=[query_textbox],
        outputs=[clarifying_questions, state, clarifying_questions, *clarification_inputs, submit_clarifications],
        api_name="get_clarifying_questions"
    )

ui.launch(inbrowser=True)


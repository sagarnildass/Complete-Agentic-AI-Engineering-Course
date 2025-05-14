import os
from agents import Agent, function_tool

@function_tool
def send_email(subject: str, html_body: str):
    """Send out an email with the given subject and HTML body to all sales prospects using Mailgun"""
    import os
    import requests
    import base64
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAILGUN_RECIPIENT = os.environ.get('MAILGUN_RECIPIENT')
    auth = base64.b64encode(f'api:{MAILGUN_API_KEY}'.encode()).decode()
    response = requests.post(
        f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
        headers={
            'Authorization': f'Basic {auth}'
        },
        data={
            'from': f'Research Agent <mailgun@{MAILGUN_DOMAIN}>',
            'to': MAILGUN_RECIPIENT,
            'subject': subject,
            'html': html_body
        }
    )
    return {"status": "success" if response.status_code == 200 else "failure", "response": response.text}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
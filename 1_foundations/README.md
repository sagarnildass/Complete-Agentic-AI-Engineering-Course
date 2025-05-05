---
title: Career Conversation Assistant
app_file: app.py
sdk: gradio
sdk_version: 4.44.1
---

# Career Conversation Assistant

## Overview
This is an AI-powered personal assistant that represents Sagarnil Das and can answer questions about his career, background, skills, and experience. The assistant uses Gemini 2.0 Flash model to provide accurate responses and collects contact information from interested users.

## Features
- **Conversational Interface**: Engage in natural conversations with the assistant
- **Profile Representation**: Answers questions based on Sagarnil's LinkedIn profile and summary
- **Contact Collection**: Allows interested users to leave their email and information
- **Notification System**: Sends both push notifications (via Pushover) and emails (via Mailgun)
- **Rate Limiting**: Prevents abuse by limiting the frequency of user messages
- **IP Detection**: Intelligently identifies users by their IP address when deployed on Hugging Face Spaces

## Technical Implementation
- **Frontend**: Gradio chat interface
- **Backend**: Python with OpenAI API (configured to use Google's Gemini 2.0 Flash model)
- **Tools**: 
  - `record_user_details`: Collects and logs contact information
  - `record_unknown_question`: Logs questions that couldn't be answered
- **External Services**:
  - Mailgun for email notifications
  - Pushover for push notifications
- **Data Sources**:
  - LinkedIn profile PDF
  - Personal summary text file

## Configuration
The application uses environment variables for configuration:
- `GOOGLE_API_KEY`: API key for Google Gemini access
- `PUSHOVER_TOKEN` and `PUSHOVER_USER`: For push notifications
- `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, and `MAILGUN_RECIPIENT`: For email notifications

## Deployment
This application is designed to be deployed on Hugging Face Spaces. It handles proper IP detection through headers for accurate rate limiting. It can also be integrated with a Next.js frontend application.

## Usage
When deployed, users can:
1. Ask questions about Sagarnil's background and experience
2. Engage in natural conversation
3. Provide contact information for follow-up

## Rate Limiting
To prevent abuse, the system limits users to 5 messages within a 5-second window. Rate limiting is based on the user's IP address.

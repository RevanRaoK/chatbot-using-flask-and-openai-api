from datetime import datetime
from flask import Blueprint, render_template, request
from .models import Result
from openai import OpenAI
import os

routes = Blueprint('routes', __name__)

historyData = []

# Declare the client using openrouter endpoint and models
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
  base_url="https://openrouter.ai/api/v1",
)


def ask(question, chat_log=None):
  """Ask Model a question with optional previous chat log for context."""
  if client is None:
    return "Sorry, the AI service failed to initialize."

  messages = []
  if chat_log:
    for item in chat_log:
      role = "user" if "float-right" in item.messagetype else "assistant"
      messages.append({"role": role, "content": item.message})

  messages.append({"role": "user", "content": question})
  try:
    response = client.chat.completions.create(
      model="nvidia/nemotron-3.5-lightning",
      messages=messages
    )
    return response.choices[0].message.content.strip()
  except Exception as e:
    print(f"OpenAI API call error: {e}")
    return "Sorry, I'm experiencing an issue connection to the AI service."


@routes.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    return render_template('history.html', results=historyData)

  query = request.args.get('query')
  if not query:
    return render_template('response_view.html', results=historyData)

  # send previous history to Model
  response_text = ask(query, chat_log=historyData)

  # Create result objects for display
  now = datetime.now().strftime("%H:%M")
  queryMessage = Result(
    time=now,
    messagetype="other-message float-right",
    message=query
  )
  responseMessage = Result(
    time=now,
    messagetype='my-message',
    message=response_text
  )

  # Update history
  historyData.extend([queryMessage, responseMessage])

  return render_template('response_view.html', results=historyData)
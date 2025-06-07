from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_NAME

client = OpenAI(api_key=OPENAI_API_KEY)

def get_response_from_history(history):
    """
    Sends a conversation history to the model and returns the response.
    History should be a list of {"role": "user"/"assistant", "content": "..."}.
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=history
    )
    return response.choices[0].message.content.strip()

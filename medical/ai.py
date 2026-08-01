import os
import requests
from dotenv import load_dotenv

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


# ==========================================
# AI Function
# ==========================================

def ask_ai(question, context):

    prompt = f"""
You are a professional AI Medical Assistant.

Answer ONLY from the uploaded medical report.

If the answer is not present in the report, reply:

"I could not find this information in the uploaded medical report."

=========================
MEDICAL REPORT
=========================

{context}

=========================
USER QUESTION
=========================

{question}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://127.0.0.1:8000",
        "X-Title": "Medical RAG AI"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 1000
    }

    try:
        response = requests.post(
            URL,
            headers=headers,
            json=data,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]

        if "error" in result:
            return f"OpenRouter Error: {result['error'].get('message', 'Unknown error')}"

        return "No response received from AI."

    except requests.exceptions.RequestException as e:
        return f"Connection Error: {e}"

    except Exception as e:
        return f"Unexpected Error: {e}"
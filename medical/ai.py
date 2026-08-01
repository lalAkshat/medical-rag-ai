import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(question, context):

    prompt = f"""
You are a professional AI Medical Assistant.

Answer ONLY from the uploaded medical report.

If the answer is not present in the report, reply:

"I could not find this information in the uploaded medical report."

Medical Report:
{context}

User Question:
{question}
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://medical-rag-ai-lyvg.onrender.com",
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
            return result["error"]["message"]

        return "No response from AI."

    except Exception as e:
        return str(e)
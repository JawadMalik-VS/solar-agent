import os
import re
import requests
import datetime
import pathlib
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MCP_SERVER = "http://127.0.0.1:5000"

# -------------------------------
# Helper functions for logging
# -------------------------------
LOG_DIR = pathlib.Path("chat_logs")
LOG_DIR.mkdir(exist_ok=True)

def extract_main_topic(prompt: str, max_words=5):
    words = prompt.strip().split()
    topic = " ".join(words[:max_words])
    topic = re.sub(r"[^a-zA-Z0-9_-]", "_", topic)  # sanitize filename
    return topic.lower()

def save_to_file(prompt: str, response: str):
    topic = extract_main_topic(prompt)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{topic}_{timestamp}.txt"
    filepath = LOG_DIR / filename

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"Topic: {topic}\n")
        f.write("=" * 50 + "\n\n")
        f.write("PROMPT:\n")
        f.write(prompt + "\n\n")
        f.write("RESPONSE:\n")
        f.write(response)

# -------------------------------
# MCP tool helper
# -------------------------------
def call_solar_tool(consumption_kwh, rate_per_kwh):
    res = requests.post(
        f"{MCP_SERVER}/tool/calculate_solar",
        json={
            "consumption_kwh": consumption_kwh,
            "rate_per_kwh": rate_per_kwh
        }
    )
    return res.json()["estimated_savings"]

def extract_numbers(prompt: str):
    kwh = re.search(r"(\d+)\s*kwh", prompt.lower())
    rate = re.search(r"\$?(\d+(\.\d+)?)\s*/?\s*kwh", prompt.lower())
    return (
        float(kwh.group(1)) if kwh else None,
        float(rate.group(1)) if rate else None
    )

# -------------------------------
# Main agent function
# -------------------------------
def agent(prompt: str) -> str:
    consumption, rate = extract_numbers(prompt)

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful solar energy assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    text = res.choices[0].message.content

    if consumption and rate:
        savings = call_solar_tool(consumption, rate)
        text += f"\n\n💡 Estimated Solar Savings: ${savings} / month"

    # ✅ Save prompt + response to text file
    save_to_file(prompt, text)

    return text

import os
import re
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

MCP_SERVER = "http://127.0.0.1:5000"

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

    return text

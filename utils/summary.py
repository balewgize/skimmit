import os
import re
import json
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

print("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY"))


def summarize(text, source):
    text = text[:14000]
    part_one = (
        "In just 5 sentences, capture the heart of the {source} text below. "
        "Highlight what it's about, who it's for, and why it might be interesting. \n\n"
        "Respond with a JSON format having the following structure:\n"
    )
    part_two = """
        {{
            "title": "short descriptive title",
            "sentences": [
                "sentence 1",
                "sentence 2",
                "sentence 3",
                "sentence 4",
                "sentence 5",
            ],
        }}
    """
    part_three = (
        "\nPlase strictly adhere to JSON format standards and "
        "don't add any additional text to the response.\n\n"
        "TEXT:\n===\n{text}\n==="
    )
    prompt = part_one + part_two + part_three
    prompt = prompt.format(text=text, source=source)

    summary = None
    try:
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt).text
        match = re.search(r"\{[^{}]*\}", response, re.IGNORECASE)
        if match:
            summary = json.loads(match.group(0).strip())
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
    except Exception as e:
        print("Error while summarizing:", e)  # TODO: add logging

    return summary

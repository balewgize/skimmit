import os
import json
import logging
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


def summarize_text(text, source):
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
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(
            prompt, generation_config={"response_mime_type": "application/json"}
        )
        summary = json.loads(response.text)
        logging.info("Summary generated successfully.")
    except json.JSONDecodeError as e:
        logging.error("Invalid JSON returned by the API.")
        logging.exception(e)
    except Exception as e:
        logging.error("Failed to generate summary.")
        logging.exception(e)

    return summary

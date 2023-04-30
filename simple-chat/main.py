import json
import requests
import os
import sys
from pathlib import Path

API_KEY = os.environ["OPENAI_API_KEY"]
API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def create_chat_file(chat_filename):
    chat_filepath = Path(chat_filename)
    if not chat_filepath.exists():
        with open(chat_filename, "w") as f:
            json.dump([], f)


def get_chat_history():
    with open("current_chat.txt", "r") as f:
        current_chat = f.read().strip()

    create_chat_file(current_chat)

    with open(current_chat, "r") as f:
        chat_history = json.load(f)

    return chat_history


def store_chat_history(chat_history):
    with open("current_chat.txt", "r") as f:
        current_chat = f.read().strip()

    with open(current_chat, "w") as f:
        json.dump(chat_history, f)


def change_chat(new_chat_filename):
    with open("current_chat.txt", "w") as f:
        f.write(new_chat_filename)


def contact_api(content):
    chat_history = get_chat_history()
    chat_history.append({"role": "user", "content": content})

    response = requests.post(API_URL, headers=HEADERS, json={
                             "model": "gpt-4", "messages": chat_history})
    response_json = response.json()

    if "choices" in response_json and len(response_json["choices"]) > 0:
        assistant_message = response_json["choices"][0]["message"]["content"]
        chat_history.append(
            {"role": "assistant", "content": assistant_message})
        store_chat_history(chat_history)
        return assistant_message
    else:
        return "Error: Unable to get a response from the GPT-4 API."


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <user_prompt>")
        sys.exit(1)

    user_input = sys.argv[1]

    if user_input.lower().startswith("switch "):
        _, new_chat_filename = user_input.split(" ", 1)
        change_chat(new_chat_filename)
        print(f"Switched to chat: {new_chat_filename}")
    else:
        assistant_response = contact_api(user_input)
        print(f"GPT-4: {assistant_response}")

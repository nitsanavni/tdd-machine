import json
import requests
import os
from pathlib import Path

API_KEY = os.environ["OPENAI_API_KEY"]
API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}


def load_chat_history():
    with open("current_chat.txt", "r") as f:
        chat_history = json.load(f)
    return chat_history


def save_chat_history(chat_history):
    with open("current_chat.txt", "w") as f:
        json.dump(chat_history, f)


def send_message_to_api(content):
    chat_history = load_chat_history()
    chat_history.append({"role": "user", "content": content})

    response = requests.post(API_URL, headers=HEADERS, json={
                             "model": "gpt-4", "messages": chat_history})
    response_json = response.json()

    if "choices" in response_json and len(response_json["choices"]) > 0:
        assistant_message = response_json["choices"][0]["message"]["content"]
        chat_history.append(
            {"role": "assistant", "content": assistant_message})
        save_chat_history(chat_history)
        return assistant_message
    else:
        return "Error: Unable to get a response from the GPT-4 API."


if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        assistant_response = send_message_to_api(user_input)
        print(f"GPT-4: {assistant_response}")

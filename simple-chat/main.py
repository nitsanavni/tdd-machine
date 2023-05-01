import json
import requests
import os
import sys
import subprocess
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


def execute_and_get_result(command):
    print(f"About to execute the following command: {command}")
    confirmation = input("Do you want to proceed? (yes/no): ").lower().strip()

    if confirmation == "yes":
        try:
            output = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True)
            exit_status = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            exit_status = e.returncode

        return output.strip(), exit_status
    else:
        print("Command execution canceled.")
        return "Canceled by user", -1


def split_response_and_command(assistant_response):
    lines = assistant_response.split("\n")
    message = []
    execute_command = None
    for line in lines:
        if line.lower().startswith("execute:"):
            execute_command = line[len("execute:"):].strip()
        else:
            message.append(line)
    return "\n".join(message).strip(), execute_command


while True:
    user_input_lines = []
    print("You (Press Ctrl+D to submit your input):")
    while True:
        try:
            line = input()
            user_input_lines.append(line)
        except EOFError:
            print()  # Add an extra newline before continuing
            break

    user_input = "\n".join(user_input_lines)

    if user_input.lower().startswith("switch "):
        _, new_chat_filename = user_input.split(" ", 1)
        change_chat(new_chat_filename)
        print(f"Switched to chat: {new_chat_filename}")
    else:
        assistant_response = contact_api(user_input)

        message, command = split_response_and_command(assistant_response)

        print(f"GPT-4: {message}")

        if command:
            command_output, exit_status = execute_and_get_result(command)

            print(f"Output: {command_output}\nExit Status: {exit_status}")

            user_input = f"The command executed with the following output:\n{command_output}\nExit Status: {exit_status}"
            assistant_response = contact_api(user_input)

            message, command = split_response_and_command(assistant_response)

            print(f"GPT-4: {message}")

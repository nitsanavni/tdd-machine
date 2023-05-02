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
        return f"Error: Unable to get a response from the GPT-4 API. {response.text}"


def execute_and_get_result(command):
    print(f"executing command: {command}")
    # confirmation = input("Do you want to proceed? (yes/no): ").lower().strip()

    # if confirmation == "yes":
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True)
        exit_status = 0
    except subprocess.CalledProcessError as e:
        output = e.output
        exit_status = e.returncode

    return output.strip(), exit_status
    # else:
    #     print("Command execution canceled.")
    #     return "Canceled by user", -1


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


message, command = None, None

while True:
    prompt = ""

    if command:
        command_output, exit_status = execute_and_get_result(command)
        exec_result_prompt = f"executeResult {{\n  cmd: {command}\n  output: {command_output}\n  exit: {exit_status}\n}}"
        print(exec_result_prompt)
        prompt += exec_result_prompt + "\n---\n"

    user_input_lines = []
    print("> (Ctrl+D to submit)")
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
        continue

    prompt += user_input

    assistant_response = contact_api(prompt)

    message, command = split_response_and_command(assistant_response)

    print(f">> {assistant_response}")

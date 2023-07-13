import json
import subprocess

from chat import chat_with_gpt4


def build_template(template_file, execute_result_json, log_json):
    with open(template_file, "r") as file:
        template_string = file.read()
        return template_string.format(execute_result=execute_result_json, log=log_json)


def parse_response(response):
    return json.loads(response)


def execute_commands(execute):
    execute_result = []
    for command in execute:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        stdout, _ = process.communicate()
        exitcode = process.returncode
        execute_result.append(
            {
                "intention": command,
                "command": command,
                "stdout": stdout.decode("utf-8"),
                "exitCode": exitcode,
            }
        )
    return execute_result


def add_to_log_file(log_file, summary):
    with open(log_file, "a") as file:
        file.write(summary)


def load_from_file(filename):
    with open(filename, "r") as file:
        return json.load(file)


def write_to_file(filename, content):
    with open(filename, "w") as file:
        json.dump(content, file)


while True:
    execute_result = load_from_file("execute_result.json")
    log = load_from_file("log.json")

    text = build_template("prompt", execute_result, log)
    gpt4_response = chat_with_gpt4(text)

    print(gpt4_response)

    response = parse_response(gpt4_response)

    execute_result = execute_commands(response["execute"])
    write_to_file("execute_result.json", execute_result)

    add_to_log_file("log.json", response["summary"])

import json
import subprocess

from chat import chat_with_gpt4


def read_file(file):
    with open(file, "r") as f:
        return f.read()


def build_template(template_file, execute_result_json, log_json, message_from_user):
    return read_file(template_file).format(
        log=log_json,
        execute_result=execute_result_json,
        message_from_user=message_from_user,
    )


def parse_response(response):
    return json.loads(response)


def execute_commands(execute):
    execute_result = []
    for command in execute:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        stdout, stderr = process.communicate()
        exitcode = process.returncode
        execute_result.append(
            {
                "command": command,
                "stdout": stdout.decode("utf-8"),
                "stderr": stderr.decode("utf-8"),
                "exitCode": exitcode,
            }
        )
    return execute_result


def add_to_log_file(log_file, summary):
    with open(log_file, "a") as file:
        file.write("\n" + summary)


def load_from_file(filename):
    with open(filename, "r") as file:
        return json.load(file)


def write_to_file(filename, content):
    with open(filename, "w") as file:
        json.dump(content, file)


write_to_file("execute_result.json", {})
write_to_file("log.json", [])

while True:
    user_input = input(">")

    execute_result = load_from_file("execute_result.json")
    log = read_file("log.json")

    text = build_template("prompt", execute_result, log, user_input)
    gpt4_response = chat_with_gpt4(text + "\n\n" + user_input)

    print(gpt4_response)

    response = parse_response(gpt4_response)

    if response["execute"]:
        execute_result = {
            "intention": response["intention"],
            "exec": execute_commands(response["execute"]),
        }
        print(execute_result)
        write_to_file("execute_result.json", execute_result)
    else:
        write_to_file("execute_result.json", {})

    if response["summary"]:
        add_to_log_file("log.json", "\n".join(response["summary"]))

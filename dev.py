import json
import subprocess

from chat import chat_with_gpt4


def read_file(file):
    with open(file, "r") as f:
        return f.read()


def read_files(files):
    contents = {}
    for file in files:
        try:
            contents[file] = read_file(file)
        except FileNotFoundError:
            contents[file] = "File not found"
        except Exception as e:
            contents[file] = f"Error reading file: {str(e)}"
    return contents


def build_template(
    template_file,
    execute_result_json,
    log_json,
    message_from_user,
    files_before_execute_json,
    files_after_execute_json,
):
    return read_file(template_file).format(
        log=log_json,
        execute_result=execute_result_json,
        message_from_user=message_from_user,
        files_before_execute=files_before_execute_json,
        files_after_execution=files_after_execute_json,
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

message_to_user = ["start"]

files_before_execution = {}
files_after_execution = {}

while True:
    if message_to_user:
        user_input = input("\n".join(message_to_user) + "\n>")
    else:
        user_input = ""

    execute_result = load_from_file("execute_result.json")
    log = read_file("log.json")

    text = build_template(
        "prompt",
        execute_result,
        log,
        user_input,
        json.dumps(files_before_execution, indent=4),
        json.dumps(files_after_execution, indent=4),
    )

    print("\n-------\n")

    print(text)

    gpt4_response = chat_with_gpt4(text)

    print(gpt4_response)

    response = parse_response(gpt4_response)

    if response.get("files"):
        files_before_execution = read_files(response.get("files"))

    if response.get("execute"):
        execute_result = {
            "intention": response["intention"],
            "exec": execute_commands(response["execute"]),
        }
        print(execute_result)
        write_to_file("execute_result.json", execute_result)
    else:
        write_to_file("execute_result.json", {})

    if response.get("files"):
        files_after_execution = read_files(response.get("files"))

    if response.get("summary"):
        add_to_log_file(
            "log.json",
            "thinking:\n"
            + "\n".join(response["thinking"])
            + "\nsummary:\n"
            + "\n".join(response["summary"])
            + "\nintention:\n"
            + "\n".join(response["intention"]),
        )

    message_to_user = response.get("message_to_user")

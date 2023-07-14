import argparse
import requests
import os


def chat_with_gpt4(text):
    """
    Initiates a chat with GPT-4 using the provided text. Uses environment variable "OPENAI_API_KEY" for authorization.
    Raises an exception if the environment variable is not found.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("Couldn't find the 'OPENAI_API_KEY' environment variable!")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(
            f"Request to GPT-4 API failed with status {response.status_code}. The response is: {response.text}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="The text to be used as prompt for GPT-4.")
    args = parser.parse_args()

    print(chat_with_gpt4(args.text))


if __name__ == "__main__":
    main()

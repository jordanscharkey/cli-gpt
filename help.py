import json
import subprocess
from pathlib import Path

import tiktoken

# TODO: I don't love the way this file is structured from an extensibility perspective.
# Find a way to maybe like the 'options' dict with the command list?

def start_chat(model: str):
    print("System: Welcome to cli-gpt. You may type your questions, or seek additional functionality via '/help'.")
    print(f"System: Currently using model '{model}'.")
    return [{"role": "system", "content": "You are a helpful assistant."}]

def get_token_count(messages: list, model: str):
    total_tokens: int = 0
    encoding = tiktoken.encoding_for_model(model)
    for message in messages:
        if message.get("role") == "system":
            continue
        text = message.get("content", "")
        message_tokens = len(encoding.encode(text))
        total_tokens += message_tokens
    return total_tokens

class HelpCommands:
    
    options: dict = {
        "/exit": "Closes the chat.",
        "/context": "Passthrough a URL to curl the context of into the chat history.",
        "/help": "Display this list of available commands.",
        "/load": "Load in a previous chat's JSON file.",
        "/save": "Saves messages to specified JSON file and closes chat.",
        "/clear": "Clears all messages and tokens from the chatlog, restarting the chat.",
        "/model": "Change the model being used.",
        "/info": "Print model information and cli-gpt version.",
    }

    text_models = [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-32k",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        "gpt-4-32k-0613",
        "gpt-4-1106-preview",
        "gpt-4-vision-preview",
    ]

    image_models = [
        "dall-e-2",
        "dall-e-3",
    ]

    model_type = None

    def __init__(self, model: str):
        if model in self.text_models:
            self.model_type = "text"
        elif model in self.image_models:
            self.model_type = "image"
        else:
            raise TypeError(f"System: Model '{model}' is not available. Please start again and re-specify model version, or leave blank.")


    def command(self, user_input: str, messages: list, model: str) -> (int, list, str):
        if user_input.lower() in list(self.options.keys()):
            user_input_lower = user_input.lower()

            if user_input_lower == "/exit":
                return 1, [None], ""

            if user_input_lower == "/context":
                print("\nSystem: Please provide the URL you would like to curl.")
                url = input("URL: ")
                curl_output = subprocess.check_output(f"curl {url}", shell=True).decode('utf-8').strip()
                return [None, f"I would like to provide the following context from a curl command to '{url} to this chat: {curl_output}"]

            if user_input_lower == "/help":
                print(f"\nSystem: Below is a list of available commands.\n")
                for key in list(self.options.keys()):
                    print(f" - {key}: {self.options[key]}")
                return 2, messages, model

            if user_input_lower == "/load":
                print("\nSystem: Please specify the filepath you would like to load in from, or '/cancel'.")
                url = input("Path: ")
                if url != "/cancel":
                    with open(Path(url), "r") as file:
                        messages = json.load(file)
                    print(f"System: Successfully read in from {url}. Continuing chat.")
                return 2, messages, model

            if user_input_lower == "/save":
                status, destination = self._save(messages)
                if status == 1:
                    return 2, messages, model
                print(f"System: Successfully saved to {destination}. Closing chat.")
                return 1, [None], ""

            if user_input_lower == "/clear":
                print(f"\nSystem: Clearing messages and restarting log.\n\n")
                messages = start_chat(model)
                return 2, messages, model

            if user_input_lower == "/info":
                print(f"\nSystem: This chatlog has used {get_token_count(messages, model)} token for model version '{model}'.")
                print("System: Currently using cli-gpt version 0.0.1.")
                return 2, messages, model

            if user_input_lower == "/model":
                print("\nSystem: Below is a list of available models. View up-to-date model information in the OpenAI API documentation.")
                print("\n - Text Models")
                for list_model in self.text_models:
                    print(f"   - {list_model}")
                print("\n - Image Models")
                for list_model in self.image_models:
                    print(f"   - {list_model}")
                print("\nSystem: Change model version below, use '/list' to reprint available models, or '/cancel' to return to chat.")
                new_model = input("\nModel: ")
                while new_model not in self.text_models and new_model not in self.image_models:
                    if new_model == "/list": 
                        print("\nSystem: Below is a list of available models. View up-to-date model information in the OpenAI API documentation.")
                        print("\n - Text Models")
                        for list_model in self.text_models:
                            print(f"   - {list_model}")
                        print("\n - Image Models")
                        for list_model in self.image_models:
                            print(f"   - {list_model}")
                    elif new_model == "/cancel":
                        return 2, messages, model
                    else:
                        print(f"System: '{new_model}' is not an accepted model. Use 'list' to output available models.")
                    new_model = input("\nModel: ")

                # "image" models and "text" models behave different, handle switching
                if (self.model_type == "text" and new_model in self.image_models) or (self.model_type == "image" and new_model in self.text_models):
                    print("\nSystem: Switching between 'text' and 'image' models requires clearing the current message log. Would you like to save before switching models?")
                    user_save = input("Save? (y,N): ")
                    if user_save.lower() == "y":
                        self._save(messages)
                return 2, messages, new_model

        messages.append({"role": "user", "content": user_input})
        return 0, messages, model

    def _save(self, messages):
        print("\nSystem: Please specify the filepath you would like to save to as a *.json file, or '/cancel'.")
        url = input("Path: ")
        if url == "/cancel":
            return 1, None
        with open(Path(url), "w+") as file:
            json.dump(messages, file)
        return 0, url


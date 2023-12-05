import json
import re
import subprocess
import sys
from pathlib import Path

import tiktoken

# TODO: I don't love the way this file is structured from an extensibility perspective.
# Find a way to maybe like the 'options' dict with the command list?

def start_chat(model: str, styler):
    sys.stdout.write('\033[2J\033[H')
    styler.prompt("none", "")
    styler.prompt("system", "Welcome to cli-gpt. You may type your questions, or seek additional functionality via '/help'.")
    styler.prompt("system", f"Currently using model '{model}'.")
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
        "/context": "Passthrough a URL to curl the context of into the chat history.", #TODO
        "/help": "Display this list of available commands.",
        "/load": "Load in a previous chat's JSON file.",
        "/save": "Saves messages to specified JSON file and closes chat.",
        "/clear": "Clears all messages and tokens from the chatlog, restarting the chat.",
        "/model": "Change the model being used.",
        "/info": "Print model information and cli-gpt version.",
        "/write": "Write out any code from the previous message to a specified file.",
        "/copy": "Copy code snippets from the previous message into the copy buffer.",
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


    def command(self, user_input: str, messages: list, model: str, styler) -> (int, list, str):
        if user_input.lower() in list(self.options.keys()):
            user_input_lower = user_input.lower()

            if "/exit" in user_input_lower:
                return 1, [None], ""

            if "/context" in user_input_lower:
                styler.prompt("system", "Please provide the URL you would like to curl.")
                url = input("URL: ")
                curl_output = subprocess.check_output(f"curl {url}", shell=True).decode('utf-8').strip()
                return [None, f"I would like to provide the following context from a curl command to '{url} to this chat: {curl_output}"]

            if "/help" in user_input_lower:
                styler.prompt("system", "Below is a list of available commands.")
                for key in list(self.options.keys()):
                    styler.prompt("none", f" - {key}: {self.options[key]}")
                return 2, messages, model

            if "/load" in user_input_lower:
                styler.prompt("system", "Please specify the filepath you would like to load in from, or '/cancel'.")
                path = input("Path: ")
                if path != "/cancel":
                    with open(Path(path), "r") as file:
                        messages = json.load(file)
                    styler.prompt("system", f"Successfully read in from {path}. Continuing chat.")
                return 2, messages, model

            if "/save" in user_input_lower:
                status, destination = self._save(messages)
                if status == 1:
                    return 2, messages, model
                styler.prompt("system", f"Successfully saved to {destination}. Closing chat.")
                return 1, [None], ""

            if "/clear" in user_input_lower:
                styler.prompt("system", "Clearing messages and restarting log.\n\n")
                messages = start_chat(model, styler)
                return 2, messages, model

            if "/info" in user_input_lower:
                styler.prompt("system", f"This chatlog has used {get_token_count(messages, model)} token for model version '{model}'.")
                styler.prompt("system", "Currently using cli-gpt version 0.0.1.")
                return 2, messages, model

            if "/model" in user_input_lower:
                styler.prompt("system", "Below is a list of available models. View up-to-date model information in the OpenAI API documentation.")
                styler.prompt("none", "\n - Text Models")
                for list_model in self.text_models:
                    styler.prompt("none", f"   - {list_model}")
                styler.prompt("none", "\n - Image Models")
                for list_model in self.image_models:
                    styler.prompt("none", f"   - {list_model}")
                styler.prompt("system", "Change model version below, use '/list' to reprint available models, or '/cancel' to return to chat.")
                new_model = input("\nModel: ")
                while new_model not in self.text_models and new_model not in self.image_models:
                    if new_model == "/list": 
                        styler.prompt("system", "Below is a list of available models. View up-to-date model information in the OpenAI API documentation.")
                        styler.prompt("none", "\n - Text Models")
                        for list_model in self.text_models:
                            styler.prompt("none", f"   - {list_model}")
                        styler.prompt("none", "\n - Image Models")
                        for list_model in self.image_models:
                            styler.prompt("none", f"   - {list_model}")
                    elif new_model == "/cancel":
                        return 2, messages, model
                    else:
                        print(f"System: '{new_model}' is not an accepted model. Use 'list' to output available models.")
                    new_model = input("\nModel: ")

                # "image" models and "text" models behave different, handle switching
                if (self.model_type == "text" and new_model in self.image_models) or (self.model_type == "image" and new_model in self.text_models):
                    styler.prompt("system", "Switching between 'text' and 'image' models requires clearing the current message log. Would you like to save before switching models?")
                    user_save = input("Save? (y,N): ")
                    if user_save.lower() == "y":
                        self._save(messages)
                return 2, messages, new_model

            if "/write" in user_input_lower:
                pattern = r'```(.*?)```'
                code_blocks = re.findall(pattern, messages[-1]['content'], re.DOTALL)
                print(f"\nSystem: Found {len(code_blocks)} code examples.")
                for block in code_blocks:
                    block = re.sub(r'^.*\n', '', block)
                    print(f"\n{block}")
                    print("\nSystem: Please specify the filepath you would like to load in from, or '/cancel'.")
                    path = input("Path: ")
                    if path == "/cancel":
                        return 2, messages, model
                    with open(Path(path), "w+") as file:
                        file.write(block)
                print(f"System: Successfully saved code snippets. Continuing chat.")
                return 2, messages, model


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


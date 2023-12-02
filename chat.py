import queue
import sys
import threading
import time

from openai import OpenAI

from help import HelpCommands, start_chat
from style import StyleLog

# Read in token from "token" file
# TODO: env variable in future?
with open("token", "r") as file:
    token = file.readlines()
client = OpenAI(api_key=token[0].strip())

def text_call(api_call_queue, messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    api_call_queue.put(response.choices[0].message.content)

def image_call(api_call_queue, messages, model):
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    api_call_queue.put(response.choices[0].message.content)

def main():

    model = ""
    if len(sys.argv) > 1:
        model = sys.argv[1]
    else:
        model = "gpt-3.5-turbo"

    helper = HelpCommands(model)
    styler = StyleLog()
    messages = start_chat(model)

    while True:
        # TODO: Format output nicer :)
        user_input = input("\nInput: ")

        status, messages, model = helper.command(user_input, messages, model)
        if status == 1:
            break
        elif status == 2:
            continue

        global api_call_done
        api_call_done = threading.Event()
        api_call_queue = queue.Queue()

        if model == "dall-e-2" or model == "dall-e-3":
            response_thread = threading.Thread(target=image_call, args=(api_call_queue, messages, model,))
        else:
            response_thread = threading.Thread(target=text_call, args=(api_call_queue, messages, model,))
        response_thread.start()

        ellipsis_thread = threading.Thread(target=styler.show_ellipsis, args=(api_call_done,))
        ellipsis_thread.start()

        response_thread.join()
        api_call_done.set()
        ellipsis_thread.join()

        ai_response = api_call_queue.get()
        messages.append({"role": "assistant", "content": ai_response})
        print(f"\nAI: {ai_response}\n")

        # TODO: Add some form of token check, as to not overflow


if __name__ == "__main__":
    main()

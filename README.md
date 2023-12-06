                                                        
     ██████╗██╗     ██╗       ██████╗ ██████╗ ████████╗
    ██╔════╝██║     ██║      ██╔════╝ ██╔══██╗╚══██╔══╝
    ██║     ██║     ██║█████╗██║  ███╗██████╔╝   ██║   
    ██║     ██║     ██║╚════╝██║   ██║██╔═══╝    ██║   
    ╚██████╗███████╗██║      ╚██████╔╝██║        ██║   
     ╚═════╝╚══════╝╚═╝       ╚═════╝ ╚═╝        ╚═╝   
                                                   

cli-gpt is a ChatGPT-like terminal wrapper to make interfacing with GPT models with an OpenAI API key easier.

## Installation

### Requirements

I've tried to keep requirements low as to keep the program pretty minimal. Outside of native Python libraries, we're grabbing `openai` (obviously) to interface with the OpenAI API, `tiktoken` to get token information, `selenium` for URL parsing, and `prompt_toolkit` + `pygments` for better terminal handling.

To install and run the program, simply execute the following commands.
```
# Create environment
python -m venv .venv/
. .venv/bin/activate
pip install -r requirements.txt
```

### Token File

To use this program, you will need an OpenAI API key. Keep this token in a file named `key` in the repository directory and the program should automatically read from it.

### Usage

Simply run the program using the following command in the repository directory

```
python src/chat.py
```

## Additional Functionalities

In addition to expected chat-bot call/response functionality, the `/help` command will list all commands and a short description of what that command will accomplish. Here is a summary of those commands:

```
 - /exit: Closes the chat.
 - /context: Passthrough a URL or filepath to add context into the chat history.
 - /help: Display this list of available commands.
 - /load: Load in a previous chat's JSON file.
 - /save: Saves messages to specified JSON file and closes chat.
 - /clear: Clears all messages and tokens from the chatlog, restarting the chat.
 - /model: Change the model being used.
 - /info: Print model information and cli-gpt version.
 - /write: Write out any code from the previous message to a specified file.
```

## TODO:

Implementations I'm still working on include:

- "/copy" function to easily copy/paste codeblocks from assistant messages
- Better handling of key reading (perhaps an environment variable)
- Condensing token usage
- Switching between text and image models
- More intuitive command handling, particularly with "/cancel" catching
- More robust error handling :) 

## Contact

For any inquiries, please reach out to [jordan@schark.online](mailto:jordan@schark.online). A mirror of this repositor can be found at [https://git.schark.online/cli-gpt/](https://git.schark.online/cli-gpt).

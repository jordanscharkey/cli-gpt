                                                        
     ██████╗██╗     ██╗       ██████╗ ██████╗ ████████╗
    ██╔════╝██║     ██║      ██╔════╝ ██╔══██╗╚══██╔══╝
    ██║     ██║     ██║█████╗██║  ███╗██████╔╝   ██║   
    ██║     ██║     ██║╚════╝██║   ██║██╔═══╝    ██║   
    ╚██████╗███████╗██║      ╚██████╔╝██║        ██║   
     ╚═════╝╚══════╝╚═╝       ╚═════╝ ╚═╝        ╚═╝   
                                                   

cli-gpt is a ChatGPT-like terminal wrapper to make interfacing with GPT models with an OpenAI API key easier.

## Requirements and Installation

I've tried to keep requirements low as to keep the program pretty minimal. Outside of native Python libraries, we're grabbing `openai` (obviously) to interface with the OpenAI API, `tiktoken` to get token information, and `prompt_toolkit` + `pygments` for better terminal handling.

To install and run the program, simply execute the following commands.
```
# Clone repository
git clone https://github.com/jordanscharkey/cli-gpt.git
cd cli-gpt/

# Create environment
python -m venv .venv/
. .venv/bin/activate
pip install -r requirements.txt

# Fill token file and run
vim token
python chat.py
```

### Token File

To use this program, you will need an OpenAI API key. Keep this token in a file named `key` in the repository and the program should automatically read from it.

## Additional Functionality

The `/help` command will list all commands and a short description of what that command will accomplish. Here is a summary of those commands:

```
 - /exit: Closes the chat.
 - /context: Passthrough a URL to curl the context of into the chat history.
 - /help: Display this list of available commands.
 - /load: Load in a previous chat's JSON file.
 - /save: Saves messages to specified JSON file and closes chat.
 - /clear: Clears all messages and tokens from the chatlog, restarting the chat.
 - /model: Change the model being used.
 - /info: Print model information and cli-gpt version.
 - /write: Write out any code from the previous message to a specified file.
 - /copy: Copy code snippets from the previous message into the copy buffer.
```

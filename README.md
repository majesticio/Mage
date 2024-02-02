# Mage
## Installation
`pipenv shell`  
`pip install requirements.txt`

## Overview
This project creates a realistic voice assistant with powerful and flexible AI integration. All of the files work modularly, and just pass files to each other, except for the LLM which can either be selfhosted or dropin OpenAI's API - interchangeably.


## Quick start
### SSH proxy a remote server (optional)
>will use remote host as localhost!

`ssh -L 1234:localhost:8000 samus@192.168.5.58`

### Run the shell script
>Make sure start.sh is executable `chmod +x start.sh`  

`pipenv shell`  <-- start your virtual ennvironment

`./start.sh`

### Meanwhile.. run that AI assistant
> giving away pearls here. this could be added to start.sh, however I am running it on another machine. ITS VERY IMPORTANT too correctly identify the model `author/llm-model`. It will automatically download the named file if you are signed in to huggingface CLI.


```bash 
python -m vllm.entrypoints.openai.api_server \
    --model mistralai/Mistral-7B-Instruct-v0.2 \
    --max-model-len 16284
```
That last flag reduces the context windows and saves you a lot of compute.  

The chat assistant needs to have the IP and port with the OpenAI style endpoint, like `http://localhost:8000/v1`

## Usage
Simply press the space bar and speak. Mage will respond in Kind
>TODO: add abillities

## Run seperately (optional)
*Each file needs its own shell and active virtual environment*. This might seem like a hindrance but the compute needed for some of the better models may cause you to split your resources across devices.

1. Create a tunnel localhost proxy from your machine to chatbot host (if needed)
    - `ssh -L 8000:localhost:8000 samus@192.168.5.58` 

2. transcribe
    - `python transcriber.py` 

3. speak
    - `python speaker.py`

4. record
    - works by holding the space bar (for now)
    - `sudo recorder.py`

5. chat
    - `chat_assistant.py`



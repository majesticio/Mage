# Mage
`pipenv shell`  
`pip install requirements.txt`

## Overview
This project creates a realistic voice assistant with powerful and flexible AI integration. All of the files work modularly, and just pass files to each other, except for the LLM which can either be selfhosted or OpenAI's API interchangeably.

*Each file needs its own shell and active virtual environment*. This might seem like a hindrance but the compute needed for some of the better models may cause you to split your resources across devices.

## Run
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


### Meanwhile..
> giving away pearls here
```bash
pip install vllm
```

```bash 
python -m vllm.entrypoints.openai.api_server --model author/model --max-model-len 8192 
```
That last flag reduces the context windows and saves you a lot of compute.  

The chat assistant needs to have the IP and port with the OpenAI style endpoint, like `http://localhost:8000/v1`
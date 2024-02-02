#!/bin/bash

echo "Starting transcriber.py in a new Alacritty window..."
alacritty -e sh -c 'echo "Running transcriber.py"; python transcriber.py; echo "transcriber.py completed"' &
sleep 10

echo "Starting speaker.py in a new Alacritty window..."
alacritty -e sh -c 'echo "Running speaker.py"; python speaker.py; echo "speaker.py completed"' &
sleep 10

echo "Starting recorder.py with sudo in a new Alacritty window..."
alacritty -e sh -c 'echo "Running recorder.py with sudo"; sudo python recorder.py; echo "recorder.py completed"' &
sleep 5

echo "Opening SSH session in a new Alacritty window..."
# alacritty -e sh -c 'ssh -L 1234:localhost:8000 user@host' &
sleep 5

# Now running chat_assistant.py in the foreground, ensuring user interaction is seamless.
echo "Now running chat_assistant.py in the foreground..."
echo "Please interact with the chat assistant as needed."
python chat_assistant.py

echo "chat_assistant.py has completed. All tasks done."

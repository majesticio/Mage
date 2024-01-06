from chat_assistant import ChatAssistant
from speaker import Speaker
from transcriber import Transcriber
from recorder import AudioRecorder
import threading
import signal

class ThreadController:
    def __init__(self):
        self.active = True

def main():
    controller = ThreadController()

    assistant = ChatAssistant(
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        history_file="chat_history.json"
    )
    
    speaker = Speaker()
    transcriber = Transcriber()
    recorder = AudioRecorder()

    def run_thread(target):
        while controller.active:
            target()

    chat_thread = threading.Thread(target=lambda: run_thread(assistant.chat))
    speaker_thread = threading.Thread(target=lambda: run_thread(speaker.run))
    transcriber_thread = threading.Thread(target=lambda: run_thread(transcriber.run))
    recorder_thread = threading.Thread(target=lambda: run_thread(recorder.run))

    chat_thread.start()
    speaker_thread.start()
    transcriber_thread.start()
    recorder_thread.start()

    try:
        # Wait for threads to complete
        chat_thread.join()
        speaker_thread.join()
        transcriber_thread.join()
        recorder_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        controller.active = False

if __name__ == "__main__":
    main()

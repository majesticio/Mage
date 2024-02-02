import os
import time
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play
import torch

MODEL_NAME = "tts_models/en/jenny/jenny"
# MODEL_NAME = "tts_models/en/vctk/vits"

class Speaker:
    def __init__(self, model_name=MODEL_NAME, wav_dir="../speaker/", responses_dir="responses/"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_engine = TTS(model_name=model_name, progress_bar=True).to(self.device)
        # self.tts_engine.tts_to_file(text=text, file_path=out_path, speaker="p230") # vits
        self.wav_dir = wav_dir
        self.responses_dir = responses_dir
        self.audio_lock = threading.Lock()  # Ensure only one audio file plays at a time
        self.executor = ThreadPoolExecutor(max_workers=4)  # Manage threads efficiently

        if not os.path.exists(self.wav_dir):
            os.makedirs(self.wav_dir)
        if not os.path.exists(self.responses_dir):
            os.makedirs(self.responses_dir)

    def speak(self, text, out_path):
        try:
            self.tts_engine.tts_to_file(text=text, file_path=out_path)
            audio = AudioSegment.from_wav(out_path)
            with self.audio_lock:  # Acquire lock to ensure exclusive playback
                play(audio)
            os.remove(out_path)
        except Exception as e:
            print(f"Error during speech synthesis or playback: {e}")

    def process_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                text = file.read()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            wav_file_path = f"{self.wav_dir}response_{timestamp}.wav"
            # Use executor to manage thread lifecycle
            self.executor.submit(self.speak, text, wav_file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        finally:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")

    def get_oldest_file(self):
        try:
            files = [os.path.join(self.responses_dir, f) for f in os.listdir(self.responses_dir) if f.endswith('.txt')]
            if not files:
                return None
            return min(files, key=os.path.getctime)
        except Exception as e:
            print(f"Error getting oldest file: {e}")
            return None

    def run(self):
        try:
            while True:
                oldest_file = self.get_oldest_file()
                if oldest_file:
                    self.process_file(oldest_file)
                else:
                    time.sleep(1)
        except KeyboardInterrupt:
            print("Shutting down gracefully...")
        finally:
            self.executor.shutdown(wait=True)

# Example usage
if __name__ == "__main__":
    speaker = Speaker()
    speaker.run()

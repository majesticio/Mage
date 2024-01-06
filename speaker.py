import os
import time
import threading
from datetime import datetime
from TTS.api import TTS
from pydub import AudioSegment
from pydub.playback import play
import torch

class Speaker:
    def __init__(self, model_name="tts_models/en/vctk/vits", wav_dir="../speaker/", responses_dir="responses/"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts_engine = TTS(model_name=model_name, progress_bar=False).to(self.device)
        self.wav_dir = wav_dir
        self.responses_dir = responses_dir

        if not os.path.exists(self.wav_dir):
            os.makedirs(self.wav_dir)

    def speak(self, text, out_path):
        self.tts_engine.tts_to_file(text=text, file_path=out_path, speaker="p230")
        audio = AudioSegment.from_wav(out_path)
        play(audio)
        os.remove(out_path)

    def process_file(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_file_path = f"{self.wav_dir}response_{timestamp}.wav"
        threading.Thread(target=self.speak, args=(text, wav_file_path)).start()
        os.remove(file_path)

    def get_oldest_file(self):
        files = [os.path.join(self.responses_dir, f) for f in os.listdir(self.responses_dir) if f.endswith('.txt')]
        if not files:
            return None
        return min(files, key=os.path.getctime)

    def run(self):
        while True:
            oldest_file = self.get_oldest_file()
            if oldest_file:
                self.process_file(oldest_file)
            else:
                time.sleep(1)

# Example usage in master.py
if __name__ == "__main__":
    speaker = Speaker()
    speaker.run()

import os
import whisper
import time
from datetime import datetime

class Transcriber:
    def __init__(self, model_name="tiny", recordings_folder="recordings", prompts_folder="prompts"):
        self.model = whisper.load_model(model_name)
        self.recordings_folder = recordings_folder
        self.prompts_folder = prompts_folder

        # Ensure prompts directory exists
        if not os.path.exists(self.prompts_folder):
            os.makedirs(self.prompts_folder)

        # Ensure recordings directory exists
        if not os.path.exists(self.recordings_folder):
            os.makedirs(self.recordings_folder)

    def get_earliest_file(self):
        files = [f for f in os.listdir(self.recordings_folder) if os.path.isfile(os.path.join(self.recordings_folder, f))]
        if not files:
            return None
        earliest_file = min(files, key=lambda x: datetime.strptime(x.replace('.wav', ''), '%Y%m%d_%H%M%S'))
        return os.path.join(self.recordings_folder, earliest_file)

    def save_transcription(self, text):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(self.prompts_folder, f"transcription_{timestamp}.txt")
        with open(file_path, 'w') as file:
            file.write(text)
        print(f"Transcription saved to {file_path}")

    def run(self):
        while True:
            try:
                earliest_filename = self.get_earliest_file()

                if earliest_filename:
                    result = self.model.transcribe(earliest_filename, fp16=False)
                    print("Transcribing:", earliest_filename)
                    transcription = result['text']
                    print(transcription)

                    self.save_transcription(transcription)

                    try:
                        os.remove(earliest_filename)
                        print(f"Deleted file: {earliest_filename}")
                    except OSError as e:
                        print(f"Error deleting file {earliest_filename}: {e}")

                else:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nExiting program...")
                break

# Example usage in master.py
if __name__ == "__main__":
    transcriber = Transcriber()
    transcriber.run()

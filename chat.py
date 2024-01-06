import json
from openai import OpenAI

class ChatAssistant:
    def __init__(self, base_url, api_key, history_file, max_history_entries=100):
        self.base_url = base_url
        self.api_key = api_key
        self.history_file = history_file
        self.max_history_entries = max_history_entries
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)
        self.history = self.load_history()

    def load_history(self):
        try:
            with open(self.history_file, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return [
                {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
                {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
            ]

    def save_history(self):
        with open(self.history_file, "w") as file:
            json.dump(self.history[-self.max_history_entries:], file, indent=2)

    def chat(self):
        while True:
            try:
                completion = self.client.chat.completions.create(
                    model="local-model",
                    messages=self.history[-self.max_history_entries:],
                    temperature=0.7,
                    stream=True,
                )

                new_message = {"role": "assistant", "content": ""}

                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="", flush=True)
                        new_message["content"] += chunk.choices[0].delta.content

                self.history.append(new_message)

                print()

                user_input = input("> ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                self.history.append({"role": "user", "content": user_input})

                self.save_history()

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        print("Session ended.")


# Example usage
if __name__ == "__main__":
    assistant = ChatAssistant(
        base_url="http://localhost:1234/v1",
        api_key="not-needed",
        history_file="chat_history.json"
    )
    assistant.chat()

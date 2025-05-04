import openai

class AskGPT:
    def __init__(self, api_key="your_key"):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.chat_history = []

    def ask(self, prompt):
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"An error occurred: {e}"
    def ask_with_history(self, prompt):
        self.chat_history.append({"role": "user", "content": prompt})
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.chat_history
            )
            answer = response['choices'][0]['message']['content'].strip()
            self.chat_history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            return f"An error occurred: {e}"
    def clear_history(self):
        self.chat_history = []
    def get_history(self):
        return self.chat_history
    def set_api_key(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
    def get_api_key(self):
        return self.api_key
        
if __name__ == "__main__":
    # Example usage
    api_key = "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"
    gpt = AskGPT(api_key)
    prompt = "What is the capital of France?"
    response = gpt.ask(prompt)
    print(response)  # Should print "Paris"

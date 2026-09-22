from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            break

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "user", "content": "My name is LoopKaka"},
                {"role": "assistant", "content": "Hello, LoopKaka! How can I assist you today?"},
                {"role": "user", "content": user_input},
            ]
        )

        print("LLM: ", response.output_text.strip())
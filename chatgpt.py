# Import the necessary libraries
import openai
import os

# Authenticate with your OpenAI API key
openai.api_key = "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"

def chat(question):
    # Create a chat context with an initial prompt

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=1024,
        temperature=0.5,
    )
    # Use the chat context to generate a response from ChatGPT
    response = response["choices"][0]["text"]
    print(response)
    return response
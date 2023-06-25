# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 10:07:44 2023

@author: Md. Asrahraful Haque
"""

import openai

openai.api_key = "API_KEY_OPENAI"

def generate_response(prompt):
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print("An error occurred:", str(e))
        return None

prompt = "Once upon a time"

response = generate_response(prompt)

if response is not None:
    print("Generated response:")
    print(response)
else:
    print("Failed to generate a response. Please check the error message above.")
from openai_chat import ChatCompletion

# Define your prompt or initial message
prompt = "Hello, chatbot!"

# Initialize the ChatCompletion class
chatbot = ChatCompletion(api_key='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')

# Create an array of message objects for the chat
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': prompt}
]

# Generate a chat response
response = chatbot.chat('davinci-codex', messages)

# Extract the chatbot's response
reply = response['choices'][0]['message']['content']

# Process and display the chatbot's response
print("Chatbot:", reply)

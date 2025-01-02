import os
import subprocess
import pyautogui
import pyttsx3
import speech_recognition as sr
import requests
import random
import ollama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Function: Query Llama 2
def query_llama2(query):
    """Generates a response to the query using the Ollama API."""
    try:
        response = ollama.chat(
            model="llama2",  # Specify the model you want to use
            messages=[
                {"role": "user", "content": f"Respond to the following query: \"{query}\""}
            ]
        )
        response_text = response['message']['content'].strip()  # Extract the response content
        print(response_text)
        return response_text  # Filter unsupported characters
    except Exception as e:
        print(f"Error generating response: {e}")
        return None
    
# Function: Execute Commands
def execute_command(command):
    command = command.lower()
    if "open chrome" in command:
        os.system("start chrome")
        speak("Opening Google Chrome.")
    elif "close chrome" in command:
        os.system("taskkill /im chrome.exe /f")
        speak("Closing Google Chrome.")
    else:
        speak("Command not recognized. Please try again.")


# Function: Text-to-Speech
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Function: Get Voice Command
def get_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening for your command.")
        try:
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand you."
        except sr.RequestError:
            return "Could not request results; check your internet connection."
        except Exception as e:
            return f"Error: {e}"


# Function: Classify Prompt
def classify_prompt(prompt):
    prompt = prompt.lower()
    if prompt.startswith(("who is", "what is", "how can", "explain", "tell me about")):
        return "information"
    else:
        return "task"


# Fetching random news article
def fetch_news():
    news_api_url = "https://newsapi.org/v2/everything"
    params = {
        "domains": "wsj.com",
        "q": "technology",
        "apiKey": "4e67960493ca496d8c15cd966c94e3a5",
        "pageSize": 10,  # Fetch 10 articles
    }
    try:
        response = requests.get(news_api_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        articles = data.get("articles", [])
        if articles:
            random_article = random.choice(articles)
            return random_article.get('content', "No content available.")
        print("No articles found.")
        return None
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


# Helper function to filter unsupported characters
def filter_bmp_characters(text):
    return ''.join(char for char in text if ord(char) <= 0xFFFF)


# Main Function
def main():
    speak("Greetings Master, I am Iggiris present in front of you to assist you.")
    while True:
        try:
            # Step 1: Get Voice Input
            voice_command = get_voice_command()
            print(f"User: {voice_command}")  # Print the user's voice command

            if "exit" in voice_command.lower() or "quit" in voice_command.lower():
                speak("Goodbye!")
                print("User: Goodbye!")  # Print exit command in terminal
                break

            # Step 2: Classify Prompt
            intent = classify_prompt(voice_command)

            if intent == "information":
                # Use Llama 2 for answering information-based prompts
                speak(f"Yes Mastes Lest me just quickly search for {voice_command}")
                ai_response = query_llama2(voice_command)
                speak(f"Master {ai_response}")
            elif intent == "task":
                # Use local commands for task-based prompts
                speak(f"Processing your command: {voice_command}.")
                print(f"User: {voice_command}")  # Print the user's voice command again
                ai_response = query_llama2(
                    f"Convert the following user command into a precise actionable task: {voice_command}"
                )
                print(f"AI: {ai_response}")  # Print the AI's response in terminal
                if "error" not in ai_response.lower():
                    execute_command(ai_response)
                else:
                    speak("I am sorry Master but i could not process the command.")

        except KeyboardInterrupt:
            speak("Exiting. Goodbye!")
            print("User: Goodbye!")  # Print exit command in terminal
            break


# Run the Assistant
if __name__ == "__main__":
    main()

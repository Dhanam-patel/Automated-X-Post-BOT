import requests
import random
import ollama
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Step 1: Fetch news articles
def fetch_news():
    """Fetches a random news article about technology from the Wall Street Journal."""
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
            # Select a random article from the fetched articles
            random_article = random.choice(articles)
            return random_article.get('content', "No content available.")
        print("No articles found.")
        return None
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

# Helper function to filter unsupported characters
def filter_bmp_characters(text):
    """Remove characters that are not in the Basic Multilingual Plane (BMP)."""
    return ''.join(char for char in text if ord(char) <= 0xFFFF)

# Step 2: Use Ollama to create a tweet (summarize the news)
def create_tweet(news_text):
    """Generates a tweet summarizing the news using the Ollama API."""
    try:
        response = ollama.chat(
            model="llama2",  # Specify the model you want to use
            messages=[
                {"role": "user", "content": f"Summarize this news article  \"{news_text}\" into a highly engaging X (formerly known as Twitter) post in 270 characters."}
            ]
        )
        tweet_text = response['message']['content'].strip()  # Extract the response content
        return filter_bmp_characters(tweet_text)  # Filter unsupported characters
    except Exception as e:
        print(f"Error generating tweet: {e}")
        return None

# Step 3: Automate posting the tweet using Selenium
def post_to_x(tweet_text):
    """Automates logging in and navigating to the post section, filling the tweet, and waiting for manual posting."""
    driver = None  # Initialize the WebDriver to handle potential exceptions
    try:
        # Decoder
        with open("X_POST_AI/Credentials.txt") as f:
            UserInput = f.read()
        words = UserInput.split(" ")
        DFinal = []
        for SingWord in words:
            if len(SingWord) > 7:
                DNewWord = "" + SingWord[len(SingWord)-3] + SingWord[len(SingWord)-4] + SingWord[2:len(SingWord)-4]
            else:
                DNewWord = SingWord[2:len(SingWord)-2][::-1]
            DFinal.append(DNewWord)
        mail = DFinal[0]
        username = DFinal[1]
        password = DFinal[2]

        twitter_email = f"{mail}@gmail.com"
        twitter_username = f"@{username}"
        twitter_password = f"{password}"

        # Initialize WebDriver
        driver = webdriver.Chrome()
        driver.get("https://twitter.com/login")

        print("Logging in to Twitter...")

        # Enter username
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_input.send_keys(twitter_username)
        username_input.send_keys(Keys.RETURN)

        # Handle email prompt if present
        try:
            email_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            email_input.send_keys(twitter_email)
            email_input.send_keys(Keys.RETURN)
        except:
            print("Email prompt not displayed. Proceeding...")

        # Enter password
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_input.send_keys(twitter_password)
        password_input.send_keys(Keys.RETURN)

        # Wait until logged in and redirect to home page
        WebDriverWait(driver, 10).until(
            EC.url_contains("home")
        )

        print("Login successful. Navigating to the tweet composer...")

        # Navigate to tweet composer
        driver.get("https://twitter.com/compose/tweet")

        # Wait for the tweet text box to be ready
        tweet_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweetTextarea_0']"))
        )
        tweet_box.send_keys(tweet_text)

        print("Tweet text filled. You have 10 seconds to review and post manually.")
        time.sleep(10)

        print("Closing the browser automatically.")
        print("\nProcess Completed Successfully!!!")

    except Exception as e:
        print(f"Error posting tweet: {e}")

    finally:
        if driver:
            driver.quit()

# Main script
def main():
    """Main function to fetch news, generate a tweet, and post it."""
    news = fetch_news()
    if news:
        print("Fetched News:", news)
        tweet = create_tweet(news)
        if tweet:
            print("Generated Tweet:", tweet)
            post_to_x(tweet)
        else:
            print("Failed to generate tweet.")
    else:
        print("Failed to fetch news.")

if __name__ == "__main__":
    main()
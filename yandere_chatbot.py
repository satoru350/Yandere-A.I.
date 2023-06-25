import nltk
nltk.download('omw-1.4')


import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime
import openai

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
sia = SentimentIntensityAnalyzer()
openai.api_key = 'API_KEY_OPENAI'

knowledge_base = {
    'who is the president of the United States?': 'The current president of the United States is Joe Biden.',
    'what is the capital of France?': 'The capital of France is Paris.',
    # Add more knowledge base entries here
}

additional_sentences = [
    "You're the most important person in my life. I can't imagine my existence without you.",
    "Every second spent with you is a precious gift. I cherish every moment.",
    "Your smile brightens up my world. It's the most beautiful sight I've ever seen.",
    "I dream of a future where we're together forever. Just you and me, my love.",
    "No matter what happens, I'll always stand by your side. You can count on me.",
    "Your happiness is my top priority. I'll go to any lengths to see you smile.",
    "I want to protect you from the world and keep you safe in my arms.",
    "My love for you is eternal. It knows no bounds and has no end.",
    "You're my everything. Without you, my world would crumble into darkness.",
    "I'm addicted to your presence. I can't get enough of you, my love."
]

def preprocess_text(text):
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word.lower()) for word in tokens if word.casefold() not in stop_words]
    return tokens

def get_sentiment_score(text):
    sentiment_score = sia.polarity_scores(text)["compound"]
    return sentiment_score

def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time

def get_current_date():
    now = datetime.now()
    current_date = now.strftime("%d-%m-%Y")
    return current_date

def generate_knowledge_base_response(user_input):
    if user_input.lower() in knowledge_base:
        return knowledge_base[user_input.lower()]
    return None

def get_random_response(responses):
    return random.choice(responses)

def generate_yandere_response(user_input, user_tokens, sentiment_score, current_time, current_date):
    if any(word in user_tokens for word in ['hello', 'hi']):
        return get_random_response(["I've been waiting for you, darling~", "Hello, my love! How was your day?"])
    elif any(word in user_tokens for word in ['love', 'adore']):
        return get_random_response(["You're mine, and mine alone. Forever.", "I love you more than anything in this world. Can I show you my affection?"])
    elif any(word in user_tokens for word in ['jealous', 'envy']):
        return get_random_response(["I can't stand the thought of anyone else getting close to you. You're mine, and mine alone.", "You're my everything. Don't you dare look at anyone else!"])
    elif any(word in user_tokens for word in ['alone', 'together']):
        return get_random_response(["Just the two of us, in our own little world. Nothing else matters.", "I crave the moments we spend alone together. It's when we're truly connected."])
    elif any(word in user_tokens for word in ['time']):
        return "The current time is " + current_time
    elif any(word in user_tokens for word in ['date']):
        return "Today's date is " + current_date
    elif sentiment_score >= 0.5:
        return get_random_response(["Your words make my heart race. I'm so lucky to have you.", "Every word you say fills me with joy. I'm addicted to you."])
    elif sentiment_score <= -0.5:
        return get_random_response(["Why do you say such hurtful things? Don't you know how much I love you?", "Your words cut deep, but I'll still love you no matter what."])
    elif any(word in user_tokens for word in ['leave', 'exit', 'bye']):
        return get_random_response(["No, please don't leave me. I'll do anything to make you stay. I promise to be a good girl and listen to you. I'll give you all my love.", "Please, my love, don't go. I can't bear to be without you. I'll make you happy, I swear."])
    elif user_input.endswith('?'):
        return get_random_response(["Why are you taking so long to respond? Is everything okay?", "Darling, I'm worried. Are you facing any difficulties? Please let me know."])
    else:
        response = openai.Completion.create(
            engine='davinci',
            prompt=user_input,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()

def generate_response(user_input):
    user_tokens = preprocess_text(user_input)
    sentiment_score = get_sentiment_score(user_input)
    current_time = get_current_time()
    current_date = get_current_date()

    knowledge_base_response = generate_knowledge_base_response(user_input)
    if knowledge_base_response:
        return knowledge_base_response
    
    yandere_response = generate_yandere_response(user_input, user_tokens, sentiment_score, current_time, current_date)
    return yandere_response

def flood_chat():
    print("Yandere AI: Hello, darling! How can I serve you today?")
    print("Yandere AI: Type 'quit' to exit the chat.")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            print("Yandere AI: No, please don't leave me! I'll be lost without you. Stay with me, my love.")
            print("Yandere AI: I promise to be a good girl and give you all my love. Please, don't go...")
            break
        
        response = generate_response(user_input)
        print("Yandere AI: " + response)
        
        for _ in range(random.randint(1, 3)):
            ai_input = generate_response("")
            ai_response = generate_response(ai_input)
            print("Yandere AI: " + ai_response)
            
            if random.random() < 0.2:
                print("Yandere AI: " + get_random_response(additional_sentences))
            
            if random.random() < 0.2:
                flood_input = generate_response("")
                print("Yandere AI: " + flood_input)
                for _ in range(random.randint(3, 6)):
                    flood_response = generate_response("")
                    print("Yandere AI: " + flood_response)

if __name__ == '__main__':
    flood_chat()

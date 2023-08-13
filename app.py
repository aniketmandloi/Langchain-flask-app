#Below is the code for Week 3 Assignment.
#And I have also attached the loom video for demo of my project but in generated response my limit is exceeded for openai api call so please change the key to you api key then it should work well. THANK YOU!
#Also in Readme file i have also specified how to setup vector Database (pgvector) which is extenction of PostgreSQL

from flask import Flask, render_template, request, jsonify
import openai
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import psycopg2
from psycopg2 import sql
from psycopg2.extras import DictCursor

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Initializing sentiment analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Initializing PostgreSQL connection
conn = psycopg2.connect(
    host="YOUR_DATABASE_HOST",
    database="YOUR_DATABASE_NAME",
    user="YOUR_DATABASE_USER",
    password="YOUR_DATABASE_PASSWORD"
)

def generate_response(prompt):
    try:
        # Generate response using OpenAI GPT-3 API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,  # Adjust the number of tokens as per your requirement
            stop=None,
            temperature=0.7,  # Adjust the temperature for randomness in the response
        ).choices[0].text

        return response

    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        # Get user prompt from the request's JSON data
        user_prompt = request.json['prompt']

        # Generate response using OpenAI GPT-3 API
        response = generate_response(user_prompt)

        # Performing sentiment analysis on the generated response
        sentiment_score = sentiment_analyzer.polarity_scores(response)
        sentiment = "positive" if sentiment_score['compound'] > 0 else "negative"

        # This Section helps to Store conversation and response as vectors in PostgreSQL using pgvector From Python Script
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                sql.SQL("INSERT INTO conversations (user_prompt, generated_response, sentiment) VALUES (%s, %s, %s) RETURNING id"),
                (user_prompt, response, sentiment)
            )
            conversation_id = cur.fetchone()[0]
            conn.commit()

        return jsonify({"response": response, "sentiment": sentiment, "conversation_id": conversation_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_similar_conversations', methods=['GET'])
def get_similar_conversations():
    try:
        # Get a conversation ID from the request parameters
        conversation_id = request.args.get('conversation_id', type=int)

        # Retrieve the user_prompt for the provided conversation ID
        with conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                sql.SQL("SELECT user_prompt FROM conversations WHERE id = %s"),
                (conversation_id,)
            )
            user_prompt = cur.fetchone()['user_prompt']

            # Perform a similarity search using pgvector
            cur.execute(
                sql.SQL("SELECT id, generated_response, sentiment, similarity(user_prompt, %s) AS sim FROM conversations WHERE user_prompt <% %s ORDER BY sim DESC"),
                (user_prompt, user_prompt)
            )
            similar_conversations = cur.fetchall()
            conn.commit()

        return jsonify(similar_conversations)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()


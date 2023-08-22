# Langchain-flask-app
My Api Key got expired so i m not getting the responses from AI model So I will not be able to provide Loom Video
Please Consider this code 
clone this repository and please change Openapi key with your api key, It should Work Fine.

Install Required Python Packages:
    
    pip install Flask openai vaderSentiment psycopg2-binary Flask-Migrate requests


Set Up PostgreSQL:
Open a terminal/command prompt and log in to PostgreSQL using the psql command:
    
    psql -U postgres


Create a new database for your project:
    
    CREATE DATABASE langchain_db;


Exit the PostgreSQL prompt:
    
    \q


Install and Configure pgvector Extension:
Connect to your newly created database using psql:
    
    psql -U postgres -d langchain_db


Inside the PostgreSQL prompt, install the pgvector extension:
    
    CREATE EXTENSION IF NOT EXISTS pgvector;


Create a table to store conversations and a vector column:
    
    CREATE TABLE conversations (
        id SERIAL PRIMARY KEY,
        user_prompt TEXT,
        generated_response TEXT,
        sentiment TEXT
    );

    ALTER TABLE conversations ADD COLUMN user_prompt_vector vector;


Exit the PostgreSQL prompt:
    
    \q

Conducting End-to-End Testing
Ensure your Flask application is running.

    python test_chatbot.py

Credits
This project was developed by Aniket Mandloi. Feel free to contact me for any inquiries or feedback.

Feel free to customize and expand upon this README to include more detailed instructions, screenshots, acknowledgments, and any additional information relevant to your project.

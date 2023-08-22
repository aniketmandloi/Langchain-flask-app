import requests

# Set the URL of your Flask application
url = "http://127.0.0.1:5000/get_response"

# Sample user prompts for testing
user_prompts = [
    "Tell me a joke",
    "What's the weather like today?",
    "How does photosynthesis work?",
    "Write a Python program to calculate the factorial of a number",
    "Congratulations! You won $10,000. Please share your mobile number"
]

for prompt in user_prompts:
    # Create a JSON payload with the user prompt
    payload = {"prompt": prompt}

    # Send a POST request to the Flask application's API
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("User Prompt:", prompt)
        print("AI Response:", data["response"])
        print("Sentiment:", data["sentiment"])
        print("-" * 30)
    else:
        print("Error:", response.text)

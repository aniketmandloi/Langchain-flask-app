#Below is the code for Week 3 Assignment.
#And I have also attached the loom video for demo of my project but in generated response my limit is exceeded for openai api call so please change the key to you api key then it should work well. THANK YOU!

from flask import Flask, render_template, request, jsonify
import openai

app = Flask(__name__)

# Set up your OpenAI API key
openai.api_key = "YOUR_OPEN_API_KEY"

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

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()

import openai
from flask import Flask, request, render_template

# Initialize the OpenAI API with your API key
openai.api_key = "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"

# Initialize the Flask app
app = Flask(__name__)
chat_history = []

# Define a route for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get the user's message from the request body
    message = request.form['message']

    # Call the OpenAI API to get the chatbot's response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{message}. output response with a pirate accent:",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract the chatbot's response from the API response
    bot_message = response.choices[0].text.strip()

    # Add the chat to the chat history
    chat_history.append({'input': message, 'output': bot_message})

    # Return the chatbot's response to the user
    return bot_message

# Define a route for the home page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the user's message from the request form
        message = request.form['message']

        # Call the OpenAI API to get the chatbot's response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{message}:",
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the chatbot's response from the API response
        bot_message = response.choices[0].text.strip()

        # Add the chat to the chat history
        chat_history.append({'input': message, 'output': bot_message})

        # Render the home page template with the chat history
        return render_template('index.html', chat_history=chat_history)

    else:
        # Render the home page template with the initial chat history
        return render_template('index.html', chat_history=chat_history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

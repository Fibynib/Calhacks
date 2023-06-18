from flask import Flask
from flask import request

import openai
openai.api_key = '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'

app = Flask("flask server")


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Process the file and generate questions
    text = file.read().decode('utf-8')  # Read the file content as text

    # Generate questions using the OpenAI API
    response = openai.Completion.create(
        engine='GPT-4',  # Choose the GPT-3.5 model or GPT-4 model you want to use
        prompt=text,
        max_tokens=50,  # Adjust the number of tokens based on your desired question length
        n=5,  # Adjust the number of questions you want to generate
        stop=None,  # Add stop conditions if needed
    )

    # Extract the generated questions from the API response
    questions = [choice['text'].strip() for choice in response['choices']]

    # Return the generated questions as a JSON response
    return {'questions': questions}



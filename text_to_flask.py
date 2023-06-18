import os

from flask import Flask, render_template, request

os.environ["OPENAI_API_KEY"] = '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'
import openai
from langchain.chat_models import ChatOpenAI


def get_completion(prompt, model="gpt-4"):
    response = openai.ChatCompletion.create(
        model = model,
        messages = prompt,
        temperature = 0.7
    )
    return response.choices[0].message["content"]

class Riddler():
    answer = ""
    answer_text = ""
    response_list = ""
    question = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('text_to_flask.html')

@app.route('/quiz', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # Save the file or process it as needed
        print(type(file))
        file.save(file.filename)

        with open(file.filename, mode='r') as f:
            all_of_it = f.read()
        
    Riddler.question.append({"role": "system", "content": "You are a quiz bot that gives people 4-option multiple choice questions based solely on the provided text.\
                             You will generate a new multiple-choice question that encourages deep understanding and critical thinking about the main ideas, themes, and details. The question should be challenging and require a thorough understanding of the text to answer correctly.\
                             The question should be followed by four diverse and insightful options. Each option should be plausible and thought-provoking, but only one option should be the correct answer. The options should not be too obvious or too obscure.\
                             The question and options must be formatted as a json object formatted as {question: 'Your question string goes here', choice1: 'First option string goes here', choice2: 'Second option string goes here', choice3: 'Third option string goes here', choice4: 'Fourth option string goes here', answer:'An integer in {1,2,3,4} that indicates the correct answer choice'}.\
                             Please note that the word 'Question' should not be included in the output. The output should start directly with the question text. Do not to repeat questions.\
                             Please ensure that the question, options, and answer adhere to these guidelines and are grammatically correct, clear, and concise."})

    if request.method == "POST":
        Riddler.question.append({"role": "user", "content": "You can make this first question easy, like 3rd grade level, like read off the first line of the book."})
        Riddler.question.append({"role": "user", "content": "This is the provided text you will test the user on\n" + all_of_it})

    response = get_completion(Riddler.question)
    Riddler.response_list = eval(response)
    print(Riddler.response_list)
    Riddler.answer = Riddler.response_list["answer"]

    Riddler.question.append({"role": "assistant", "content": response})
    Riddler.answer_text = Riddler.response_list['choice' + str(Riddler.answer).strip()]

    print(str(response))
    print()

    
    print(Riddler.question)
    print()

    return render_template(
        "quiz.html",
        question=Riddler.response_list["question"],
        option1=Riddler.response_list["choice1"],
        option2=Riddler.response_list["choice2"],
        option3=Riddler.response_list["choice3"],
        option4=Riddler.response_list["choice4"]
    )

@app.route('/answer', methods=['POST'])
def show_results():
    choice = request.form['question1']
    Riddler.question.append({"role": "user", "content": "I answered:\n" + Riddler.response_list["choice"+choice] + "\n"})
    prompt = [Riddler.question[-2], {"role": "system", "content": "You are a bot to evaluate the user's answers to exam questions. Do not be polite and do not apologize. Have fun with belittling me, but explain the correct answer and why. The question/answer pair is formatted as a json object formatted as {question: 'Your question string goes here', choice1: 'First option string goes here', choice2: 'Second option string goes here', choice3: 'Third option string goes here', choice4: 'Fourth option string goes here', answer:'An integer in {1,2,3,4} that indicates the correct answer choice'}"}, Riddler.question[-1], {"role": "user", "content": "If I was wrong, can you explain what the right answer to the most recent question was? If I was right, congratulate me."}]

    if int(choice) == Riddler.answer:
        Riddler.question.append({"role": "user", "content": "Because I got it right, make the next question a lot more challenging by making it more creative and complex. You might try a question that is unanswerable by surface-level knowledge or simple recall to reinforce learning of the rules. Make sure your question follows the rules."})
    else:
        Riddler.question.append({"role": "user", "content": "Because I got it wrong, make the next question a lot easier by making it less complex and a little more surface-level."})

    response = get_completion(prompt)
    print("history starting")
    print(Riddler.question)

    return render_template(
        "results.html",
        response = response
    )

if __name__ == '__main__':
    app.run()

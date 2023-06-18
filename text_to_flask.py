import os

from flask import Flask, render_template, request

os.environ["OPENAI_API_KEY"] = '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'
from llama_index import (  # LLMPredictor,; ServiceContext
    SimpleDirectoryReader, VectorStoreIndex)

char_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

class Riddler():
    answer = ""
    answer_text = ""
    history = ""

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
        file.save("input/"+file.filename)

        documents = SimpleDirectoryReader("input").load_data()

        # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="text-davinci-003"))
        # service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

        index = VectorStoreIndex.from_documents(documents) #, service_context=service_context)

        global query_engine
        
        query_engine = index.as_query_engine()

    question = Riddler.history + \
               "Based on the provided text, generate a new multiple-choice question that encourages deep understanding and critical thinking about the main ideas, themes, and details. The question should be challenging and require a thorough understanding of the text to answer correctly. \
                The question should be followed by four diverse and insightful options. Each option should be plausible and thought-provoking, but only one option should be the correct answer. The options should not be too obvious or too obscure. \
                The question and options should be formatted as follows: 'Question~option1~option2~option3~option4~answer'. The 'answer' should be a single lowercase letter that corresponds to the correct option: 'a' for the first option, 'b' for the second option, 'c' for the third option, and 'd' for the fourth option. \
                Please note that the word 'Question' should not be included in the output. The output should start directly with the question text. + \
                Try not to repeat questions. + \
                Please ensure that the question, options, and answer adhere to these guidelines and are grammatically correct, clear, and concise."

    prompt = question

    response = query_engine.query(prompt)
    response_list = str(response).split("~")
    print(response_list)
    Riddler.answer = response_list[5][0]

    Riddler.answer_text = response_list[char_to_num[Riddler.answer]]
    Riddler.history = Riddler.history + \
           "You asked:" + str(response) + "\n"

    print(str(response))
    print()

    
    #print(history)
    print()

    return render_template(
        "quiz.html",
        question=response_list[0],
        option1=response_list[1],
        option2=response_list[2],
        option3=response_list[3],
        option4=response_list[4]
    )

@app.route('/answer', methods=['POST'])
def show_results():
    choice = request.form['question1']
    Riddler.history = Riddler.history + \
                      "I answered:\n" + Riddler.answer_text + "\n"
    
    if choice == str(Riddler.answer):
        response = "You got it right! Good job! The answer is " + Riddler.answer_text
        Riddler.history = Riddler.history + \
                          "Because I got it right, make the next question a lot more challenging by making it more creative and complex. You might try a question that is unanswerable by surface-level knowledge or simple recall to reinforce learning of the rules. Make sure your question follows the rules."
    else:
        prompt = Riddler.history + \
                 "Tell me I was wrong. I do not know the answer. Can you explain what the right answer was? Where in the text was this stated?"
        Riddler.history = Riddler.history + \
                          "Because I got it wrong, make the next question a lot easier by making it less complex and a little more surface-level."
        response = query_engine.query(prompt)

    print("history starting")
    print(Riddler.history)

    return render_template(
        "results.html",
        response = response
    )

if __name__ == '__main__':
    app.run()

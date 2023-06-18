import os

from flask import Flask, render_template, request

os.environ["OPENAI_API_KEY"] = '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'

from llama_index import (  # LLMPredictor,; ServiceContext
    SimpleDirectoryReader, VectorStoreIndex)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('text_to_flask.html')

@app.route('/quiz', methods=['POST'])
def upload():
    file = request.files['file']
    # Save the file or process it as needed
    print(type(file))
    file.save("input/"+file.filename)

    documents = SimpleDirectoryReader("input").load_data()

    # llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="text-davinci-003"))
    # service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    index = VectorStoreIndex.from_documents(documents) #, service_context=service_context)


    query_engine = index.as_query_engine()

    question = "Give a 4-choice multiple choice question without the answer about this topic in the following format: Question,option1,option2,option3,option4"

    prompt = question

    response = query_engine.query(prompt)
    response_list = str(response).split(",")
    print(response_list)
    # history = history + \
    #        "They asked " + question + "\n" + \
    #        "You responded with " + str(response) + "\n"

    print(str(response))
    print()

    print("history starting")
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

if __name__ == '__main__':
    app.run()

import os

from flask import Flask, render_template, request

os.environ["OPENAI_API_KEY"] = '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'

from llama_index import (  # LLMPredictor,; ServiceContext
    SimpleDirectoryReader, VectorStoreIndex)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('text_to_flask.html')

@app.route('/upload', methods=['POST'])
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

    question = "Give a 4-choice multiple choice question without the answer about this topic"

    prompt = question

    response = query_engine.query(prompt)

    # history = history + \
    #        "They asked " + question + "\n" + \
    #        "You responded with " + str(response) + "\n"

    print(response.response_txt)
    print()

    print("history starting")
    #print(history)
    print()

    return response.response_txt

if __name__ == '__main__':
    app.run()

import os

os.environ["OPENAI_API_KEY"] = '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'

from llama_index import (  # LLMPredictor,; ServiceContext
    SimpleDirectoryReader, VectorStoreIndex)

# from langchain.chat_models import ChatOpenAI

documents = SimpleDirectoryReader('hi.txt').load_data()

# llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="text-davinci-003"))
# service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

index = VectorStoreIndex.from_documents(documents) #, service_context=service_context)

query_engine = index.as_query_engine()
history = ""

while(1):
    question = input("hi\n")

    prompt = history + question

    response = query_engine.query(prompt)

    history = history + \
              "They asked " + question + "\n" + \
              "You responded with " + str(response) + "\n"

    print(response)
    print()

    print("history starting")
    print(history)
    print()

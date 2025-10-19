from flask import Flask, render_template, jsonify, request
from src.helper import *
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY=os.environ.get('PINECONE_API_KEY')

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

embeddings = get_ollama_embeddings()

index_name = "chanakya"

# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
from langchain_community.llms import Ollama
llm = Ollama(model="deepseek-r1:1.5b", temperature=0.4)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# The rest of your code for creating the chain remains the same!
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    # print(input)
    response = rag_chain.invoke({"input": msg})
    # print("Response : ", response["answer"])
    final_answer = filter_response(msg, response["answer"])
    cleaned_answer = re.sub(r"<think>.*?</think>", "", final_answer, flags=re.DOTALL).strip()

    return str(cleaned_answer)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    """Handles incoming WhatsApp messages from Twilio"""
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")
    try:
        # Generate chatbot response using the same RAG chain
        response = rag_chain.invoke({"input": incoming_msg})
        final_answer = filter_response(incoming_msg, response["answer"])
        cleaned_answer = re.sub(r"<think>.*?</think>", "", final_answer, flags=re.DOTALL).strip()
    except Exception as e:
        print("Error:", e)
        cleaned_answer = "Sorry, something went wrong while processing your message."

    # Send response back to WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(cleaned_answer)
    return str(twilio_resp)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)
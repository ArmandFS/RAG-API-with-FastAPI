from fastapi import FastAPI
import chromadb
import ollama
import os
import logging

#what is host.docker.internal?
#it is a special hostname that lets containers access services on host machine

#implement logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    )

MODEL_NAME = os.getenv("OLLAMA_MODEL", "tinyllama")
logging.info(f"Using Model: {MODEL_NAME}")
#this logger will be used to log events in the app + timestamps
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")


#also add request logging
app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")
#have to rechange this from docker code to host code for testing.
#ollama_client = ollama.Client(host="http://host.docker.internal:11434")
ollama_client = ollama.Client(host=OLLAMA_HOST)



#addick mock llm mode for testing.
@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"] [0][0] if results["documents"] else ""
    logging.info(f"/query asked: {q}")

    use_mock = os.getenv("USE_MOCK_LLM", "0") == "1"

    #if else statement for mock llm mode
    if use_mock:
        return {"answer": context}
    else:
        #use real LLM (in production mode)
#what mock does is that it checks USE_MOCK_LLM env variable. If set to 1, returns retrieved context directly
#it makes it deterministic.

        answer = ollama.generate(
            model="tinyllama",
            prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
        )
        return {"answer": answer["response"]}

@app.post("/add")
def add_knowledge(text: str):
    """add new content to the knowledge base dynamically"""
    try:

        import uuid
        doc_id = str(uuid.uuid4())
        # add the text to chroma collection
        collection.add(documents=[text], ids=[doc_id])
        logging.info(f"/add received new text (id will be generated)")

        return {
            "status": "success",
            "message": "content added to knowledge base successfully",
            "id": doc_id    
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/health")
def health():
    return {"status": "ok"}

#this was the last commit and code i wrote before going to bed
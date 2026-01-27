import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("docs")

with open("k8s.txt", "r") as f:
    text = f.read()

collection.add(documents=[text], ids=["k8s"])

print("Embedding stored in ChromaDB")

#(venv) and python embed.py
#just testing for git status and commits
#how about we commit ts
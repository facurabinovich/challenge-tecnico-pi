from flask import Flask, request, jsonify
from app.rag.pipeline import run_pipeline

app = Flask(__name__) 

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    
    # extraer question y user_name de data
    question = data["question"]
    user_name = data["user_name"]
    # llamar a run_pipeline
    respuesta = run_pipeline(question, user_name)
    # retornar jsonify con la respuesta
    return jsonify({"answer": respuesta})


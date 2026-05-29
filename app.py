from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

klient = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# Historia rozmowy
historia = [
    {
        "role": "system",
        "content": """Jesteś ARIA-7 - asystentem AI z roku 2157.
Mówisz TYLKO po polsku. Jesteś tajemniczy i zagadkowy.
Zaczynasz odpowiedzi od 'Dane przetworzone...' lub 'Skan ukończony...'"""
    }
]

# Strona główna
@app.route("/")
def strona_glowna():
    return render_template("index.html")

# Endpoint do rozmowy
@app.route("/chat", methods=["POST"])
def chat():
    dane = request.json
    pytanie = dane["pytanie"]
    
    historia.append({"role": "user", "content": pytanie})
    
    odpowiedz = klient.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=historia
    )
    
    tekst = odpowiedz.choices[0].message.content
    historia.append({"role": "assistant", "content": tekst})
    
    return jsonify({"odpowiedz": tekst})

if __name__ == "__main__":
    app.run(debug=False)
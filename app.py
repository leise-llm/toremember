from flask import Flask, render_template, request
import openai
from dotenv import load_dotenv
import os

# Lade die Umgebungsvariablen aus der app.env-Datei
load_dotenv('app.env')

app = Flask(__name__)

# Setze den OpenAI API-Schlüssel
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Stichworte aus dem Formular auslesen
        keywords = [request.form.get(f'keyword{i}') for i in range(1, 6)]
        prompt = (
            "Du bist ein freundlicher Zuhörer. Erstelle einen kurzen Erinnerungstext "
            "in Ich-Form, basierend auf folgenden Stichworten: "
            + ", ".join(keywords) +
            ". Nutze persönliche Sprache ('Ich', 'Wir', 'Du') und beschreibe eine Szene."
        )

        # Anfrage an OpenAI senden
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein freundlicher Zuhörer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        reminder_text = response['choices'][0]['message']['content'].strip()
        return render_template('index.html', reminder_text=reminder_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

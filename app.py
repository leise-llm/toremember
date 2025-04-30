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
        land = request.form['land']
        urlaubsart = request.form['urlaubsart']
        region = request.form['region']
        
        # Frage an das Sprachmodell
        prompt = f"Beschreibe einen Urlaubstag in {region}, {land} mit der Urlaubsart {urlaubsart}."
        response = openai.Completion.create(
            model="gpt-4",
            prompt=prompt,
            max_tokens=150
        )
        
        beschreibung = response.choices[0].text.strip()
        return render_template('index.html', beschreibung=beschreibung)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
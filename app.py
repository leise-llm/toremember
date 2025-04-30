from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Setze den OpenAI API-Schlüssel aus den Umgebungsvariablen
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY ist nicht gesetzt. Bitte überprüfe deine Azure-Konfiguration.")
openai.api_key = api_key

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Stichworte aus dem Formular auslesen und Eingaben überprüfen
        keywords = [request.form.get(f'keyword{i}', '').strip() for i in range(1, 6)]
        keywords = [kw for kw in keywords if kw]  # Leere Stichworte entfernen

        if not keywords:
            reminder_text = "Bitte geben Sie mindestens ein Stichwort ein."
        else:
            prompt = (
                "Du bist ein freundlicher Zuhörer. Erstelle einen kurzen Erinnerungstext "
                "in Ich-Form, basierend auf folgenden Stichworten: "
                + ", ".join(keywords) +
                ". Nutze persönliche Sprache ('Ich', 'Wir', 'Du') und beschreibe eine Szene."
            )

            try:
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
            except Exception as e:
                reminder_text = f"Es gab ein Problem bei der Anfrage an OpenAI: {str(e)}"

        return render_template('index.html', reminder_text=reminder_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Securely get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/openai_assistant", methods=['POST', 'GET'])
def openai_assistant():
    user_speech = request.form.get('SpeechResult') or request.args.get('SpeechResult')

    if not user_speech:
        return jsonify(reply="לא התקבל קלט."), 200

    try:
        assistant_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "אתה עוזר אישי ידידותי שעונה בעברית."},
                {"role": "user", "content": user_speech},
            ],
            timeout=10
        )
        reply = assistant_response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"שגיאה: {str(e)}"

 	response = jsonify(reply=reply)  # Make sure this line uses spaces
	response.headers['Content-Type'] = 'application/json; charset=utf-8'

    return response, 200

if __name__ == "__main__":
    app.run(debug=True)

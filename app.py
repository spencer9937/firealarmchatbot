from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return jsonify({"message": "Send a POST request with a message to get a response."})

    # DEBUG: Print incoming request data to Render logs for troubleshooting
    print("Received raw request data:", request.data)
    print("Received parsed JSON:", request.get_json())

    try:
        data = request.get_json()
        
        # Ensure 'message' is present in the request body
        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"]

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a fire alarm technician assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error:", str(e))  # Log the error
        return jsonify({"error": str(e)}), 500

# Ensure Flask runs on the correct port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

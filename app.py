from flask import Flask, render_template, request, jsonify

from predictor import analyze_message
from moderation import process_violation, is_user_blocked
from database import initialize_database, create_user

app = Flask(__name__)

# Initialize the database when the server starts
initialize_database()


@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    username = data["username"].strip()

    message = data["message"].strip()

    if username == "":
        return jsonify({
            "status": "error",
            "message": "Username is required."
        })

    if message == "":
        return jsonify({
            "status": "error",
            "message": "Message cannot be empty."
        })

    create_user(username)

    blocked, remaining = is_user_blocked(username)

    if blocked:

        return jsonify({

            "status": "blocked",

            "message": "You are temporarily blocked.",

            "remaining_time": str(remaining).split(".")[0]

        })

    result = analyze_message(message)

    if result["safe"]:

        return jsonify({

            "status": "safe",

            "message": "Message is safe.",

            "severity": result["severity"],

            "confidence": result["confidence"]

        })

    violation = process_violation(username)

    categories = [

        item["category"]

        for item in result["categories"]

    ]

    return jsonify({

        "status": "hate",

        "message": "Hate speech detected.",

        "severity": result["severity"],

        "confidence": result["confidence"],

        "categories": categories,

        "violations": violation["violations"],

        "remaining": 3 - violation["violations"]

    })

if __name__ == "__main__":
    app.run(debug=True)
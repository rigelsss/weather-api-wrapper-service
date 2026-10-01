from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    return jsonify({
        "city": city,
        "temperature": "25°C",
        "condition": "Sunny",
        "Source": "Hardcoded"
    })
    
    
if __name__ == "__main__":
    app.run(debug=True)
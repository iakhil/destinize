from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

@app.route('/planner', methods=['POST'])
def planner():
    try:
        data = request.json
        budget = data.get('budget')
        days = data.get('days')
        travel_type = data.get('travel_type')
        destination = data.get('destination')
        source = data.get('source')

        if not all([budget, days, travel_type, destination]):
            return jsonify({"error": "Missing required fields."}), 400

        # Create the prompt for OpenAI API
        prompt = (
            f"You are an expert tour guide. Plan a {days}-day trip from {source} to {destination} with a budget of ${budget}."
            f"The trip should focus on '{travel_type}' experiences. "
            "Provide the top 5 must-visit destinations, recommended modes of transport (the one that's most feasible. e.g. if travelling from Chicago to NYC, train is an option but not feasible. SUGGEST FLIGHT AS THE MODE OF TRANSPORT FOR TRAVELS WHERE THE DISTANCE BETWEEN THE SOURCE AND DESTINATION IS MORE THAN 300 MILES), and a cost breakdown. Keep your responses succinct and under 5 sentences. Do not use asterisks."
        )

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
            ],
            max_tokens=500
        )

        plan = response.choices[0].message.content

        return jsonify({"plan": plan})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

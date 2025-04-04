from flask import Flask, request, jsonify
import openai

import os
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    data = request.json
    destination = data.get('destination')
    days = data.get('days')
    budget = data.get('budget')
    preferences = data.get('preferences')

    prompt = f"""
    Plan a {days}-day trip to {destination} with a budget of ${budget}.
    The traveler prefers: {preferences}.
    Include suggestions for activities, meals, and ideal timing for each day.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful travel planner."},
            {"role": "user", "content": prompt}
        ]
    )

    itinerary = response['choices'][0]['message']['content']
    return jsonify({'itinerary': itinerary})

if __name__ == '__main__':
    app.run(debug=True)
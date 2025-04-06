import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
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

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful travel planner."},
                {"role": "user", "content": prompt}
            ]
        )

        itinerary = response.choices[0].message.content
        return jsonify({'itinerary': itinerary})
    except Exception as e:
        # Log the error for debugging; this will appear in Render's logs
        print("Error in generate_itinerary:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=True)

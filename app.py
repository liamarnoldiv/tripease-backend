import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

# Set your API key using the environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/generate-itinerary', methods=['POST', 'OPTIONS'])
def generate_itinerary():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
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

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful travel planner."},
                {"role": "user", "content": prompt}
            ]
        )

        itinerary = response['choices'][0]['message']['content']
        return jsonify({'itinerary': itinerary})
    except Exception as e:
        import traceback
        print("Error in generate_itinerary:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port, debug=True)


from riva_api import RivaAPI
riva_api = RivaAPI(api_key='api_key', region='riva_region')
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


# Function to handle incoming customer queries
def handle_customer_query(query_text):

    response = riva_api.query(query_text)

    
    intent = response.get('intent')
    entities = response.get('entities')

    if intent == 'order_status':
        # Fetch order status from backend 
        order_id = entities['order_id']
        order_status = fetch_order_status(order_id)
        return f"Your order {order_id} is currently {order_status}."
    elif intent == 'product_recommendation':
        # Get personalized recommendations based on user ID
        user_id = entities['user_id']
        recommendations = get_personalized_recommendations(user_id)
        return f"Based on your preferences, we recommend: {', '.join(recommendations)}."
    else:
        return "I'm sorry, I didn't quite understand that. Can you please rephrase your question?"


def fetch_order_status(order_id):
    # backend API call
    url = f"https://websazco.com/orders/{order_id}"
    headers = {'Authorization': 'auth_token'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            order_data = response.json()
            return order_data['status']
        else:
            return "Status not available"
    except requests.exceptions.RequestException as e:
        return f"Error fetching order status: {str(e)}"

# Function to get personalized recommendations based on user ID
def get_personalized_recommendations(user_id):
   
    url = f"https://websazco.com/recommendations/{user_id}"
    headers = {'Authorization': 'auth_token'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            recommendations = response.json()['recommendations']
            return recommendations
        else:
            return [f"Error fetching recommendations: {str(e)}"]

# Define endpoint to handle incoming queries
@app.route('/query', methods=['POST'])
def process_query():
    data = request.get_json()
    query_text = data['query']

    response = handle_customer_query(query_text)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
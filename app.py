from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import joblib
import numpy as np
from flask_cors import CORS
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load the model
model = joblib.load('water_purity_model.pkl')

# MongoDB connection string
MONGO_URI = os.getenv('MONGO_URI')

# Connect to MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['WaterC']
    water_features_collection = db['waterFeatures']
    archive_collection = db['archive']
    users_collection = db['users']
    logging.info("Connected to MongoDB successfully")
except Exception as e:
    logging.error(f"Failed to connect to MongoDB: {e}")
    raise

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        if users_collection.find_one({'email': email}):
            return jsonify({'error': 'Email already registered'}), 400

        hashed_password = generate_password_hash(password)
        user_id = users_collection.insert_one({
            'email': email,
            'password': hashed_password
        }).inserted_id

        return jsonify({'message': 'User registered successfully', 'user_id': str(user_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        user = users_collection.find_one({'email': email})
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token(identity=str(user['_id']))
            return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid email or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/waterFeatures', methods=['GET'])
# @jwt_required()
def get_data():
    try:
        data = list(water_features_collection.find({}, {'_id': 0}))  # Exclude the '_id' field
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/archive', methods=['GET'])
# @jwt_required()
def get_archive_data():
    try:
        data = list(archive_collection.find({}, {'_id': 0}))  # Exclude the '_id' field
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/archive', methods=['POST'])
# @jwt_required()  # Uncomment if JWT authentication is needed
def post_data():
    try:
        print(request.json)
        data = request.json
        required_fields = ['Ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity', 'Quality']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        archive_collection.insert_one(data)
        return jsonify({'message': 'Data inserted successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/archive/<id>', methods=['DELETE'])
# @jwt_required()
def delete_archive_data(id):
    try:
        if not ObjectId.is_valid(id):
            return jsonify({'error': 'Invalid ID format'}), 400
        
        result = archive_collection.delete_one({'_id': ObjectId(id)})
        
        if result.deleted_count == 0:
            return jsonify({'error': 'Document not found'}), 404
        
        return jsonify({'message': 'Document deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        features = np.array(list(data.values())).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({'prediction': prediction.tolist()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

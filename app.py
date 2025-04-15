from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import logging
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Gemini - use environment variable for API key
from google import genai
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai_client = genai.Client(api_key=gemini_api_key)

# Groq models - use environment variable for API key
from groq import Groq
groq_api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_api_key)

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
CORS(app)  # Enable CORS for all routes

def get_prompt_from_request():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return None, jsonify({'error': 'Missing "prompt" in request body'}), 400
    return data['prompt'], None, None

# Routes
@app.route('/')
def index():
    # Serve the HTML directly from Flask
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "online",
        "endpoints": {
            "gemini": "/gemini",
            "llama3": "/llama3"
        },
        "api_keys": {
            "gemini": bool(gemini_api_key),
            "groq": bool(groq_api_key)
        }
    })

@app.route('/gemini', methods=['POST'])
def gemini_endpoint():
    try:
        if not gemini_api_key:
            return jsonify({"error": "Gemini API key not configured in environment variables"}), 500
            
        prompt, error_response, status = get_prompt_from_request()
        if error_response:
            return error_response, status
        
        # Record response time
        start_time = time.time()
        response = genai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[prompt]
        )
        elapsed_time = time.time() - start_time
        
        return jsonify({
            "model": "gemini-2.0-flash",
            "response": response.text,
            "time_taken": f"{elapsed_time:.2f} seconds"
        })
    
    except Exception as e:
        logger.error(f"Error in Gemini endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/llama3', methods=['POST'])
def llama3_endpoint():
    try:
        if not groq_api_key:
            return jsonify({"error": "Groq API key not configured in environment variables"}), 500
            
        prompt, error_response, status = get_prompt_from_request()
        if error_response:
            return error_response, status
        
        # Record response time
        start_time = time.time()
        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=32768,
            top_p=1,
            stop=None,
        )
        elapsed_time = time.time() - start_time
        
        return jsonify({
            "model": "llama-3.3-70b-versatile",
            "response": completion.choices[0].message.content,
            "time_taken": f"{elapsed_time:.2f} seconds"
        })
    
    except Exception as e:
        logger.error(f"Error in LLaMA 3 endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)

# Multi-AI Model Flask API

This Flask API integrates multiple AI models including Google Gemini and Groq's LLaMA 3.

## Features

- Flask API with CORS support
- Endpoints for multiple AI models
- JSON-formatted responses
- Environment variable configuration for API keys
- Error handling for API calls

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file based on `.env.example` with your actual API keys
4. Run the application:
   ```
   python app.py
   ```

## Environment Variables

Create a `.env` file with the following:

```
GEMINI_API_KEY=your-gemini-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

## API Endpoints

### Status Check
```
GET /
```

### Google Gemini
```
POST /gemini
Content-Type: application/json

{
  "prompt": "Your prompt text here"
}
```

### Groq LLaMA 3
```
POST /llama3
Content-Type: application/json

{
  "prompt": "Your prompt text here"
}
```

## Example curl Commands

### Check API Status
```bash
curl http://localhost:5000/
```

### Query Gemini Model
```bash
curl -X POST http://localhost:5000/gemini \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'
```

### Query LLaMA 3 Model
```bash
curl -X POST http://localhost:5000/llama3 \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a short poem about artificial intelligence"}'
```

## Sample Educational Prompts

1. "Explain the difference between supervised and unsupervised learning"
2. "What are the ethical considerations in artificial intelligence?"
3. "Describe how neural networks work"
4. "Explain the concept of backpropagation in machine learning"
5. "What is transfer learning and why is it important?"

## Deployment on Render

### Option 1: Using Blueprint (Automated)

1. Push your code with the `render.yaml` file to a GitHub or GitLab repository
2. Log in to your Render account
3. Go to "Blueprints" in the dashboard
4. Click "New Blueprint Instance"
5. Select your repository
6. Render will automatically detect the `render.yaml` file and create the service
7. Set up your environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GROQ_API_KEY`: Your Groq API key

### Option 2: Manual Setup

If you prefer to set up manually:

1. Push your code to a GitHub or GitLab repository
2. Log in to your Render account
3. Click "New" and select "Web Service"
4. Connect your repository
5. Configure the service:
   - **Name**: ai-models-api (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Add environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GROQ_API_KEY`: Your Groq API key
7. Click "Create Web Service"

## Accessing Your API

Once deployed, your API will be available at:
- Web Interface: `https://your-service-name.onrender.com/`
- API Status: `https://your-service-name.onrender.com/api/status`
- Gemini Endpoint: `https://your-service-name.onrender.com/gemini`
- LLaMA3 Endpoint: `https://your-service-name.onrender.com/llama3`

## Making API Requests

```python
import requests

API_URL = "https://your-service-name.onrender.com"

# Query Gemini
response = requests.post(
    f"{API_URL}/gemini",
    json={"prompt": "Explain quantum computing"}
)
print(response.json()["response"])

# Query LLaMA 3
response = requests.post(
    f"{API_URL}/llama3",
    json={"prompt": "Write a poem about AI"}
)
print(response.json()["response"])
```

## Security Notes

- Never commit your .env file with actual API keys
- Set up environment variables in Render's dashboard
- Use HTTPS for production deployments
- Consider implementing rate limiting for production use

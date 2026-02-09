from flask import Flask, request, Response
import orjson
import logging
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import requests
import os

from .core.analyzer import CommandAnalyzer
from .core.validator import TargetValidator

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KAOS_BRAIN")

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
APP_HOST = os.getenv("KAOS_HOST", "127.0.0.1")
APP_PORT = int(os.getenv("KAOS_PORT", "5000"))

def json_response(data, status=200):
    return Response(
        orjson.dumps(data),
        status=status,
        mimetype="application/json"
    )

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2), retry=retry_if_exception_type(requests.exceptions.ConnectionError))
def query_ollama(prompt: str):
    """Queries the LLM with retry logic via Tenacity."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=10)
    response.raise_for_status()
    return response.json().get("response", "")

@app.route('/api/v1/health', methods=['GET'])
def health():
    return json_response({"status": "healthy", "mode": "enterprise-hybrid"})

@app.route('/api/v1/analyze', methods=['POST'])
def analyze():
    try:
        raw_data = request.get_data()
        data = orjson.loads(raw_data)
        command_input = data.get('command', '')

        # 1. Scope Validation
        valid_target, msg = TargetValidator.validate_target(command_input)
        if not valid_target:
             return json_response({"error": msg}, status=403)

        # 2. Hybrid Engine Analysis (Fast-Path)
        analysis = CommandAnalyzer.analyze(command_input)
        
        response_payload = {
            "llm_layer": {
                "command": command_input,
                "reasoning": analysis["reasoning"],
                "tool_type": analysis["tool_type"],
                "risk": analysis["risk"]
            }
        }

        # 3. LLM Augmentation (if not simple conversation)
        if analysis["tool_type"] not in ["conversation", "system"] and analysis["allowed"]:
            try:
                llm_reasoning = query_ollama(f"Explain security impact of: {command_input}")
                response_payload["llm_layer"]["reasoning"] += f" | LLM Insight: {llm_reasoning[:100]}..."
            except Exception as e:
                logger.error(f"LLM unavailable: {e}")
                response_payload["llm_layer"]["reasoning"] += " | LLM Offline"

        return json_response(response_payload)

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return json_response({"error": "Internal Server Error"}, status=500)

if __name__ == '__main__':
    app.run(host=APP_HOST, port=APP_PORT)

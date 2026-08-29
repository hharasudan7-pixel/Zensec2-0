"""Standalone Gemini Connectivity & Diagnostics Script

Tests direct connection to Google Gemini API outside of FastAPI to verify:
1. Environment configuration and API Key detection
2. Model availability (`gemini-3.6-flash`)
3. Round-trip API latency and response extraction
4. Network connectivity, SSL certificates, firewall, or proxy interference
"""
import os
import sys
import time
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("gemini-diagnostics")

# Load backend/.env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    logger.error("GOOGLE_API_KEY is not set in environment or .env file!")
    sys.exit(1)

masked_key = api_key[:6] + "..." + api_key[-4:] if len(api_key) > 10 else "***"
logger.info("Using GOOGLE_API_KEY: %s (length=%d)", masked_key, len(api_key))

import google.generativeai as genai

genai.configure(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"
SYSTEM_INSTRUCTION = """You are ZentraSec's AI Incident Copilot, a SOC (Security Operations Center) 
assistant. Keep responses concise (3-5 sentences) and professional."""

logger.info("Initializing GenerativeModel(%s)...", MODEL_NAME)
model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_INSTRUCTION,
)

test_prompt = "Explain in 2 sentences what a brute force SSH attack is."
logger.info("Sending test generate_content request: %r", test_prompt)

t_start = time.perf_counter()
try:
    response = model.generate_content(test_prompt)
    elapsed = time.perf_counter() - t_start
    logger.info("Successfully received response in %.2fs!", elapsed)
    logger.info("Raw response object type: %s", type(response).__name__)
    if hasattr(response, "text") and response.text:
        logger.info("Response Text:\n%s", response.text.strip())
    else:
        logger.warning("Response has no text or is empty. Candidates: %s", getattr(response, "candidates", None))
except Exception as exc:
    elapsed = time.perf_counter() - t_start
    logger.error(
        "GenerateContent FAILED after %.2fs | ExceptionType: %s | Message: %s",
        elapsed,
        type(exc).__name__,
        exc,
        exc_info=True,
    )
    sys.exit(1)

logger.info("Gemini standalone connectivity test PASSED.")

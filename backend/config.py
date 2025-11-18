import os
import dotenv

dotenv.load_dotenv() # Automatically read .env file and set environment variables

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai")  # default: "openai" 或 "hf"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL=os.getenv("OPENAI_MODEL", "gpt-4o-mini")
HF_MODEL=os.getenv("HF_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
#HF_MODEL=os.getenv("HF_MODEL", "unsloth/Meta-Llama-3.1-8B") 

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
BACKEND_LOG_PATH = os.getenv("BACKEND_LOG_PATH", "backend.log")
FRONTEND_LOG_PATH = os.getenv("FRONTEND_LOG_PATH", "frontend.log")



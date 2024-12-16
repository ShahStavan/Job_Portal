import google.generativeai as genai
from pathlib import Path
import json
from typing import Dict, Any
from dotenv import load_dotenv
import os

class Config:
    _instance = None
    _config: Dict[str, Any] = None
    
    # Define class-level attributes
    GOOGLE_API_KEY: str = None
    MODEL_NAME: str = None
    GEMINI_CONFIG: Dict[str, Any] = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    def __init__(self):
        if Config._instance is None:
            load_dotenv()
            # Set class attributes
            Config.GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
            Config.MODEL_NAME = os.getenv('MODEL_NAME')
            if not Config.GOOGLE_API_KEY or not Config.MODEL_NAME:
                raise ValueError("Environment variables for API key or model name are not set.")
            Config._instance = self

    @classmethod
    def _load_config(cls) -> None:
        config_file = Path('llm_metadata.json')
        try:
            if config_file.exists():
                cls._config = json.loads(config_file.read_text())
            else:
                cls._config = cls._create_default_config()
                config_file.write_text(json.dumps(cls._config, indent=2))
            
            genai.configure(api_key=cls.GOOGLE_API_KEY)
            
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            cls._config = cls._create_default_config()

    @classmethod
    def _create_default_config(cls) -> Dict[str, Any]:
        return {
            "version": 1,
            "model_name": cls.MODEL_NAME,
            "api_version": genai.__version__,
            "GEMINI_CONFIG": cls.GEMINI_CONFIG,
        }

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        if cls._config is None:
            cls._load_config()
        return cls._config

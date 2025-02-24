# models.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from google import genai
from google.genai import types
from model_utils import (
    ModelResponse, 
    ModelConfig, 
    ModelType,
    create_audit_prompt, 
    handle_model_error
)
from logging_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()

# Initialize OpenAI clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
llama_client = OpenAI(
    api_key=os.getenv("LLAMA_API_KEY"),
    base_url="https://api.llama-api.com"
)

def get_openai_model_response(audit_md: str, question: str) -> ModelResponse:
    """Queries OpenAI model with improved error handling and response structure."""
    if not openai_client.api_key:
        return handle_model_error(ModelType.OPENAI, ValueError("OPENAI_API_KEY not found"))

    try:
        logger.info("Calling OpenAI model (gpt-4o-mini)...")
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": ModelConfig.get_system_prompt(ModelType.OPENAI)},
                {"role": "user", "content": create_audit_prompt(audit_md, question)}
            ],
            temperature=0.0
        )
        
        total_tokens = completion.usage.total_tokens
        return ModelResponse(
            text=completion.choices[0].message.content,
            total_tokens=total_tokens,
            cost=ModelConfig.calculate_cost(total_tokens, ModelType.OPENAI),
            model_type=ModelType.OPENAI
        )
    except Exception as e:
        return handle_model_error(ModelType.OPENAI, e)

def get_llama_model_response(audit_md: str, question: str) -> ModelResponse:
    """Queries Llama model with standardized error handling and response structure."""
    if not llama_client.api_key:
        return handle_model_error(ModelType.LLAMA, ValueError("LLAMA_API_KEY not found"))

    try:
        logger.info("Calling Llama model (llama3.2-3b)...")
        completion = llama_client.chat.completions.create(
            model="llama3.2-3b",
            messages=[
                {"role": "system", "content": ModelConfig.get_system_prompt(ModelType.LLAMA)},
                {"role": "user", "content": create_audit_prompt(audit_md, question)}
            ]
        )
        
        total_tokens = completion.usage.total_tokens
        return ModelResponse(
            text=completion.choices[0].message.content,
            total_tokens=total_tokens,
            cost=ModelConfig.calculate_cost(total_tokens, ModelType.LLAMA),
            model_type=ModelType.LLAMA
        )
    except Exception as e:
        return handle_model_error(ModelType.LLAMA, e)

def get_gemini_model_response(audit_md: str, question: str) -> ModelResponse:
    """Queries Gemini model with standardized error handling and response structure."""
    if not os.getenv("GEMINI_API_KEY"):
        return handle_model_error(ModelType.GEMINI, ValueError("GEMINI_API_KEY not found"))
    
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        logger.info("Calling Gemini model (gemini-2.0-flash)...")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=ModelConfig.get_system_prompt(ModelType.GEMINI),
            ),
            contents=[create_audit_prompt(audit_md, question)]
        )
        
        total_tokens = (
            response.usage_metadata.total_token_count
            if hasattr(response, 'usage_metadata') and response.usage_metadata
            else 0
        )
        
        return ModelResponse(
            text=response.text.strip(),
            total_tokens=total_tokens,
            cost=ModelConfig.calculate_cost(total_tokens, ModelType.GEMINI),
            model_type=ModelType.GEMINI
        )
    except Exception as e:
        return handle_model_error(ModelType.GEMINI, e)
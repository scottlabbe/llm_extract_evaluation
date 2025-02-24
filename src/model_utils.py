# model_utils.py
from typing import Tuple, Optional, Dict
import logging
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Enum for supported model types"""
    OPENAI = "gpt-4o-mini"
    GEMINI = "gemini-2.0-flash"
    LLAMA = "llama3.2-3b"

@dataclass
class ModelResponse:
    """Standardized response object for all model interactions"""
    text: str
    total_tokens: int
    cost: float
    model_type: ModelType
    error: Optional[str] = None
    
    @property
    def is_error(self) -> bool:
        """Check if response contains an error"""
        return self.error is not None

class ModelConfig:
    """Configuration for model costs and endpoints"""
    COSTS_PER_1K = {
        ModelType.OPENAI: 0.0006,
        ModelType.GEMINI: 0.000001,
        ModelType.LLAMA: 0.0004  # Update with actual cost
    }
    
    @staticmethod
    def calculate_cost(total_tokens: int, model_type: ModelType) -> float:
        """Calculate cost based on token count and model type"""
        cost_per_1k = ModelConfig.COSTS_PER_1K[model_type]
        return (total_tokens / 1000) * cost_per_1k

    @staticmethod
    def get_system_prompt(model_type: ModelType) -> str:
        """Get standardized system prompt for each model"""
        return "You are an audit expert."

def create_audit_prompt(audit_md: str, question: str) -> str:
    """Create standardized prompt for all models"""
    return (f"Below is an audit report:\n\n{audit_md}\n\n"
            f"Based on this report, answer:\n{question}")

def handle_model_error(model_type: ModelType, error: Exception) -> ModelResponse:
    """Standardized error handling for model interactions"""
    error_msg = f"{model_type.value} error: {str(error)}"
    logger.error(error_msg, exc_info=True)
    return ModelResponse(
        text="",
        total_tokens=0,
        cost=0.0,
        model_type=model_type,
        error=error_msg
    )
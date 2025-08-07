import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # Data paths
    data_dir: str = Field(default="data", description="Data directory")
    dataset_path: str = Field(default="data/combined_dataset.json", description="Path to dataset file")
    cases_path: str = Field(default="data/cases.json", description="Path to cases file")
    index_dir: str = Field(default="data/indices", description="Path to indices directory")
    
    # AI/ML settings
    embed_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Embedding model to use"
    )
    llm_api_key: str = Field(default=None, description="LLM API key")
    
    # Timeout settings
    search_timeout: int = Field(default=10, ge=1, le=60, description="Search timeout in seconds")
    coach_timeout: int = Field(default=20, ge=1, le=120, description="Coach timeout in seconds")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Backward compatibility - keep the old config dict for now
config = {
    "data_dir": settings.data_dir,
    "dataset_path": settings.dataset_path,
    "cases_path": settings.cases_path,
    "index_dir": settings.index_dir,
    "embed_model": settings.embed_model,
    "llm_api_key": settings.llm_api_key,
    "search_timeout": settings.search_timeout,
    "coach_timeout": settings.coach_timeout,
} 
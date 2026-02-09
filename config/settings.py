"""
K.A.O.S. Configuration Management
Centralized configuration for all environments
"""

import os
from enum import Enum


class Environment(Enum):
    """Application environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class Config:
    """Base configuration"""
    
    # Application
    APP_NAME = "K.A.O.S."
    APP_VERSION = "0.1.0-dev"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Security
    ENABLE_CORS = False
    ENABLE_HTTPS = True


class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Backend (Brain)
    BRAIN_HOST = "127.0.0.1"
    BRAIN_PORT = 5000
    
    # LLM (Ollama)
    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://localhost:11434/api/generate"
    )
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_TIMEOUT = 10
    OLLAMA_RETRIES = 3
    
    # Frontend (ARM)
    SESSION_LOG = "/opt/arm/session.log"
    SESSION_TIMEOUT = 3600
    
    # Logging
    LOG_LEVEL = "DEBUG"


class StagingConfig(Config):
    """Staging configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Backend (Brain)
    BRAIN_HOST = os.getenv("BRAIN_HOST", "0.0.0.0")
    BRAIN_PORT = os.getenv("BRAIN_PORT", 5000)
    
    # LLM (Ollama)
    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://ollama:11434/api/generate"
    )
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_TIMEOUT = 15
    OLLAMA_RETRIES = 3
    
    # Frontend (ARM)
    SESSION_LOG = "/var/log/kaos/session.log"
    SESSION_TIMEOUT = 7200


class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Backend (Brain)
    BRAIN_HOST = os.getenv("BRAIN_HOST", "0.0.0.0")
    BRAIN_PORT = os.getenv("BRAIN_PORT", 5000)
    
    # LLM (Ollama)
    OLLAMA_URL = os.getenv("OLLAMA_URL")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    OLLAMA_TIMEOUT = 20
    OLLAMA_RETRIES = 5
    
    # Frontend (ARM)
    SESSION_LOG = "/var/log/kaos/session.log"
    SESSION_TIMEOUT = 14400
    
    # Security
    ENABLE_CORS = False
    ENABLE_HTTPS = True
    
    # Logging
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    """Testing configuration"""
    
    DEBUG = True
    TESTING = True
    
    # Backend (Brain)
    BRAIN_HOST = "127.0.0.1"
    BRAIN_PORT = 5000
    
    # LLM (Ollama) - Mock
    OLLAMA_URL = "http://localhost:11434/api/generate"
    OLLAMA_MODEL = "test-model"
    OLLAMA_TIMEOUT = 1
    OLLAMA_RETRIES = 1
    
    # Frontend (ARM)
    SESSION_LOG = "/tmp/kaos_test_session.log"
    SESSION_TIMEOUT = 300


def get_config(environment: str = None) -> Config:
    """
    Get configuration object based on environment
    
    Args:
        environment: Environment name (dev/staging/prod/test)
        
    Returns:
        Configuration object
    """
    if environment is None:
        environment = os.getenv("KAOS_ENV", "development")
    
    configs = {
        "development": DevelopmentConfig,
        "staging": StagingConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    
    config_class = configs.get(environment, DevelopmentConfig)
    return config_class()

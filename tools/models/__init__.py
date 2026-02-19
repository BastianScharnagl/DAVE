"""
Main models package initialization
Provides access to all LISA models and the intelligent router
"""

# Import all model functions
from .lisa_pro import lisa_pro
from .lisa_flash import lisa_flash
from .lisa_vision import lisa_vision
from .lisa_code_101 import lisa_code_101
from .lisa_image_generation import lisa_image_generation
from .prompter_for_image_generator import prompter_for_image_generator

# Import and initialize the router
from .router import ModelRouter
router = ModelRouter()

# Make all components available at package level
__all__ = [
    'lisa_pro',
    'lisa_flash',
    'lisa_vision',
    'lisa_code_101',
    'lisa_image_generation',
    'prompter_for_image_generator',
    'ModelRouter',
    'router'
]

# Package metadata
__version__ = '1.0.0'
__author__ = 'LISA System'
__description__ = 'Specialized models for the LISA system with intelligent routing'
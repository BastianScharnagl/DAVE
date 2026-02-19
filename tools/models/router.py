import os
from typing import Dict, Any, Optional, List

# Import all model functions
from .lisa_pro import lisa_pro
from .lisa_flash import lisa_flash
from .lisa_vision import lisa_vision
from .lisa_code_101 import lisa_code_101
from .lisa_image_generation import lisa_image_generation
from .prompter_for_image_generator import prompter_for_image_generator

__all__ = [
    'lisa_pro',
    'lisa_flash',
    'lisa_vision',
    'lisa_code_101',
    'lisa_image_generation',
    'prompter_for_image_generator',
    'ModelRouter'
]

class ModelRouter:
    """A router class to intelligently select and route requests to appropriate models."""
    
    def __init__(self):
        self.models = {
            'pro': lisa_pro,
            'flash': lisa_flash,
            'vision': lisa_vision,
            'code': lisa_code_101,
            'image_generation': lisa_image_generation,
            'prompter': prompter_for_image_generator
        }
        
        # Define capabilities mapping for automatic routing
        self.capability_mapping = {
            'complex': 'pro',
            'reasoning': 'flash',
            'thinking': 'flash',
            'image analysis': 'vision',
            'picture': 'vision',
            'photo': 'vision',
            'programming': 'code',
            'coding': 'code',
            'code': 'code',
            'develop': 'code',
            'software': 'code',
            'generate image': 'image_generation',
            'create image': 'image_generation',
            'draw': 'image_generation',
            'paint': 'image_generation',
            'prompt': 'prompter',
            'enhance': 'prompter',
            'improve': 'prompter'
        }
    
    def route(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Intelligently route the request to the most appropriate model.
        
        Args:
            prompt (str): The input prompt to analyze for routing
            **kwargs: Additional arguments to pass to the model function
            
        Returns:
            Dict[str, Any]: The response from the appropriate model
        """
        prompt_lower = prompt.lower()
        
        # Check for specific model requests
        if 'lisa pro' in prompt_lower:
            return self.models['pro'](prompt, **kwargs)
        elif 'lisa flash' in prompt_lower:
            return self.models['flash'](prompt, **kwargs)
        elif 'lisa vision' in prompt_lower:
            return self.models['vision']('', **kwargs) if 'image_path' in kwargs else self.models['vision'](prompt, **kwargs)
        elif 'lisa code' in prompt_lower or 'lisa-code' in prompt_lower:
            return self.models['code'](prompt, **kwargs)
        elif 'lisa bildgenerierung' in prompt_lower or 'lisa image generation' in prompt_lower:
            return self.models['image_generation'](prompt, **kwargs)
        elif 'prompter' in prompt_lower:
            return self.models['prompter'](prompt, **kwargs)
        
        # Automatic routing based on keywords
        for keyword, model_key in self.capability_mapping.items():
            if keyword in prompt_lower:
                return self.models[model_key](prompt, **kwargs)
        
        # Default to LISA Pro for general queries
        return self.models['pro'](prompt, **kwargs)
        
    def get_available_models(self) -> List[str]:
        """Get list of available models.
        
        Returns:
            List[str]: List of available model keys
        """
        return list(self.models.keys())
        
    def get_model_capabilities(self) -> Dict[str, List[str]]:
        """Get capabilities of all models.
        
        Returns:
            Dict[str, List[str]]: Dictionary mapping model keys to their capabilities
        """
        # This would be enhanced with actual capability information
        return {
            'pro': ['complex_tasks', 'broad_knowledge', 'large_context'],
            'flash': ['deep_reasoning', 'complex_questions'],
            'vision': ['image_understanding', 'visual_description'],
            'code': ['programming', 'code_generation'],
            'image_generation': ['image_creation', 'visual_content'],
            'prompter': ['prompt_enhancement', 'optimization']
        }
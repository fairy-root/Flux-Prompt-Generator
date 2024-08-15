from .flux_prompt_generator import FluxPromptGenerator

NODE_CLASS_MAPPINGS = {
    "FluxPromptGenerator": FluxPromptGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxPromptGenerator": "Flux Prompt Generator"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
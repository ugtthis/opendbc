"""
Helper functions for working with model data.

This module provides utility functions for working with model data
that can be used across different brand implementations.
"""

from typing import Dict, List, Optional, Any, Set, TypeVar, Generic
from enum import Enum

T = TypeVar('T', bound=Enum)

def get_model_data(model_data_dict: Dict[str, Dict[str, Any]], model_id: str) -> Optional[Dict[str, Any]]:
    """Get the metadata for a specific model from a model data dictionary."""
    return model_data_dict.get(model_id)

def get_visible_models(model_data_dict: Dict[str, Dict[str, Any]]) -> List[str]:
    """Get a list of all models that should be visible in documentation."""
    return [model_id for model_id, data in model_data_dict.items()]

def get_model_by_platform(model_data_dict: Dict[str, Dict[str, Any]], platform: str) -> Optional[str]:
    """Get the model ID for a specific platform."""
    for model_id, data in model_data_dict.items():
        if data.get("platform") == platform:
            return model_id
    return None

def get_all_parts_for_model(explicit_parts: List[Enum]) -> List[Enum]:
    """
    Get all parts including dependencies for a model.
    
    This function works with any enum-based parts system where the enum values
    have an all_parts() method that returns a list of dependent parts.
    """
    all_parts = []
    processed_parts = set()
    
    for part_enum in explicit_parts:
        if part_enum in processed_parts:
            continue
            
        all_parts.append(part_enum)
        processed_parts.add(part_enum)
        
        # Add dependencies through the all_parts() method
        if hasattr(part_enum.value, 'all_parts'):
            for dep_part in part_enum.value.all_parts():
                if dep_part not in processed_parts:
                    all_parts.append(dep_part)
                    processed_parts.add(dep_part)
    
    return all_parts 
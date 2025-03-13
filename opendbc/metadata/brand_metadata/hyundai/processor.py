"""
Hyundai metadata processor.

This module handles Hyundai vehicle metadata for documentation and UI purposes.
Focuses on harness selection and relevant footnotes based on model/year.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum

from opendbc.metadata.base.processor import BaseProcessor
from opendbc.metadata.base.flag_processor import FlagConfig
from opendbc.metadata.base.parts import CarParts, PartCategory
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.constants import COLUMNS
from opendbc.metadata.base.model_helpers import (
    get_model_data as base_get_model_data,
    get_visible_models as base_get_visible_models,
    get_model_by_platform as base_get_model_by_platform,
    get_all_parts_for_model
)
from opendbc.car.hyundai.values import HyundaiFlags, Footnote as HyundaiFootnote, CAR
from opendbc.metadata.base.parts_definitions import Kit, Category, Harness, Tool  # Direct import from new system
from opendbc.metadata.brand_metadata.hyundai.footnotes import (
    FOOTNOTES, get_footnote, get_footnotes_for_model
)
from opendbc.car.hyundai.values import HyundaiCanFDPlatformConfig

@dataclass
class HyundaiProcessor(BaseProcessor):
    """Processor for Hyundai vehicle metadata."""
    
    def process_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Process metadata for a specific model."""
        model_data = self.get_model_data(model_id)
        if not model_data:
            return None
            
        # Process parts
        parts = self._get_parts(model_id)
        
        # Process footnotes
        footnotes = self._get_footnotes(model_data)
        
        # Store the results
        self.parts_data[model_id] = parts
        self.footnotes[model_id] = footnotes
        
        return model_data
        
    def _get_parts(self, model_id: str) -> Optional[CarParts]:
        """Get required parts based on model data."""
        model_data = self.get_model_data(model_id)
        if not model_data:
            return None
            
        explicit_parts = model_data.get("explicit_parts", [])
        
        if not explicit_parts:
            return None
        
        # Convert string references to actual enum objects
        enum_parts = []
        for part in explicit_parts:
            # Handle both string references and enum objects
            if isinstance(part, str):
                if part.startswith("Harness.HYUNDAI_"):
                    harness_letter = part.split("_")[-1]
                    enum_parts.append(getattr(Harness, f"HYUNDAI_{harness_letter}"))
                elif part == "Kit.CANFD_KIT":
                    enum_parts.append(Kit.CANFD_KIT)
            elif isinstance(part, Enum):
                enum_parts.append(part)
        
        # Check for flags that require additional parts
        platform = model_data.get("platform")
        if platform and hasattr(CAR, platform):
            car_config = getattr(CAR, platform)
            # Check if the car config has the CANFD flag
            if hasattr(car_config.config, 'flags') and car_config.config.flags & HyundaiFlags.CANFD:
                enum_parts.append(Kit.CANFD_KIT)
        
        # Add pry tool for all models
        enum_parts.append(Tool.PRY_TOOL)
        
        all_parts = get_all_parts_for_model(enum_parts)
        
        if not all_parts:
            return None
        
        # Separate parts and tools
        parts = []
        tools = []
        
        for part in all_parts:
            if part.value.category == Category.TOOL:
                tools.append(part)
            else:
                parts.append(part)
                
        # Convert to CarParts for compatibility
        return CarParts.create_from_enums(parts=parts, tools=tools)
        
    def _get_footnotes(self, model_data: Dict[str, Any]) -> Optional[FootnoteCollection]:
        """Get footnotes based on model data."""
        explicit_footnotes = model_data.get("explicit_footnotes", [])
        
        if not explicit_footnotes:
            return None
            
        footnotes = get_footnotes_for_model(explicit_footnotes)
        
        # Add min_speed footnote if the model has the MIN_STEER_32_MPH flag
        platform = model_data.get("platform")
        if platform and platform in ["HYUNDAI_ELANTRA"]:
            footnotes["min_speed"] = Footnote("Minimum engage speed applies", ["FSR_LONGITUDINAL"])
                
        return FootnoteCollection.create(footnotes)
    
    def get_model_data(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get the metadata for a specific model."""
        from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
        return base_get_model_data(MODEL_DATA, model_id)
        
    def get_visible_models(self) -> List[str]:
        """Get a list of all models that should be visible in documentation."""
        from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
        return base_get_visible_models(MODEL_DATA)
        
    def get_model_by_platform(self, platform: str) -> Optional[str]:
        """Get the model ID for a specific platform."""
        from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
        return base_get_model_by_platform(MODEL_DATA, platform)

    # Define flag configurations with direct references
    FLAGS = HyundaiFlags
    FLAG_CONFIGS = [
        FlagConfig(
            flag_name='MIN_STEER_32_MPH',
            footnote_key='min_speed',
            footnote_text='Minimum engage speed applies',
            footnote_column='FSR_LONGITUDINAL'
        ),
        FlagConfig(
            flag_name='MANDO_RADAR',
            footnote_key='radar_scc',
            footnote_text='Uses radar-based Smart Cruise Control',
            footnote_column='LONGITUDINAL'
        ),
    ]

    def __init__(self):
        super().__init__()
        self._initialize_common_footnotes()

    def _initialize_common_footnotes(self):
        """Initialize common footnotes."""
        # Base SCC footnote always required
        self.common_footnotes = {
            'scc': Footnote('Requires Smart Cruise Control (SCC)', ['LONGITUDINAL']),
            'min_speed': Footnote('Minimum engage speed applies', ['FSR_LONGITUDINAL']),
            'radar_scc': Footnote('Uses radar-based Smart Cruise Control', ['LONGITUDINAL']),
        }

    def get_parts(self, model_id: str) -> Optional[CarParts]:
        """Get parts for a specific model."""
        return self.parts_data.get(model_id) or self._get_parts(model_id)
        
    def get_footnotes(self, model_id: str) -> Optional[FootnoteCollection]:
        """Get footnotes for a specific model."""
        return self.footnotes.get(model_id) 
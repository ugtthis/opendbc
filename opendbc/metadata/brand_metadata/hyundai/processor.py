"""
Hyundai metadata processor.

This module handles Hyundai vehicle metadata for documentation and UI purposes.
Focuses on harness selection and relevant footnotes based on model/year.
"""

from typing import Dict, List, Optional, Any

from opendbc.metadata.base.processor import BaseProcessor
from opendbc.metadata.base.flag_processor import FlagConfig
from opendbc.metadata.base.parts import Part, CarParts, PartCategory
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.constants import COLUMNS
from opendbc.car.hyundai.values import HyundaiFlags, Footnote as HyundaiFootnote
from opendbc.metadata.brand_metadata.hyundai.attributes import (
    get_model_data, get_visible_models, get_model_by_platform,
    get_all_parts_for_model, get_footnotes_for_model, HyundaiKit
)

from dataclasses import dataclass

@dataclass
class HyundaiProcessor(BaseProcessor):
    """Processor for Hyundai vehicle metadata."""
    
    def process_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Process metadata for a specific model."""
        model_data = get_model_data(model_id)
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
        model_data = get_model_data(model_id)
        if not model_data:
            return None
            
        explicit_parts = model_data.get("explicit_parts", [])
        
        if not explicit_parts:
            return None
        
        all_parts = get_all_parts_for_model(explicit_parts)
        
        if not all_parts:
            return None
        
        # Separate parts and tools
        parts = []
        tools = []
        
        for part in all_parts:
            if part.category == PartCategory.TOOL:
                tools.append(part)
            else:
                parts.append(part)
                
        return CarParts.create(parts=parts, tools=tools)
        
    def _get_footnotes(self, model_data: Dict[str, Any]) -> Optional[FootnoteCollection]:
        """Get footnotes based on model data."""
        explicit_footnotes = model_data.get("explicit_footnotes", [])
        
        if not explicit_footnotes:
            return None
            
        footnotes = get_footnotes_for_model(explicit_footnotes)
                
        return FootnoteCollection.create(footnotes)
        
    def get_visible_models(self) -> List[str]:
        """Get a list of all models that should be visible in documentation."""
        return get_visible_models()
        
    def get_model_by_platform(self, platform: str) -> Optional[str]:
        """Get the model ID for a specific platform."""
        return get_model_by_platform(platform)

    # Define flag configurations
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
        FlagConfig(
            flag_name='CANFD',
            footnote_key='canfd',
            footnote_text=HyundaiFootnote.CANFD.value.text,
            footnote_column='MODEL',
            part_required=HyundaiKit.CANFD_KIT
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
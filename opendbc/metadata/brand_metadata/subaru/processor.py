"""
Subaru-specific metadata processor.

This module extends the base processor to handle Subaru-specific metadata,
including platform configurations, parts, and footnotes.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from opendbc.metadata.base.processor import BaseProcessor, ModelData
from opendbc.metadata.base.parts import CarParts, PartCategory
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.constants import COLUMNS
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit, Category
from opendbc.car.subaru.values import SubaruFlags, CAR, Footnote as SubaruFootnote

@dataclass
class SubaruProcessor(BaseProcessor):
    """Processor for Subaru vehicle metadata."""
    
    def __init__(self):
        """Initialize the Subaru processor with brand-specific data."""
        super().__init__()
        self._initialize_common_footnotes()
    
    def _initialize_common_footnotes(self):
        """Initialize common footnotes used across Subaru models."""
        self.common_footnotes = {
            "eyesight": Footnote(
                text="Requires EyeSight with Lane Keep Assist",
                columns=["PACKAGE"]
            ),
            "angle_lkas": Footnote(
                text="Uses angle-based Lane Keep Assist System",
                columns=["STEERING_TORQUE"]
            ),
            "torque_lkas": Footnote(
                text="Uses torque-based Lane Keep Assist System",
                columns=["STEERING_TORQUE"]
            ),
            "steer_rate": Footnote(
                text="Vehicle may temporarily fault when steering angle rate exceeds threshold",
                columns=["STEERING_TORQUE"]
            ),
            "global": Footnote(
                text=SubaruFootnote.GLOBAL.value.text,
                columns=["PACKAGE"]  # From values.py
            ),
            "exp_long": Footnote(
                text=SubaruFootnote.EXP_LONG.value.text,
                columns=["LONGITUDINAL"]  # From values.py
            )
        }
    
    def process_model(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Process metadata for a specific Subaru model."""
        model_data = super().process_model(model_id)
        if not model_data:
            return None
            
        # Add model-specific parts
        parts = self._get_parts(model_data)
        if parts:
            self.parts_data[model_id] = parts
            
        # Add model-specific footnotes
        footnotes = self._get_model_footnotes(model_data)
        if footnotes:
            self.footnotes[model_id] = footnotes
            
        return model_data
    
    def _get_parts(self, model_data: ModelData) -> Optional[CarParts]:
        """Get parts specific to a Subaru model based on platform configuration."""
        # Determine which harness to use based on platform configuration
        harness = None
        tools = [Tool.SOCKET_8MM_DEEP, Tool.PRY_TOOL]
        
        # Match exact harness assignments from values.py
        if model_data.platform in ["SUBARU_OUTBACK_2023", "SUBARU_ASCENT_2023"]:
            harness = Harness.SUBARU_D
        elif model_data.platform == "SUBARU_FORESTER_2022":
            harness = Harness.SUBARU_C
        elif (model_data.platform in ["SUBARU_OUTBACK", "SUBARU_LEGACY"] or
              model_data.platform == "SUBARU_CROSSTREK_HYBRID"):
            harness = Harness.SUBARU_B
        else:
            harness = Harness.SUBARU_A
            
        return CarParts.create_from_enums(
            parts=[harness],
            tools=tools
        )
    
    def _get_model_footnotes(self, model_data: ModelData) -> Optional[FootnoteCollection]:
        """Get footnotes specific to a Subaru model."""
        footnotes = {}
        
        # Get platform configuration from CAR enum
        platform_config = getattr(CAR, model_data.platform).config
        
        # All Subaru models require EyeSight and have global market footnote
        footnotes["eyesight"] = self.common_footnotes["eyesight"]
        footnotes["global"] = self.common_footnotes["global"]
        
        # Add LKAS type footnote based on platform flags
        if platform_config.flags & SubaruFlags.LKAS_ANGLE:
            footnotes["angle_lkas"] = self.common_footnotes["angle_lkas"]
        else:
            footnotes["torque_lkas"] = self.common_footnotes["torque_lkas"]
            
        # Add steering rate limit footnote if applicable
        if platform_config.flags & SubaruFlags.STEER_RATE_LIMITED:
            footnotes["steer_rate"] = self.common_footnotes["steer_rate"]
        
        # Add experimental longitudinal control footnote if available
        if hasattr(platform_config, "experimentalLongitudinalAvailable") and platform_config.experimentalLongitudinalAvailable:
            footnotes["exp_long"] = self.common_footnotes["exp_long"]
            
        return FootnoteCollection.create(footnotes)
    
    def get_model_by_platform(self, platform: str) -> Optional[str]:
        """Get the model ID for a specific platform."""
        for model_id, data in self.model_data.items():
            if data.platform == platform:
                return model_id
        return None

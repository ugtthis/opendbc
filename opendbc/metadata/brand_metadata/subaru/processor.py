"""
Subaru-specific metadata processor.

This module extends the base processor to handle Subaru-specific metadata,
including platform configurations, parts, and footnotes.
"""

from typing import Dict, List, Optional

from opendbc.metadata.base.processor import BaseProcessor, ModelData
from opendbc.metadata.base.parts import CarParts, Part, Tool, BrandPartProcessor, PartCategory, PlatformParts
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.constants import COLUMNS
from opendbc.car.subaru.values import SubaruFlags, CAR, Footnote as SubaruFootnote

class SubaruProcessor(BaseProcessor):
    """Processor for Subaru vehicle metadata."""
    
    def __init__(self):
        """Initialize the Subaru processor with brand-specific data."""
        super().__init__()
        self._initialize_common_parts()
        self._initialize_common_footnotes()
    
    def _initialize_common_parts(self):
        """Initialize common parts used across Subaru models."""
        self.common_parts = {
            "harness_a": Part(
                id="subaru_a",
                name="Subaru A Harness",
                category=PartCategory.HARNESS,
                description="For pre-2020 models with torque-based LKAS",
                url="https://comma.ai/shop/harnesses/subaru-a"
            ),
            "harness_b": Part(
                id="subaru_b",
                name="Subaru B Harness",
                category=PartCategory.HARNESS,
                description="For 2020-22 Outback/Legacy and 2020 Crosstrek Hybrid",
                url="https://comma.ai/shop/harnesses/subaru-b"
            ),
            "harness_c": Part(
                id="subaru_c",
                name="Subaru C Harness",
                category=PartCategory.HARNESS,
                description="For 2022-24 Forester",
                url="https://comma.ai/shop/harnesses/subaru-c"
            ),
            "harness_d": Part(
                id="subaru_d",
                name="Subaru D Harness",
                category=PartCategory.HARNESS,
                description="For 2023+ Outback and Ascent with angle-based LKAS",
                url="https://comma.ai/shop/harnesses/subaru-d"
            )
        }
        
        self.common_tools = [
            Tool(
                name="Socket 8mm Deep",
                description="For removing steering column covers"
            ),
            Tool(
                name="Trim Removal Tool",
                description="For removing trim pieces"
            )
        ]
    
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
    
    def process_model(self, model_id: str) -> Optional[ModelData]:
        """Process metadata for a specific Subaru model."""
        model_data = super().process_model(model_id)
        if not model_data:
            return None
            
        # Add model-specific parts
        parts = self._get_model_parts(model_data)
        if parts:
            self.parts_data[model_id] = parts
            
        # Add model-specific footnotes
        footnotes = self._get_model_footnotes(model_data)
        if footnotes:
            self.footnotes[model_id] = footnotes
            
        return model_data
    
    def _get_model_parts(self, model_data: ModelData) -> Optional[CarParts]:
        """Get parts specific to a Subaru model based on values.py assignments."""
        # Determine which harness to use based on platform configuration
        harness = None
        
        # Match exact harness assignments from values.py
        if model_data.platform in ["SUBARU_OUTBACK_2023", "SUBARU_ASCENT_2023"]:
            harness = self.common_parts["harness_d"]
        elif model_data.platform == "SUBARU_FORESTER_2022":
            harness = self.common_parts["harness_c"]
        elif (model_data.platform in ["SUBARU_OUTBACK", "SUBARU_LEGACY"] or
              model_data.platform == "SUBARU_CROSSTREK_HYBRID"):
            harness = self.common_parts["harness_b"]
        else:
            harness = self.common_parts["harness_a"]
            
        return CarParts.create(
            parts=[harness],
            tools=self.common_tools
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
            footnotes["lkas"] = self.common_footnotes["angle_lkas"]
        else:
            footnotes["lkas"] = self.common_footnotes["torque_lkas"]
            
        # Add steering rate limit footnote if applicable
        if platform_config.flags & SubaruFlags.STEER_RATE_LIMITED:
            footnotes["steer_rate"] = self.common_footnotes["steer_rate"]
        
        # Add experimental longitudinal control footnote if available
        if hasattr(platform_config, "experimentalLongitudinalAvailable") and platform_config.experimentalLongitudinalAvailable:
            footnotes["exp_long"] = self.common_footnotes["exp_long"]
            
        return FootnoteCollection.create(footnotes)

class SubaruPartProcessor(BrandPartProcessor):
    """Processor for determining Subaru parts based on platform flags."""
    
    def __init__(self):
        # Define parts catalog
        self.HARNESS_A = Part(
            id="subaru_a",
            name="Subaru Harness Type A",
            category=PartCategory.HARNESS,
            description="For pre-Global platform vehicles"
        )
        self.HARNESS_B = Part(
            id="subaru_b",
            name="Subaru Harness Type B",
            category=PartCategory.HARNESS,
            description="For Global platform vehicles"
        )
        self.HARNESS_C = Part(
            id="subaru_c",
            name="Subaru Harness Type C",
            category=PartCategory.HARNESS,
            description="For 2022+ Forester with LKAS"
        )
        self.HARNESS_D = Part(
            id="subaru_d",
            name="Subaru Harness Type D",
            category=PartCategory.HARNESS,
            description="For 2023+ vehicles with LKAS"
        )
        
        # Tools
        self.SOCKET_8MM = Part(
            id="socket_8mm_deep",
            name="8mm Deep Socket",
            category=PartCategory.TOOL,
            description="For removing OBD port cover"
        )
        self.PRY_TOOL = Part(
            id="pry_tool",
            name="Trim Removal Tool",
            category=PartCategory.TOOL,
            description="For removing trim pieces"
        )

    def get_parts_for_platform(self, platform_config) -> PlatformParts:
        """Get parts based on platform flags from values.py."""
        parts = PlatformParts(
            required_parts=set(),
            tools={self.SOCKET_8MM, self.PRY_TOOL}  # All Subarus need these
        )

        # Extract years from car_docs
        years = []
        for car_doc in platform_config.car_docs:
            _, _, year_str = car_doc.name.rpartition(" ")
            if "-" in year_str:
                start, end = year_str.split("-")
                if len(end) == 2:  # Handle two-digit years
                    end = f"20{end}"
                years.extend(range(int(start), int(end) + 1))
            else:
                years.append(int(year_str))

        # Use existing flags from values.py
        if platform_config.flags & SubaruFlags.LKAS_ANGLE:
            # Check if it's a Forester 2022-24
            is_forester = any("Forester" in doc.name for doc in platform_config.car_docs)
            if is_forester:
                parts.required_parts.add(self.HARNESS_C)  # 2022+ Forester
            else:
                parts.required_parts.add(self.HARNESS_D)  # 2023+ with angle-based LKAS
        elif platform_config.flags & SubaruFlags.GLOBAL_GEN2:
            parts.required_parts.add(self.HARNESS_B)  # 2020-22 Outback/Legacy
        else:
            parts.required_parts.add(self.HARNESS_A)  # Pre-2020 models

        return parts

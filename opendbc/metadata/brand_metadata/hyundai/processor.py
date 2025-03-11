"""
Hyundai metadata processor.

This module handles Hyundai vehicle metadata for documentation and UI purposes.
Focuses on harness selection and relevant footnotes based on model/year.
"""

from typing import Dict, List, Optional

from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.base.flag_processor import FlagBasedProcessor, FlagConfig
from opendbc.metadata.base.parts import Part, CarParts, Tool, BrandPartProcessor, PartCategory, PlatformParts
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.constants import COLUMNS
from opendbc.metadata.base.parts_catalog import PartsCatalog, HarnessId, ToolId, AccessoryId, KitId
from opendbc.car.hyundai.values import HyundaiFlags, CAR, Footnote as HyundaiFootnote

from dataclasses import dataclass

@dataclass
class HyundaiProcessor(FlagBasedProcessor):
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
            part_required='canfd_kit'
        ),
    ]

    def __init__(self):
        super().__init__()
        self._initialize_common_parts()
        self._initialize_common_footnotes()

    def _initialize_common_parts(self):
        """Initialize parts catalog."""
        self.common_parts = {
            'harness_a': PartsCatalog.get_harness(HarnessId.HYUNDAI_A),
            'harness_b': PartsCatalog.get_harness(HarnessId.HYUNDAI_B),
            'harness_g': PartsCatalog.get_harness(HarnessId.HYUNDAI_G),
            'harness_k': PartsCatalog.get_harness(HarnessId.HYUNDAI_K),
            'canfd_kit': PartsCatalog.get_kit(KitId.CANFD_KIT),
        }

        self.common_tools = [
            PartsCatalog.get_tool(ToolId.PRY_TOOL)
        ]

    def _initialize_common_footnotes(self):
        """Initialize common footnotes."""
        # Base SCC footnote always required
        self.common_footnotes = {
            'scc': Footnote('Requires Smart Cruise Control (SCC)', ['LONGITUDINAL']),
            'min_speed': Footnote('Minimum engage speed applies', ['FSR_LONGITUDINAL']),
            'radar_scc': Footnote('Uses radar-based Smart Cruise Control', ['LONGITUDINAL']),
        }

    def _get_platform_flags(self, model_data: ModelData) -> int:
        """Get flags for a specific platform from values.py."""
        platform = getattr(CAR, model_data.platform)
        return platform.config.flags

    def _get_base_parts(self, model_data: ModelData) -> List[Part]:
        """Get base harness based on model and year."""
        model = model_data.model.lower()
        year = model_data.years[0]  # Use first year for harness selection
        
        # Match values.py harness selection exactly
        if model == 'elantra':
            if year >= 2021:
                return [self.common_parts['harness_k']]  # HYUNDAI_ELANTRA_2021
            elif year == 2019:
                return [self.common_parts['harness_g']]  # HYUNDAI_ELANTRA
            elif year <= 2018:
                return [self.common_parts['harness_b']]  # HYUNDAI_ELANTRA
        elif model == 'sonata' and year >= 2020:
            return [self.common_parts['harness_a']]  # HYUNDAI_SONATA
        
        return []

    def process_model(self, model_id: str) -> Optional[Dict[str, str]]:
        """Process metadata for a specific model."""
        model_data = super().process_model(model_id)
        if not model_data:
            return None

        parts = self._get_parts(model_data)
        footnotes = self._get_footnotes(model_data)

        if not parts or not footnotes:
            return None

        # Store the results
        self.parts_data[model_id] = parts
        self.footnotes[model_id] = footnotes

        return model_data

    def _get_parts(self, model_data: ModelData) -> Optional[CarParts]:
        """Get required parts based on model and year."""
        model = model_data.model.lower()
        year = model_data.years[0]  # Use first year for harness selection
        
        parts = []

        # Match values.py harness selection exactly
        if model == 'elantra':
            if year >= 2021:
                parts.append(self.common_parts['harness_k'])  # HYUNDAI_ELANTRA_2021
            elif year == 2019:
                parts.append(self.common_parts['harness_g'])  # HYUNDAI_ELANTRA
            elif year <= 2018:
                parts.append(self.common_parts['harness_b'])  # HYUNDAI_ELANTRA
        elif model == 'sonata' and year >= 2020:
            parts.append(self.common_parts['harness_a'])  # HYUNDAI_SONATA
        else:
            return None

        return CarParts.create(parts=parts, tools=self.common_tools)

    def _get_footnotes(self, model_data: ModelData) -> Optional[FootnoteCollection]:
        """Get relevant footnotes based on model and year."""
        model = model_data.model.lower()
        year = model_data.years[0]  # Use first year for footnote selection
        
        footnotes = {}
        
        # All supported Hyundai models require SCC
        footnotes['scc'] = self.common_footnotes['scc']

        # Add minimum speed footnote for models with MIN_STEER_32_MPH flag
        if model == 'elantra' and year <= 2019:  # HYUNDAI_ELANTRA has MIN_STEER_32_MPH
            footnotes['min_speed'] = self.common_footnotes['min_speed']

        # Add SCC type footnote based on flags
        if model == 'sonata' and year >= 2020:  # HYUNDAI_SONATA has MANDO_RADAR
            footnotes['radar_scc'] = self.common_footnotes['radar_scc']

        return FootnoteCollection.create(footnotes)

class HyundaiPartProcessor(BrandPartProcessor):
    """Processor for determining Hyundai parts based on platform flags."""
    
    def __init__(self):
        # Define parts catalog
        # Harnesses
        self.HARNESS_A = Part(
            id="hyundai_a",
            name="Hyundai Type A Harness",
            category=PartCategory.HARNESS,
            description="For newer models with standard SCC"
        )
        self.HARNESS_B = Part(
            id="hyundai_b",
            name="Hyundai Type B Harness",
            category=PartCategory.HARNESS,
            description="For older models with standard SCC"
        )
        self.HARNESS_C = Part(
            id="hyundai_c",
            name="Hyundai Type C Harness",
            category=PartCategory.HARNESS,
            description="For hybrid/EV models with standard SCC"
        )
        self.HARNESS_D = Part(
            id="hyundai_d",
            name="Hyundai Type D Harness",
            category=PartCategory.HARNESS,
            description="For models with Mando radar"
        )
        self.HARNESS_E = Part(
            id="hyundai_e",
            name="Hyundai Type E Harness",
            category=PartCategory.HARNESS,
            description="For legacy models"
        )
        self.HARNESS_F = Part(
            id="hyundai_f",
            name="Hyundai Type F Harness",
            category=PartCategory.HARNESS,
            description="For Genesis models"
        )
        self.HARNESS_G = Part(
            id="hyundai_g",
            name="Hyundai Type G Harness",
            category=PartCategory.HARNESS,
            description="For models with unsupported longitudinal"
        )
        self.HARNESS_H = Part(
            id="hyundai_h",
            name="Hyundai Type H Harness",
            category=PartCategory.HARNESS,
            description="For newer hybrid/EV models"
        )
        self.HARNESS_I = Part(
            id="hyundai_i",
            name="Hyundai Type I Harness",
            category=PartCategory.HARNESS,
            description="For Kona Hybrid 2020"
        )
        self.HARNESS_K = Part(
            id="hyundai_k",
            name="Hyundai Type K Harness",
            category=PartCategory.HARNESS,
            description="For CAN FD models"
        )
        self.HARNESS_L = Part(
            id="hyundai_l",
            name="Hyundai Type L Harness",
            category=PartCategory.HARNESS,
            description="For newer models with CAN FD"
        )
        self.HARNESS_N = Part(
            id="hyundai_n",
            name="Hyundai Type N Harness",
            category=PartCategory.HARNESS,
            description="For 4th gen Tucson and Santa Cruz"
        )
        self.HARNESS_O = Part(
            id="hyundai_o",
            name="Hyundai Type O Harness",
            category=PartCategory.HARNESS,
            description="For 2022-23 Kona models"
        )
        self.HARNESS_P = Part(
            id="hyundai_p",
            name="Hyundai Type P Harness",
            category=PartCategory.HARNESS,
            description="For Ioniq 6 with HDA II"
        )
        self.HARNESS_Q = Part(
            id="hyundai_q",
            name="Hyundai Type Q Harness",
            category=PartCategory.HARNESS,
            description="For Ioniq 5 with HDA II"
        )

        # Tools
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
            tools={self.PRY_TOOL}  # All Hyundais need this
        )

        # Extract model info from car_docs
        model_name = platform_config.car_docs[0].name.lower()
        is_genesis = "genesis" in model_name
        is_ioniq = "ioniq" in model_name
        is_kona = "kona" in model_name
        has_hda2 = any("HDA II" in doc.package or "Highway Driving Assist II" in doc.package for doc in platform_config.car_docs)
        
        # Special case for Kona 2022-23 models
        if is_kona and any(year in model_name for year in ["2022", "2023"]):
            parts.required_parts.add(self.HARNESS_O)
            return parts
            
        # Special case for Kona Hybrid 2020
        if "kona hybrid 2020" in model_name:
            parts.required_parts.add(self.HARNESS_I)
            return parts
            
        # Special case for Sonata Hybrid
        if "sonata hybrid" in model_name:
            parts.required_parts.add(self.HARNESS_A)
            return parts

        # Determine harness based on flags and model
        if platform_config.flags & HyundaiFlags.CANFD:
            # Special case for Ioniq 6 (always has HDA II)
            if "ioniq 6" in model_name:
                parts.required_parts.add(self.HARNESS_P)
            # Special case for Ioniq 5 with HDA II
            elif "ioniq 5" in model_name and has_hda2:
                parts.required_parts.add(self.HARNESS_Q)
            elif any(model in model_name for model in ["tucson", "santa cruz"]):
                parts.required_parts.add(self.HARNESS_N)
            elif is_genesis or "staria" in model_name:
                parts.required_parts.add(self.HARNESS_K)
            else:
                parts.required_parts.add(self.HARNESS_L)
        elif platform_config.flags & HyundaiFlags.LEGACY:
            parts.required_parts.add(self.HARNESS_E)
        elif platform_config.flags & HyundaiFlags.UNSUPPORTED_LONGITUDINAL:
            parts.required_parts.add(self.HARNESS_G)
        elif platform_config.flags & HyundaiFlags.MANDO_RADAR:
            parts.required_parts.add(self.HARNESS_D)
        elif platform_config.flags & (HyundaiFlags.HYBRID | HyundaiFlags.EV):
            if is_ioniq or "2020" in model_name:
                parts.required_parts.add(self.HARNESS_H)
            else:
                parts.required_parts.add(self.HARNESS_C)
        elif is_genesis:
            parts.required_parts.add(self.HARNESS_F)
        else:
            # Standard SCC models
            if any(year in model_name for year in ["2020", "2021", "2022", "2023"]):
                parts.required_parts.add(self.HARNESS_A)
            else:
                parts.required_parts.add(self.HARNESS_B)

        return parts 
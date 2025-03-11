"""
Static metadata attributes for Hyundai vehicles.

This module contains all the non-functional metadata for Hyundai vehicles,
including model information, parts, footnotes, and other documentation-related information.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from opendbc.metadata.base.parts import Part, PartCategory
from opendbc.metadata.base.footnotes import Footnote
from opendbc.metadata.base.constants import COLUMNS

# ===== PARTS DEFINITIONS =====

# Base part class for enums
class BasePart:
    """Base class for part enums to store the actual Part object."""
    def __init__(self, part: Part):
        self.part = part

# Harness enum
class HyundaiHarness(Enum):
    """Enum for Hyundai harnesses."""
    A = BasePart(Part(
        id="hyundai_harness_a",
        name="Hyundai A connector",
        category=PartCategory.HARNESS,
        description="For Hyundai Sonata 2020+ models",
        url="https://comma.ai/shop/products/comma-car-harness"
    ))
    
    B = BasePart(Part(
        id="hyundai_harness_b",
        name="Hyundai B connector",
        category=PartCategory.HARNESS,
        description="For Hyundai Elantra 2017-18 models",
        url="https://comma.ai/shop/products/comma-car-harness"
    ))
    
    C = BasePart(Part(
        id="hyundai_c",
        name="Hyundai C connector",
        category=PartCategory.HARNESS,
        description="For hybrid/EV models with standard SCC"
    ))
    
    D = BasePart(Part(
        id="hyundai_d",
        name="Hyundai D connector",
        category=PartCategory.HARNESS,
        description="For models with Mando radar"
    ))
    
    E = BasePart(Part(
        id="hyundai_e",
        name="Hyundai E connector",
        category=PartCategory.HARNESS,
        description="For legacy models"
    ))
    
    F = BasePart(Part(
        id="hyundai_f",
        name="Hyundai F connector",
        category=PartCategory.HARNESS,
        description="For Genesis models"
    ))
    
    G = BasePart(Part(
        id="hyundai_harness_g",
        name="Hyundai G connector",
        category=PartCategory.HARNESS,
        description="For Hyundai Elantra 2019 models",
        url="https://comma.ai/shop/products/comma-car-harness"
    ))
    
    H = BasePart(Part(
        id="hyundai_h",
        name="Hyundai H connector",
        category=PartCategory.HARNESS,
        description="For newer hybrid/EV models"
    ))
    
    I = BasePart(Part(
        id="hyundai_i",
        name="Hyundai I connector",
        category=PartCategory.HARNESS,
        description="For Kona Hybrid 2020"
    ))
    
    J = BasePart(Part(
        id="hyundai_j",
        name="Hyundai J connector",
        category=PartCategory.HARNESS,
        description="For Genesis 2015-17"
    ))
    
    K = BasePart(Part(
        id="hyundai_harness_k",
        name="Hyundai K connector",
        category=PartCategory.HARNESS,
        description="For Hyundai Elantra 2021+ models",
        url="https://comma.ai/shop/products/comma-car-harness"
    ))
    
    L = BasePart(Part(
        id="hyundai_l",
        name="Hyundai L connector",
        category=PartCategory.HARNESS,
        description="For newer models with CAN FD"
    ))
    
    M = BasePart(Part(
        id="hyundai_m",
        name="Hyundai M connector",
        category=PartCategory.HARNESS,
        description="For Genesis GV70 3.5T and GV80"
    ))
    
    N = BasePart(Part(
        id="hyundai_n",
        name="Hyundai N connector",
        category=PartCategory.HARNESS,
        description="For 4th gen Tucson and Santa Cruz"
    ))
    
    O = BasePart(Part(
        id="hyundai_o",
        name="Hyundai O connector",
        category=PartCategory.HARNESS,
        description="For Kona 2022 and Kona Electric 2022-23"
    ))
    
    P = BasePart(Part(
        id="hyundai_p",
        name="Hyundai P connector",
        category=PartCategory.HARNESS,
        description="For Ioniq 6 with HDA II"
    ))
    
    Q = BasePart(Part(
        id="hyundai_q",
        name="Hyundai Q connector",
        category=PartCategory.HARNESS,
        description="For Ioniq 5 with HDA II"
    ))
    
    R = BasePart(Part(
        id="hyundai_r",
        name="Hyundai R connector",
        category=PartCategory.HARNESS,
        description="For Kona Electric 2nd Gen"
    ))

# Tool enum
class HyundaiTool(Enum):
    """Enum for tools used with Hyundai vehicles."""
    PRY_TOOL = BasePart(Part(
        id="pry_tool",
        name="Pry Tool",
        category=PartCategory.TOOL,
        description="For removing interior trim pieces",
        url="https://comma.ai/shop/products/pry-tool"
    ))

# Kit enum
class HyundaiKit(Enum):
    """Enum for kits used with Hyundai vehicles."""
    CANFD_KIT = BasePart(Part(
        id="canfd_kit",
        name="CAN FD Kit",
        category=PartCategory.ACCESSORY,
        description="Required for CAN FD vehicles"
    ))

# Part dependencies mapping
PART_DEPENDENCIES = {
    # All harnesses require the pry tool
    HyundaiHarness.A: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.B: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.C: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.D: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.E: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.F: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.G: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.H: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.I: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.J: [HyundaiTool.PRY_TOOL],
    # Some harnesses also require the CAN FD kit
    HyundaiHarness.K: [HyundaiTool.PRY_TOOL, HyundaiKit.CANFD_KIT],
    HyundaiHarness.L: [HyundaiTool.PRY_TOOL, HyundaiKit.CANFD_KIT],
    HyundaiHarness.M: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.N: [HyundaiTool.PRY_TOOL, HyundaiKit.CANFD_KIT],
    HyundaiHarness.O: [HyundaiTool.PRY_TOOL],
    HyundaiHarness.P: [HyundaiTool.PRY_TOOL, HyundaiKit.CANFD_KIT],
    HyundaiHarness.Q: [HyundaiTool.PRY_TOOL, HyundaiKit.CANFD_KIT],
    HyundaiHarness.R: [HyundaiTool.PRY_TOOL],
}

# ===== FOOTNOTE DEFINITIONS =====

# Common footnotes
FOOTNOTE_SCC = Footnote(
    text="Requires Smart Cruise Control (SCC)",
    columns=["LONGITUDINAL", "STEERING_TORQUE"]
)

FOOTNOTE_MIN_SPEED = Footnote(
    text="Minimum engage speed is 32 mph (51 km/h)",
    columns=["FSR_STEERING"]
)

FOOTNOTE_RADAR_SCC = Footnote(
    text="Uses radar-based Smart Cruise Control",
    columns=["LONGITUDINAL"]
)

FOOTNOTE_CANFD = Footnote(
    text="Uses CAN FD communication",
    columns=["MODEL"]
)

# Footnotes dictionary for easy lookup
FOOTNOTES = {
    "scc": FOOTNOTE_SCC,
    "min_speed": FOOTNOTE_MIN_SPEED,
    "radar_scc": FOOTNOTE_RADAR_SCC,
    "canfd": FOOTNOTE_CANFD
}

# ===== MODEL DATA =====

MODEL_DATA = {
    "Hyundai Elantra 2017-18": {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2017, 2018],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["min_speed"],
        "explicit_parts": [HyundaiHarness.B],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 32 * 0.44704,  # 32 mph in m/s
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_ELANTRA"
    },
    "Hyundai Elantra 2019": {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2019],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["min_speed", "scc"],
        "explicit_parts": [HyundaiHarness.G],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 32 * 0.44704,  # 32 mph in m/s
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_ELANTRA"
    },
    "Hyundai Elantra 2021-23": {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2021, 2022, 2023],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["scc"],
        "explicit_parts": [HyundaiHarness.K],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_ELANTRA_2021"
    },
    "Hyundai Sonata 2020": {
        "make": "Hyundai",
        "model": "Sonata",
        "years": [2020],
        "package": "All",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["radar_scc", "scc"],
        "explicit_parts": [HyundaiHarness.A],
        "support_type": "upstream",
        "video_link": "https://www.youtube.com/watch?v=ix63r9kE3Fw",
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_SONATA"
    },
    "Hyundai Sonata Hybrid 2020-23": {
        "make": "Hyundai",
        "model": "Sonata Hybrid",
        "years": [2020, 2021, 2022, 2023],
        "package": "All",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["radar_scc"],
        "explicit_parts": [HyundaiHarness.A],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_SONATA_HYBRID"
    },
    "Hyundai Kona 2020": {
        "make": "Hyundai",
        "model": "Kona",
        "years": [2020],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["scc"],
        "explicit_parts": [HyundaiHarness.B],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_KONA"
    },
    "Hyundai Kona 2022": {
        "make": "Hyundai",
        "model": "Kona",
        "years": [2022],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["scc"],
        "explicit_parts": [HyundaiHarness.O],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_KONA_2022"
    },
    "Hyundai Kona Electric 2022-23": {
        "make": "Hyundai",
        "model": "Kona Electric",
        "years": [2022, 2023],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["scc"],
        "explicit_parts": [HyundaiHarness.O],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_KONA_EV_2022"
    },
    "Hyundai Kona Hybrid 2020": {
        "make": "Hyundai",
        "model": "Kona Hybrid",
        "years": [2020],
        "package": "Smart Cruise Control (SCC)",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["scc"],
        "explicit_parts": [HyundaiHarness.I],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_KONA_HEV"
    },
    "Hyundai Ioniq 6 2023-24": {
        "make": "Hyundai",
        "model": "Ioniq 6",
        "years": [2023, 2024],
        "package": "Highway Driving Assist II",
        "requirements": "Highway Driving Assist II",
        "explicit_footnotes": ["canfd"],
        "explicit_parts": [HyundaiHarness.P],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_IONIQ_6"
    },
    "Hyundai Ioniq 5 2022-24": {
        "make": "Hyundai",
        "model": "Ioniq 5",
        "years": [2022, 2023, 2024],
        "package": "Highway Driving Assist II",
        "requirements": "Highway Driving Assist II",
        "explicit_footnotes": ["canfd"],
        "explicit_parts": [HyundaiHarness.Q],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_IONIQ_5"
    },
    "Hyundai Tucson 2022-24": {
        "make": "Hyundai",
        "model": "Tucson",
        "years": [2022, 2023, 2024],
        "package": "All",
        "requirements": "Smart Cruise Control",
        "explicit_footnotes": ["canfd"],
        "explicit_parts": [HyundaiHarness.N],
        "support_type": "upstream",
        "video_link": None,
        "min_steer_speed": 0.0,
        "min_enable_speed": 0.0,
        "auto_resume": True,
        "visible_in_docs": True,
        "platform": "HYUNDAI_TUCSON_4TH_GEN"
    },
}

# ===== HELPER FUNCTIONS =====

def get_model_data(model_id: str) -> Optional[Dict[str, Any]]:
    """Get the metadata for a specific model."""
    return MODEL_DATA.get(model_id)

def get_visible_models() -> List[str]:
    """Get a list of all models that should be visible in documentation."""
    return [model_id for model_id, data in MODEL_DATA.items() 
            if data.get("visible_in_docs", True)]

def get_model_by_platform(platform: str) -> Optional[str]:
    """Get the model ID for a specific platform."""
    for model_id, data in MODEL_DATA.items():
        if data.get("platform") == platform:
            return model_id
    return None

def get_part(part_enum) -> Part:
    """Get a Part object from a part enum value."""
    return part_enum.value.part

def get_part_dependencies(part_enum) -> List[Part]:
    """Get all dependencies for a part."""
    dependencies = PART_DEPENDENCIES.get(part_enum, [])
    return [dep.value.part for dep in dependencies]

def get_all_parts_for_model(explicit_parts: List[Any]) -> List[Part]:
    """Get all parts including dependencies for a model."""
    all_parts = []
    processed_parts = set()
    
    for part_enum in explicit_parts:
        if part_enum in processed_parts:
            continue
            
        part = get_part(part_enum)
        if part:
            all_parts.append(part)
            processed_parts.add(part_enum)
            
            # Add dependencies
            dependencies = PART_DEPENDENCIES.get(part_enum, [])
            
            for dep_enum in dependencies:
                if dep_enum not in processed_parts:
                    dep_part = get_part(dep_enum)
                    all_parts.append(dep_part)
                    processed_parts.add(dep_enum)
    
    return all_parts

def get_footnote(footnote_id: str) -> Optional[Footnote]:
    """Get a footnote by its ID."""
    return FOOTNOTES.get(footnote_id)

def get_footnotes_for_model(explicit_footnotes: List[str]) -> Dict[str, Footnote]:
    """Get all footnotes for a model."""
    return {footnote_id: FOOTNOTES[footnote_id] 
            for footnote_id in explicit_footnotes 
            if footnote_id in FOOTNOTES} 
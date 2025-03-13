"""
Static metadata attributes for Hyundai vehicles.

This module contains all the non-functional metadata for Hyundai vehicles,
including model information, parts, footnotes, and other documentation-related information.
"""

from typing import Dict, List, Optional, Any
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit, EnumBase, Category
from opendbc.metadata.base.footnotes import Footnote
from opendbc.metadata.base.constants import COLUMNS

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
        "explicit_parts": [Harness.HYUNDAI_B, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_G, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_K, Tool.PRY_TOOL, Kit.CANFD_KIT],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_A, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_A, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_B, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_O, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_O, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_I, Tool.PRY_TOOL],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_P, Tool.PRY_TOOL, Kit.CANFD_KIT],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_Q, Tool.PRY_TOOL, Kit.CANFD_KIT],  # Direct references
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
        "explicit_parts": [Harness.HYUNDAI_N, Tool.PRY_TOOL, Kit.CANFD_KIT],  # Direct references
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

def get_all_parts_for_model(explicit_parts: List[EnumBase]) -> List[EnumBase]:
    """Get all parts including dependencies for a model."""
    all_parts = []
    processed_parts = set()
    
    for part_enum in explicit_parts:
        if part_enum in processed_parts:
            continue
            
        all_parts.append(part_enum)
        processed_parts.add(part_enum)
        
        # Add dependencies through the all_parts() method
        for dep_part in part_enum.value.all_parts():
            if dep_part not in processed_parts:
                all_parts.append(dep_part)
                processed_parts.add(dep_part)
    
    return all_parts

def get_footnote(footnote_id: str) -> Optional[Footnote]:
    """Get a footnote by its ID."""
    return FOOTNOTES.get(footnote_id)

def get_footnotes_for_model(explicit_footnotes: List[str]) -> Dict[str, Footnote]:
    """Get all footnotes for a model."""
    return {footnote_id: FOOTNOTES[footnote_id] 
            for footnote_id in explicit_footnotes 
            if footnote_id in FOOTNOTES} 
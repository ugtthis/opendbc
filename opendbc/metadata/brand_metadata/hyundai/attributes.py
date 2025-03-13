"""
Static metadata attributes for Hyundai vehicles.

This module contains all the non-functional metadata for Hyundai vehicles,
including model information, parts, and other documentation-related information.
Footnotes have been moved to footnotes.py and helper functions to base/model_helpers.py.
"""

from typing import Dict, Any
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit

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
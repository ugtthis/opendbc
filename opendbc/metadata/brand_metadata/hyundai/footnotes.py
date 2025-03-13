"""
Hyundai-specific footnotes.

This module contains footnote definitions specific to Hyundai vehicles.
"""

from typing import Dict, List, Optional
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

def get_footnote(footnote_id: str) -> Optional[Footnote]:
    """Get a footnote by its ID."""
    return FOOTNOTES.get(footnote_id)

def get_footnotes_for_model(explicit_footnotes: List[str]) -> Dict[str, Footnote]:
    """Get all footnotes for a model."""
    return {footnote_id: FOOTNOTES[footnote_id] 
            for footnote_id in explicit_footnotes 
            if footnote_id in FOOTNOTES} 
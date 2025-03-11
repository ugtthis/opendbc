"""Tests for the Hyundai processor module."""

import pytest
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor
from opendbc.car.hyundai.values import Footnote as HyundaiFootnote, HyundaiFlags

def test_hyundai_processor_initialization():
    """Test initializing the Hyundai processor."""
    processor = HyundaiProcessor()
    
    # Check common parts initialization - only include harnesses actually used in values.py
    assert "harness_a" in processor.common_parts  # For 2020+ Sonata
    assert "harness_b" in processor.common_parts  # For older Elantra
    assert "harness_g" in processor.common_parts  # For 2019 Elantra
    assert "harness_k" in processor.common_parts  # For 2021+ Elantra
    
    # Check common tools initialization
    assert len(processor.common_tools) == 1
    assert processor.common_tools[0].name == "Trim Removal Tool"
    
    # Check common footnotes initialization - only include footnotes used by these models
    assert "scc" in processor.common_footnotes  # All models require SCC
    assert "min_speed" in processor.common_footnotes  # For MIN_STEER_32_MPH flag
    assert "radar_scc" in processor.common_footnotes  # For MANDO_RADAR flag
    
    # Verify footnote text matches values.py
    assert processor.common_footnotes["scc"].text == "Requires Smart Cruise Control (SCC)"

def test_process_elantra_2021():
    """Test processing a 2021 Elantra (K harness, CHECKSUM_CRC8 flag)."""
    processor = HyundaiProcessor()
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2021, 2022, 2023],
        platform="HYUNDAI_ELANTRA_2021"
    )
    processor.model_data["elantra_2021"] = model_data
    
    result = processor.process_model("elantra_2021")
    assert result == model_data
    
    # Check parts - should match HYUNDAI_ELANTRA_2021 config
    parts = processor.get_parts("elantra_2021")
    assert parts is not None
    assert len(parts.parts) == 1  # Only K harness, no CAN FD kit (no CANFD flag)
    assert parts.parts[0].name == "Hyundai K Harness"
    
    # Check footnotes - should have SCC but no min_speed (no MIN_STEER_32_MPH flag)
    footnotes = processor.get_footnotes("elantra_2021")
    assert footnotes is not None
    assert "scc" in footnotes.footnotes
    assert "min_speed" not in footnotes.footnotes

def test_process_elantra_2019():
    """Test processing a 2019 Elantra (G harness, MIN_STEER_32_MPH flag)."""
    processor = HyundaiProcessor()
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2019],
        platform="HYUNDAI_ELANTRA"
    )
    processor.model_data["elantra_2019"] = model_data
    
    result = processor.process_model("elantra_2019")
    assert result == model_data
    
    # Check parts - should match HYUNDAI_ELANTRA config
    parts = processor.get_parts("elantra_2019")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Hyundai G Harness"  # G harness for 2019
    
    # Check footnotes - should have both SCC and min_speed (has MIN_STEER_32_MPH flag)
    footnotes = processor.get_footnotes("elantra_2019")
    assert footnotes is not None
    assert "scc" in footnotes.footnotes
    assert "min_speed" in footnotes.footnotes

def test_process_sonata_2020():
    """Test processing a 2020 Sonata (A harness, MANDO_RADAR flag)."""
    processor = HyundaiProcessor()
    model_data = ModelData(
        make="Hyundai",
        model="Sonata",
        years=[2020],
        platform="HYUNDAI_SONATA"
    )
    processor.model_data["sonata_2020"] = model_data
    
    result = processor.process_model("sonata_2020")
    assert result == model_data
    
    # Check parts - should match HYUNDAI_SONATA config
    parts = processor.get_parts("sonata_2020")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Hyundai A Harness"  # A harness for 2020+ Sonata
    
    # Check footnotes - should have SCC and radar_scc (has MANDO_RADAR flag)
    footnotes = processor.get_footnotes("sonata_2020")
    assert footnotes is not None
    assert "scc" in footnotes.footnotes
    assert "radar_scc" in footnotes.footnotes
    assert "camera_scc" not in footnotes.footnotes  # Uses radar, not camera

def test_process_nonexistent_model():
    """Test processing a nonexistent model."""
    processor = HyundaiProcessor()
    result = processor.process_model("nonexistent")
    assert result is None
    assert processor.get_parts("nonexistent") is None
    assert processor.get_footnotes("nonexistent") is None 
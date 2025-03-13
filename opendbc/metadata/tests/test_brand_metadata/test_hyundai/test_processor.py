"""Tests for the Hyundai processor module."""

import pytest
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit
from opendbc.car.hyundai.values import Footnote as HyundaiFootnote, HyundaiFlags, CAR, HyundaiPlatformConfig

def test_hyundai_processor_initialization():
    """Test initializing the Hyundai processor."""
    processor = HyundaiProcessor()
    
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
    processor.model_data["Hyundai Elantra 2021-23"] = model_data
    
    result = processor.process_model("Hyundai Elantra 2021-23")
    assert result is not None
    assert result["make"] == "Hyundai"
    assert result["model"] == "Elantra"
    assert result["years"] == [2021, 2022, 2023]
    assert result["platform"] == "HYUNDAI_ELANTRA_2021"
    
    # Check parts - should match HYUNDAI_ELANTRA_2021 config
    parts = processor.get_parts("Hyundai Elantra 2021-23")
    assert parts is not None
    assert len(parts.parts) == 2  # K harness and CAN FD kit
    assert any(part.name == "Hyundai K connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    
    # Check footnotes - should have SCC but no min_speed (no MIN_STEER_32_MPH flag)
    footnotes = processor.get_footnotes("Hyundai Elantra 2021-23")
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
    processor.model_data["Hyundai Elantra 2019"] = model_data
    
    result = processor.process_model("Hyundai Elantra 2019")
    assert result is not None
    assert result["make"] == "Hyundai"
    assert result["model"] == "Elantra"
    assert result["years"] == [2019]
    assert result["platform"] == "HYUNDAI_ELANTRA"
    
    # Check parts - should match HYUNDAI_ELANTRA config
    parts = processor.get_parts("Hyundai Elantra 2019")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Hyundai G connector"  # G harness for 2019
    
    # Check footnotes - should have both SCC and min_speed (has MIN_STEER_32_MPH flag)
    footnotes = processor.get_footnotes("Hyundai Elantra 2019")
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
    processor.model_data["Hyundai Sonata 2020"] = model_data
    
    result = processor.process_model("Hyundai Sonata 2020")
    assert result is not None
    assert result["make"] == "Hyundai"
    assert result["model"] == "Sonata"
    assert result["years"] == [2020]
    assert result["platform"] == "HYUNDAI_SONATA"
    
    # Check parts - should match HYUNDAI_SONATA config
    parts = processor.get_parts("Hyundai Sonata 2020")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Hyundai A connector"  # A harness for 2020+ Sonata
    
    # Check footnotes - should have SCC and radar_scc (has MANDO_RADAR flag)
    footnotes = processor.get_footnotes("Hyundai Sonata 2020")
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

def test_required_parts():
    """Test that required parts are correctly included for models."""
    processor = HyundaiProcessor()
    
    # Test Elantra 2021-23 (should have K harness and CAN FD kit)
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2021, 2022, 2023],
        platform="HYUNDAI_ELANTRA_2021"
    )
    processor.model_data["Hyundai Elantra 2021-23"] = model_data
    processor.process_model("Hyundai Elantra 2021-23")
    parts = processor.get_parts("Hyundai Elantra 2021-23")
    
    assert parts is not None
    assert len(parts.parts) == 2
    assert any(part.name == "Hyundai K connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    assert any(part.name == "Pry Tool" for part in parts.tools)
    
    # Test Ioniq 6 (should have P harness and CAN FD kit)
    model_data = ModelData(
        make="Hyundai",
        model="Ioniq 6",
        years=[2023, 2024],
        platform="HYUNDAI_IONIQ_6"
    )
    processor.model_data["Hyundai Ioniq 6 2023-24"] = model_data
    processor.process_model("Hyundai Ioniq 6 2023-24")
    parts = processor.get_parts("Hyundai Ioniq 6 2023-24")
    
    assert parts is not None
    assert len(parts.parts) == 2
    assert any(part.name == "Hyundai P connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    assert any(part.name == "Pry Tool" for part in parts.tools)
    
    # Test Tucson (should have N harness and CAN FD kit)
    model_data = ModelData(
        make="Hyundai",
        model="Tucson",
        years=[2022, 2023, 2024],
        platform="HYUNDAI_TUCSON_4TH_GEN"
    )
    processor.model_data["Hyundai Tucson 2022-24"] = model_data
    processor.process_model("Hyundai Tucson 2022-24")
    parts = processor.get_parts("Hyundai Tucson 2022-24")
    
    assert parts is not None
    assert len(parts.parts) == 2
    assert any(part.name == "Hyundai N connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    assert any(part.name == "Pry Tool" for part in parts.tools)

def test_get_model_by_platform():
    """Test getting a model by platform."""
    processor = HyundaiProcessor()
    
    # Add some models
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2021, 2022, 2023],
        platform="HYUNDAI_ELANTRA_2021"
    )
    processor.model_data["Hyundai Elantra 2021-23"] = model_data
    
    model_data = ModelData(
        make="Hyundai",
        model="Sonata",
        years=[2020],
        platform="HYUNDAI_SONATA"
    )
    processor.model_data["Hyundai Sonata 2020"] = model_data
    
    # Test getting models by platform
    assert processor.get_model_by_platform("HYUNDAI_ELANTRA_2021") == "Hyundai Elantra 2021-23"
    assert processor.get_model_by_platform("HYUNDAI_SONATA") == "Hyundai Sonata 2020"
    assert processor.get_model_by_platform("NONEXISTENT") is None

def test_year_format():
    """Test that year ranges are formatted correctly."""
    processor = HyundaiProcessor()
    
    # Single year
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2019],
        platform="HYUNDAI_ELANTRA"
    )
    processor.model_data["Hyundai Elantra 2019"] = model_data
    result = processor.process_model("Hyundai Elantra 2019")
    assert result["years"] == [2019]
    
    # Year range
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2021, 2022, 2023],
        platform="HYUNDAI_ELANTRA_2021"
    )
    processor.model_data["Hyundai Elantra 2021-23"] = model_data
    result = processor.process_model("Hyundai Elantra 2021-23")
    assert result["years"] == [2021, 2022, 2023]

def test_get_visible_models():
    """Test getting visible models."""
    processor = HyundaiProcessor()
    
    # Add some models with visibility settings
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2021, 2022, 2023],
        platform="HYUNDAI_ELANTRA_2021"
    )
    processor.model_data["Hyundai Elantra 2021-23"] = model_data
    
    model_data = ModelData(
        make="Hyundai",
        model="Sonata",
        years=[2020],
        platform="HYUNDAI_SONATA"
    )
    processor.model_data["Hyundai Sonata 2020"] = model_data
    
    # Test getting visible models
    visible_models = processor.get_visible_models()
    assert "Hyundai Elantra 2021-23" in visible_models
    assert "Hyundai Sonata 2020" in visible_models 
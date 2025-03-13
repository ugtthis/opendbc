"""Tests for the Hyundai processor module."""

import pytest
from unittest.mock import patch
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

@patch.object(HyundaiProcessor, 'get_model_data')
def test_process_elantra_2021(mock_get_model_data):
    """Test processing a 2021 Elantra (K harness)."""
    model_data = {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2021, 2022, 2023],
        "platform": "HYUNDAI_ELANTRA_2021",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_K"],
        "explicit_footnotes": ["scc"]
    }
    mock_get_model_data.return_value = model_data
    
    processor = HyundaiProcessor()
    result = processor.process_model("Hyundai Elantra 2021-23")
    assert result is not None
    assert result["make"] == "Hyundai"
    assert result["model"] == "Elantra"
    assert result["years"] == [2021, 2022, 2023]
    assert result["platform"] == "HYUNDAI_ELANTRA_2021"
    
    # Check parts - should match HYUNDAI_ELANTRA_2021 config
    parts = processor.get_parts("Hyundai Elantra 2021-23")
    assert parts is not None
    assert len(parts.parts) == 1  # K harness only
    assert parts.parts[0].name == "Hyundai K connector"
    
    # Check footnotes - should have SCC but no min_speed (no MIN_STEER_32_MPH flag)
    footnotes = processor.get_footnotes("Hyundai Elantra 2021-23")
    assert footnotes is not None
    assert "scc" in footnotes.footnotes
    assert "min_speed" not in footnotes.footnotes

@patch.object(HyundaiProcessor, 'get_model_data')
def test_process_elantra_2019(mock_get_model_data):
    """Test processing a 2019 Elantra (G harness, MIN_STEER_32_MPH flag)."""
    model_data = {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2019],
        "platform": "HYUNDAI_ELANTRA",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_G"],
        "explicit_footnotes": ["scc", "min_speed"]
    }
    mock_get_model_data.return_value = model_data
    
    processor = HyundaiProcessor()
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

@patch.object(HyundaiProcessor, 'get_model_data')
def test_process_sonata_2020(mock_get_model_data):
    """Test processing a 2020 Sonata (A harness, MANDO_RADAR flag)."""
    model_data = {
        "make": "Hyundai",
        "model": "Sonata",
        "years": [2020, 2021, 2022, 2023],
        "platform": "HYUNDAI_SONATA",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_A"],
        "explicit_footnotes": ["scc", "radar_scc"]
    }
    mock_get_model_data.return_value = model_data
    
    processor = HyundaiProcessor()
    result = processor.process_model("Hyundai Sonata 2020-23")
    assert result is not None
    assert result["make"] == "Hyundai"
    assert result["model"] == "Sonata"
    assert result["years"] == [2020, 2021, 2022, 2023]
    assert result["platform"] == "HYUNDAI_SONATA"
    
    # Check parts - should match HYUNDAI_SONATA config
    parts = processor.get_parts("Hyundai Sonata 2020-23")
    assert parts is not None
    assert len(parts.parts) == 1  # A harness only
    assert parts.parts[0].name == "Hyundai A connector"
    
    # Check footnotes - should have SCC, radar_scc (MANDO_RADAR flag)
    footnotes = processor.get_footnotes("Hyundai Sonata 2020-23")
    assert footnotes is not None
    assert "scc" in footnotes.footnotes
    assert "radar_scc" in footnotes.footnotes
    assert "canfd" not in footnotes.footnotes  # Uses radar, not camera

def test_process_nonexistent_model():
    """Test processing a nonexistent model."""
    processor = HyundaiProcessor()
    result = processor.process_model("nonexistent")
    assert result is None
    assert processor.get_parts("nonexistent") is None
    assert processor.get_footnotes("nonexistent") is None

@patch.object(HyundaiProcessor, 'get_model_data')
def test_required_parts(mock_get_model_data):
    """Test that required parts are correctly included for models."""
    processor = HyundaiProcessor()
    
    # Test Ioniq 5 (should have Q harness and CAN FD kit)
    model_data = {
        "make": "Hyundai",
        "model": "Ioniq 5",
        "years": [2022, 2023, 2024],
        "platform": "HYUNDAI_IONIQ_5",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_Q"],
        "explicit_footnotes": ["scc"]
    }
    mock_get_model_data.return_value = model_data
    
    result = processor.process_model("Hyundai Ioniq 5 2022-24")
    parts = processor.get_parts("Hyundai Ioniq 5 2022-24")
    
    assert parts is not None
    assert len(parts.parts) == 2
    assert any(part.name == "Hyundai Q connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    assert any(part.name == "Pry Tool" for part in parts.tools)
    
    # Test Ioniq 6 (should have P harness and CAN FD kit)
    model_data = {
        "make": "Hyundai",
        "model": "Ioniq 6",
        "years": [2023, 2024],
        "platform": "HYUNDAI_IONIQ_6",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_P"],
        "explicit_footnotes": ["scc"]
    }
    mock_get_model_data.return_value = model_data
    
    result = processor.process_model("Hyundai Ioniq 6 2023-24")
    parts = processor.get_parts("Hyundai Ioniq 6 2023-24")
    
    assert parts is not None
    assert len(parts.parts) == 2
    assert any(part.name == "Hyundai P connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    assert any(part.name == "Pry Tool" for part in parts.tools)
    
    # Test Tucson (should have N harness and CAN FD kit)
    model_data = {
        "make": "Hyundai",
        "model": "Tucson",
        "years": [2022, 2023, 2024],
        "platform": "HYUNDAI_TUCSON_4TH_GEN",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_N"],
        "explicit_footnotes": ["scc"]
    }
    mock_get_model_data.return_value = model_data
    
    result = processor.process_model("Hyundai Tucson 2022-24")
    parts = processor.get_parts("Hyundai Tucson 2022-24")
    
    assert parts is not None
    assert len(parts.parts) == 2
    assert any(part.name == "Hyundai N connector" for part in parts.parts)
    assert any(part.name == "CAN FD panda kit" for part in parts.parts)
    assert any(part.name == "Pry Tool" for part in parts.tools)

@patch.object(HyundaiProcessor, 'get_model_data')
def test_get_model_by_platform(mock_get_model_data):
    """Test getting a model by platform."""
    from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
    
    # Mock the base_get_model_by_platform function
    with patch('opendbc.metadata.brand_metadata.hyundai.processor.base_get_model_by_platform') as mock_base:
        mock_base.return_value = "Hyundai Elantra 2021-23"
        
        processor = HyundaiProcessor()
        assert processor.get_model_by_platform("HYUNDAI_ELANTRA_2021") == "Hyundai Elantra 2021-23"
        mock_base.assert_called_once_with(MODEL_DATA, "HYUNDAI_ELANTRA_2021")

@patch.object(HyundaiProcessor, 'get_model_data')
def test_year_format(mock_get_model_data):
    """Test that year ranges are formatted correctly."""
    # Single year
    model_data_single = {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2019],
        "platform": "HYUNDAI_ELANTRA",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_G"],
        "explicit_footnotes": ["scc", "min_speed"]
    }
    mock_get_model_data.return_value = model_data_single
    
    processor = HyundaiProcessor()
    result = processor.process_model("Hyundai Elantra 2019")
    assert result["years"] == [2019]
    
    # Year range
    model_data_range = {
        "make": "Hyundai",
        "model": "Elantra",
        "years": [2021, 2022, 2023],
        "platform": "HYUNDAI_ELANTRA_2021",
        "package": "All",
        "explicit_parts": ["Harness.HYUNDAI_K"],
        "explicit_footnotes": ["scc"]
    }
    mock_get_model_data.return_value = model_data_range
    
    result = processor.process_model("Hyundai Elantra 2021-23")
    assert result["years"] == [2021, 2022, 2023]

@patch.object(HyundaiProcessor, 'get_model_data')
def test_get_visible_models(mock_get_model_data):
    """Test getting visible models."""
    from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
    
    # Mock the base_get_visible_models function
    with patch('opendbc.metadata.brand_metadata.hyundai.processor.base_get_visible_models') as mock_base:
        mock_base.return_value = ["Hyundai Elantra 2021-23", "Hyundai Sonata 2020-23"]
        
        processor = HyundaiProcessor()
        visible_models = processor.get_visible_models()
        assert "Hyundai Elantra 2021-23" in visible_models
        assert "Hyundai Sonata 2020-23" in visible_models
        mock_base.assert_called_once_with(MODEL_DATA) 
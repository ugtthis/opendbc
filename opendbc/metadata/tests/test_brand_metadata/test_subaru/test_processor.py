"""Tests for the Subaru processor module."""

import pytest
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor

def test_subaru_processor_initialization():
    """Test initializing the Subaru processor."""
    processor = SubaruProcessor()
    
    # Check common parts initialization
    assert "harness_a" in processor.common_parts
    assert "harness_b" in processor.common_parts
    assert "harness_c" in processor.common_parts
    assert "harness_d" in processor.common_parts
    
    # Check common tools initialization
    assert len(processor.common_tools) == 2
    assert any(tool.name == "Socket 8mm Deep" for tool in processor.common_tools)
    assert any(tool.name == "Trim Removal Tool" for tool in processor.common_tools)
    
    # Check common footnotes initialization
    assert "eyesight" in processor.common_footnotes
    assert "angle_lkas" in processor.common_footnotes
    assert "torque_lkas" in processor.common_footnotes

def test_process_outback_2020():
    """Test processing a 2020-22 Outback (harness B)."""
    processor = SubaruProcessor()
    model_data = ModelData(
        make="Subaru",
        model="Outback",
        years=[2020, 2021, 2022],
        platform="SUBARU_OUTBACK"
    )
    processor.model_data["outback_2020"] = model_data
    
    result = processor.process_model("outback_2020")
    assert result == model_data
    
    # Check parts
    parts = processor.get_parts("outback_2020")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Subaru B Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("outback_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses torque-based Lane Keep Assist System"

def test_process_forester_2022():
    """Test processing a 2022-24 Forester (harness C, angle LKAS)."""
    processor = SubaruProcessor()
    model_data = ModelData(
        make="Subaru",
        model="Forester",
        years=[2022, 2023, 2024],
        platform="SUBARU_FORESTER_2022"
    )
    processor.model_data["forester_2022"] = model_data
    
    result = processor.process_model("forester_2022")
    assert result == model_data
    
    # Check parts
    parts = processor.get_parts("forester_2022")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Subaru C Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("forester_2022")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses angle-based Lane Keep Assist System"

def test_process_outback_2023():
    """Test processing a 2023 Outback (harness D, angle LKAS)."""
    processor = SubaruProcessor()
    model_data = ModelData(
        make="Subaru",
        model="Outback",
        years=[2023],
        platform="SUBARU_OUTBACK_2023"
    )
    processor.model_data["outback_2023"] = model_data
    
    result = processor.process_model("outback_2023")
    assert result == model_data
    
    # Check parts
    parts = processor.get_parts("outback_2023")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Subaru D Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("outback_2023")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses angle-based Lane Keep Assist System"

def test_process_crosstrek_hybrid_2020():
    """Test processing a 2020 Crosstrek Hybrid (harness B)."""
    processor = SubaruProcessor()
    model_data = ModelData(
        make="Subaru",
        model="Crosstrek",
        years=[2020],
        platform="SUBARU_CROSSTREK_HYBRID"
    )
    processor.model_data["crosstrek_hybrid_2020"] = model_data
    
    result = processor.process_model("crosstrek_hybrid_2020")
    assert result == model_data
    
    # Check parts
    parts = processor.get_parts("crosstrek_hybrid_2020")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Subaru B Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("crosstrek_hybrid_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses torque-based Lane Keep Assist System"

def test_process_impreza_2019():
    """Test processing a 2019 Impreza (harness A)."""
    processor = SubaruProcessor()
    model_data = ModelData(
        make="Subaru",
        model="Impreza",
        years=[2019],
        platform="SUBARU_IMPREZA"
    )
    processor.model_data["impreza_2019"] = model_data
    
    result = processor.process_model("impreza_2019")
    assert result == model_data
    
    # Check parts
    parts = processor.get_parts("impreza_2019")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == "Subaru A Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("impreza_2019")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses torque-based Lane Keep Assist System"

def test_process_nonexistent_model():
    """Test processing a nonexistent model."""
    processor = SubaruProcessor()
    result = processor.process_model("nonexistent")
    assert result is None
    assert processor.get_parts("nonexistent") is None
    assert processor.get_footnotes("nonexistent") is None

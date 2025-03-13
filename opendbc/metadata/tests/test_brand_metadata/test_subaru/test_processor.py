"""Tests for the Subaru processor module."""

import pytest
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor
from opendbc.car.subaru.values import Footnote as SubaruFootnote, SubaruFlags, CAR, SubaruPlatformConfig
from opendbc.metadata.base.parts_definitions import Harness, Tool

def test_subaru_processor_initialization():
    """Test initializing the Subaru processor."""
    processor = SubaruProcessor()
    
    # Check common footnotes initialization
    assert "eyesight" in processor.common_footnotes
    assert "angle_lkas" in processor.common_footnotes
    assert "torque_lkas" in processor.common_footnotes
    assert "steer_rate" in processor.common_footnotes
    assert "global" in processor.common_footnotes
    assert "exp_long" in processor.common_footnotes
    
    # Verify footnote text matches values.py
    assert processor.common_footnotes["global"].text == SubaruFootnote.GLOBAL.value.text
    assert processor.common_footnotes["exp_long"].text == SubaruFootnote.EXP_LONG.value.text
    assert processor.common_footnotes["steer_rate"].text == "Vehicle may temporarily fault when steering angle rate exceeds threshold"

def test_process_outback_2020():
    """Test processing a 2020-22 Outback (harness B, steer rate limited)."""
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
    assert parts.parts[0].name == Harness.SUBARU_B.name
    
    # Check footnotes
    footnotes = processor.get_footnotes("outback_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "torque_lkas" in footnotes.footnotes
    assert "steer_rate" in footnotes.footnotes

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
    assert parts.parts[0].name == Harness.SUBARU_C.name
    
    # Check footnotes
    footnotes = processor.get_footnotes("forester_2022")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "angle_lkas" in footnotes.footnotes

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
    assert parts.parts[0].name == Harness.SUBARU_D.name
    
    # Check footnotes
    footnotes = processor.get_footnotes("outback_2023")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "angle_lkas" in footnotes.footnotes

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
    assert parts.parts[0].name == Harness.SUBARU_B.name
    
    # Check footnotes
    footnotes = processor.get_footnotes("crosstrek_hybrid_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "torque_lkas" in footnotes.footnotes

def test_process_impreza_2020():
    """Test processing a 2020 Impreza (harness A, steer rate limited)."""
    processor = SubaruProcessor()
    model_data = ModelData(
        make="Subaru",
        model="Impreza",
        years=[2020],
        platform="SUBARU_IMPREZA_2020"
    )
    processor.model_data["impreza_2020"] = model_data
    
    result = processor.process_model("impreza_2020")
    assert result == model_data
    
    # Check parts
    parts = processor.get_parts("impreza_2020")
    assert parts is not None
    assert len(parts.parts) == 1
    assert parts.parts[0].name == Harness.SUBARU_A.name
    
    # Check footnotes
    footnotes = processor.get_footnotes("impreza_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "torque_lkas" in footnotes.footnotes
    assert "steer_rate" in footnotes.footnotes

def test_process_nonexistent_model():
    """Test processing a nonexistent model."""
    processor = SubaruProcessor()
    result = processor.process_model("nonexistent")
    assert result is None
    assert processor.get_parts("nonexistent") is None
    assert processor.get_footnotes("nonexistent") is None

def test_tools_always_included():
    """Test that required tools are always included."""
    processor = SubaruProcessor()
    
    # Set up test model data
    model_data = ModelData(
        make="Subaru",
        model="Outback",
        years=[2020, 2021, 2022],
        platform="SUBARU_OUTBACK"
    )
    processor.model_data["outback_2020"] = model_data
    
    # Process the model
    processor.process_model("outback_2020")
    
    # Get parts for the model
    parts = processor.get_parts("outback_2020")
    
    # Check that the tools match the expected values
    assert parts is not None
    assert len(parts.tools) == 2
    assert any(tool.name == Tool.SOCKET_8MM_DEEP.name for tool in parts.tools)
    assert any(tool.name == Tool.PRY_TOOL.name for tool in parts.tools)

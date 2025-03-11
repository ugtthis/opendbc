"""Tests for the Subaru processor module."""

import pytest
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor
from opendbc.car.subaru.values import Footnote as SubaruFootnote, SubaruFlags, CAR, SubaruPlatformConfig
from opendbc.metadata.brand_metadata.subaru.processor import SubaruPartProcessor

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
    assert parts.parts[0].name == "Subaru B Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("outback_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "steer_rate" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses torque-based Lane Keep Assist System"
    assert footnotes.footnotes["global"].text == SubaruFootnote.GLOBAL.value.text
    assert footnotes.footnotes["steer_rate"].text == "Vehicle may temporarily fault when steering angle rate exceeds threshold"

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
    assert "global" in footnotes.footnotes
    assert "steer_rate" not in footnotes.footnotes  # Angle-based LKAS doesn't have steer rate limit
    assert footnotes.footnotes["lkas"].text == "Uses angle-based Lane Keep Assist System"
    assert footnotes.footnotes["global"].text == SubaruFootnote.GLOBAL.value.text

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
    assert "global" in footnotes.footnotes
    assert "steer_rate" not in footnotes.footnotes  # Angle-based LKAS doesn't have steer rate limit
    assert footnotes.footnotes["lkas"].text == "Uses angle-based Lane Keep Assist System"
    assert footnotes.footnotes["global"].text == SubaruFootnote.GLOBAL.value.text

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
    assert "global" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses torque-based Lane Keep Assist System"
    assert footnotes.footnotes["global"].text == SubaruFootnote.GLOBAL.value.text

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
    assert parts.parts[0].name == "Subaru A Harness"
    
    # Check footnotes
    footnotes = processor.get_footnotes("impreza_2020")
    assert footnotes is not None
    assert "eyesight" in footnotes.footnotes
    assert "lkas" in footnotes.footnotes
    assert "global" in footnotes.footnotes
    assert "steer_rate" in footnotes.footnotes
    assert footnotes.footnotes["lkas"].text == "Uses torque-based Lane Keep Assist System"
    assert footnotes.footnotes["global"].text == SubaruFootnote.GLOBAL.value.text
    assert footnotes.footnotes["steer_rate"].text == "Vehicle may temporarily fault when steering angle rate exceeds threshold"

def test_process_nonexistent_model():
    """Test processing a nonexistent model."""
    processor = SubaruProcessor()
    result = processor.process_model("nonexistent")
    assert result is None
    assert processor.get_parts("nonexistent") is None
    assert processor.get_footnotes("nonexistent") is None

def test_subaru_parts_exact_match():
    """Test that parts EXACTLY match values.py configurations."""
    processor = SubaruPartProcessor()
    
    # Test every car in values.py
    for car in CAR:
        if not isinstance(car.config, SubaruPlatformConfig):
            continue
            
        parts = processor.get_parts_for_platform(car.config)
        
        # Verify harness matches flags
        if car in [CAR.SUBARU_OUTBACK_2023, CAR.SUBARU_ASCENT_2023]:
            assert processor.HARNESS_D in parts.required_parts, \
                f"{car} should use Harness D"
        elif car == CAR.SUBARU_FORESTER_2022:
            assert processor.HARNESS_C in parts.required_parts, \
                f"{car} should use Harness C"
        elif car.config.flags & SubaruFlags.GLOBAL_GEN2 and not (car.config.flags & SubaruFlags.LKAS_ANGLE):
            assert processor.HARNESS_B in parts.required_parts, \
                f"{car} should use Harness B"
        else:
            assert processor.HARNESS_A in parts.required_parts, \
                f"{car} should use Harness A"
        
        # All should have tools
        assert processor.SOCKET_8MM in parts.tools
        assert processor.PRY_TOOL in parts.tools

def test_subaru_specific_models():
    """Test specific model configurations."""
    processor = SubaruPartProcessor()
    
    # Test Outback 2023
    outback = next(c for c in CAR if c.name == "SUBARU_OUTBACK_2023")
    parts = processor.get_parts_for_platform(outback.config)
    assert processor.HARNESS_D in parts.required_parts
    
    # Test Forester 2022
    forester = next(c for c in CAR if c.name == "SUBARU_FORESTER_2022")
    parts = processor.get_parts_for_platform(forester.config)
    assert processor.HARNESS_C in parts.required_parts
    
    # Test Global Platform
    global_car = next(c for c in CAR if c.name == "SUBARU_OUTBACK")
    parts = processor.get_parts_for_platform(global_car.config)
    assert processor.HARNESS_B in parts.required_parts
    
    # Test Pre-Global
    preglobal = next(c for c in CAR if c.name == "SUBARU_FORESTER_PREGLOBAL")
    parts = processor.get_parts_for_platform(preglobal.config)
    assert processor.HARNESS_A in parts.required_parts

def test_tools_always_included():
    """Test that required tools are always included."""
    processor = SubaruPartProcessor()
    
    for car in CAR:
        if not isinstance(car.config, SubaruPlatformConfig):
            continue
            
        parts = processor.get_parts_for_platform(car.config)
        assert processor.SOCKET_8MM in parts.tools, \
            f"{car} missing socket"
        assert processor.PRY_TOOL in parts.tools, \
            f"{car} missing pry tool"

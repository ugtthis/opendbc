"""Tests for the integration of brand processors with the parts catalog."""

import pytest
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit

def test_subaru_processor_uses_parts_catalog():
    """Test that the Subaru processor uses the enum-based parts system."""
    processor = SubaruProcessor()
    
    # Set up test model data for different Subaru models
    outback_2020 = ModelData(
        make="Subaru",
        model="Outback",
        years=[2020, 2021, 2022],
        platform="SUBARU_OUTBACK"
    )
    processor.model_data["outback_2020"] = outback_2020
    
    forester_2022 = ModelData(
        make="Subaru",
        model="Forester",
        years=[2022, 2023, 2024],
        platform="SUBARU_FORESTER_2022"
    )
    processor.model_data["forester_2022"] = forester_2022
    
    outback_2023 = ModelData(
        make="Subaru",
        model="Outback",
        years=[2023],
        platform="SUBARU_OUTBACK_2023"
    )
    processor.model_data["outback_2023"] = outback_2023
    
    # Process the models
    processor.process_model("outback_2020")
    processor.process_model("forester_2022")
    processor.process_model("outback_2023")
    
    # Check that the parts match the expected values
    outback_2020_parts = processor.get_parts("outback_2020")
    assert outback_2020_parts is not None
    assert any(part.name == Harness.SUBARU_B.name for part in outback_2020_parts.parts)
    
    forester_2022_parts = processor.get_parts("forester_2022")
    assert forester_2022_parts is not None
    assert any(part.name == Harness.SUBARU_C.name for part in forester_2022_parts.parts)
    
    outback_2023_parts = processor.get_parts("outback_2023")
    assert outback_2023_parts is not None
    assert any(part.name == Harness.SUBARU_D.name for part in outback_2023_parts.parts)
    
    # Check that all models have the required tools
    for parts in [outback_2020_parts, forester_2022_parts, outback_2023_parts]:
        assert any(tool.name == Tool.SOCKET_8MM_DEEP.name for tool in parts.tools)
        assert any(tool.name == Tool.PRY_TOOL.name for tool in parts.tools)

def test_hyundai_processor_uses_parts_catalog():
    """Test that the Hyundai processor uses the enum-based parts system."""
    processor = HyundaiProcessor()
    
    # Set up test model data
    model_data = ModelData(
        make="Hyundai",
        model="Elantra",
        years=[2021, 2022, 2023],
        platform="HYUNDAI_ELANTRA_2021"
    )
    processor.model_data["Hyundai Elantra 2021-23"] = model_data
    
    # Process the model
    processor.process_model("Hyundai Elantra 2021-23")
    
    # Get parts for the model
    parts = processor.get_parts("Hyundai Elantra 2021-23")
    
    # Check that the parts match the expected values
    assert parts is not None
    assert len(parts.parts) == 2  # K harness and CAN FD kit
    
    # Check harness
    assert any(part.name == Harness.HYUNDAI_K.name for part in parts.parts)
    
    # Check CAN FD kit
    assert any(part.name == Kit.CANFD_KIT.name for part in parts.parts)
    
    # Check pry tool
    assert any(part.name == Tool.PRY_TOOL.name for part in parts.tools) 
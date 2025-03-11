"""Tests for the integration of brand processors with the parts catalog."""

import pytest
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor
from opendbc.metadata.base.parts_catalog import PartsCatalog, HarnessId, ToolId
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.hyundai.attributes import HyundaiHarness, HyundaiTool, HyundaiKit, get_part

def test_subaru_processor_uses_parts_catalog():
    """Test that the Subaru processor uses the parts catalog."""
    processor = SubaruProcessor()
    
    # Check that the processor uses parts from the catalog
    assert processor.common_parts["harness_a"] is PartsCatalog.get_harness(HarnessId.SUBARU_A)
    assert processor.common_parts["harness_b"] is PartsCatalog.get_harness(HarnessId.SUBARU_B)
    assert processor.common_parts["harness_c"] is PartsCatalog.get_harness(HarnessId.SUBARU_C)
    assert processor.common_parts["harness_d"] is PartsCatalog.get_harness(HarnessId.SUBARU_D)
    
    # Check that the processor uses tools from the catalog
    assert processor.common_tools[0] is PartsCatalog.get_tool(ToolId.SOCKET_8MM_DEEP)
    assert processor.common_tools[1] is PartsCatalog.get_tool(ToolId.PRY_TOOL)

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
    k_harness = get_part(HyundaiHarness.K)
    assert any(part.id == k_harness.id for part in parts.parts)
    
    # Check CAN FD kit
    canfd_kit = get_part(HyundaiKit.CANFD_KIT)
    assert any(part.id == canfd_kit.id for part in parts.parts)
    
    # Check pry tool
    pry_tool = get_part(HyundaiTool.PRY_TOOL)
    assert any(part.id == pry_tool.id for part in parts.tools) 
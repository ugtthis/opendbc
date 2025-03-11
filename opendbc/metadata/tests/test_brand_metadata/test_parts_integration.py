"""Tests for the integration of brand processors with the parts catalog."""

import pytest
from opendbc.metadata.brand_metadata.subaru.processor import SubaruProcessor
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor
from opendbc.metadata.base.parts_catalog import PartsCatalog, HarnessId, ToolId

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
    """Test that the Hyundai processor uses the parts catalog."""
    processor = HyundaiProcessor()
    
    # Check that the processor uses parts from the catalog
    assert processor.common_parts["harness_a"] is PartsCatalog.get_harness(HarnessId.HYUNDAI_A)
    assert processor.common_parts["harness_b"] is PartsCatalog.get_harness(HarnessId.HYUNDAI_B)
    
    # Check that the processor uses tools from the catalog
    assert processor.common_tools[0] is PartsCatalog.get_tool(ToolId.PRY_TOOL) 
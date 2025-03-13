"""
Tests for the parts definitions system.

This module tests that the parts definitions match exactly with docs_definitions.py.
"""

import pytest
from opendbc.metadata.base.parts_definitions import Harness, Tool, Kit, Accessory
from opendbc.car.docs_definitions import CarHarness, Tool as DocsToolEnum

def test_harness_names_match_docs_definitions():
    """Test that harness names match exactly with docs_definitions.py."""
    # Test Hyundai harnesses
    assert Harness.HYUNDAI_A.name == CarHarness.hyundai_a.value.name
    assert Harness.HYUNDAI_B.name == CarHarness.hyundai_b.value.name
    assert Harness.HYUNDAI_C.name == CarHarness.hyundai_c.value.name
    assert Harness.HYUNDAI_D.name == CarHarness.hyundai_d.value.name
    assert Harness.HYUNDAI_E.name == CarHarness.hyundai_e.value.name
    assert Harness.HYUNDAI_F.name == CarHarness.hyundai_f.value.name
    assert Harness.HYUNDAI_G.name == CarHarness.hyundai_g.value.name
    assert Harness.HYUNDAI_H.name == CarHarness.hyundai_h.value.name
    assert Harness.HYUNDAI_I.name == CarHarness.hyundai_i.value.name
    assert Harness.HYUNDAI_J.name == CarHarness.hyundai_j.value.name
    assert Harness.HYUNDAI_K.name == CarHarness.hyundai_k.value.name
    assert Harness.HYUNDAI_L.name == CarHarness.hyundai_l.value.name
    assert Harness.HYUNDAI_M.name == CarHarness.hyundai_m.value.name
    assert Harness.HYUNDAI_N.name == CarHarness.hyundai_n.value.name
    assert Harness.HYUNDAI_O.name == CarHarness.hyundai_o.value.name
    assert Harness.HYUNDAI_P.name == CarHarness.hyundai_p.value.name
    assert Harness.HYUNDAI_Q.name == CarHarness.hyundai_q.value.name
    assert Harness.HYUNDAI_R.name == CarHarness.hyundai_r.value.name
    
    # Test Honda harnesses
    assert Harness.HONDA_NIDEC.name == CarHarness.nidec.value.name
    assert Harness.HONDA_BOSCH_A.name == CarHarness.bosch_a.value.name
    assert Harness.HONDA_BOSCH_B.name == CarHarness.bosch_b.value.name
    assert Harness.HONDA_BOSCH_C.name == CarHarness.bosch_c.value.name
    
    # Test Toyota harnesses
    assert Harness.TOYOTA_A.name == CarHarness.toyota_a.value.name
    assert Harness.TOYOTA_B.name == CarHarness.toyota_b.value.name
    
    # Test Subaru harnesses
    assert Harness.SUBARU_A.name == CarHarness.subaru_a.value.name
    assert Harness.SUBARU_B.name == CarHarness.subaru_b.value.name
    assert Harness.SUBARU_C.name == CarHarness.subaru_c.value.name
    assert Harness.SUBARU_D.name == CarHarness.subaru_d.value.name

def test_tool_names_match_docs_definitions():
    """Test that tool names match exactly with docs_definitions.py."""
    assert Tool.PRY_TOOL.name == DocsToolEnum.pry_tool.value.name
    assert Tool.SOCKET_8MM_DEEP.name == DocsToolEnum.socket_8mm_deep.value.name

def test_kit_canfd_name_matches_docs_definitions():
    """Test that the CAN FD kit name matches docs_definitions.py."""
    from opendbc.car.docs_definitions import Kit as DocsKitEnum
    assert Kit.CANFD_KIT.name == DocsKitEnum.red_panda_kit.value.name 
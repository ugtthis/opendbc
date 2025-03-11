"""Tests for the Hyundai processor module."""

import pytest
from opendbc.metadata.base.processor import ModelData
from opendbc.metadata.brand_metadata.hyundai.processor import HyundaiProcessor, HyundaiPartProcessor
from opendbc.car.hyundai.values import Footnote as HyundaiFootnote, HyundaiFlags, CAR, HyundaiPlatformConfig

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

def test_hyundai_parts_exact_match():
    """Test that parts EXACTLY match values.py configurations."""
    processor = HyundaiPartProcessor()
    
    # Test every car in values.py
    for car in CAR:
        if not isinstance(car.config, HyundaiPlatformConfig):
            continue
            
        parts = processor.get_parts_for_platform(car.config)
        
        # Verify harness matches flags and model
        if car.config.flags & HyundaiFlags.CANFD:
            if "IONIQ_6" in car.name and "HDA II" in car.config.car_docs[0].package:
                assert processor.HARNESS_P in parts.required_parts, \
                    f"{car} should use Harness P"
            elif "IONIQ_5" in car.name and "HDA II" in car.config.car_docs[0].package:
                assert processor.HARNESS_Q in parts.required_parts, \
                    f"{car} should use Harness Q"
            elif "TUCSON" in car.name or "SANTA_CRUZ" in car.name:
                assert processor.HARNESS_N in parts.required_parts, \
                    f"{car} should use Harness N"
            elif "GENESIS" in car.name or "STARIA" in car.name:
                assert processor.HARNESS_K in parts.required_parts, \
                    f"{car} should use Harness K"
            else:
                assert processor.HARNESS_L in parts.required_parts, \
                    f"{car} should use Harness L"
        elif car.config.flags & HyundaiFlags.LEGACY:
            assert processor.HARNESS_E in parts.required_parts, \
                f"{car} should use Harness E"
        elif car.config.flags & HyundaiFlags.UNSUPPORTED_LONGITUDINAL:
            assert processor.HARNESS_G in parts.required_parts, \
                f"{car} should use Harness G"
        elif car.name == "HYUNDAI_SONATA_HYBRID":
            # Special case: Sonata Hybrid uses Harness A despite having MANDO_RADAR and HYBRID flags
            assert processor.HARNESS_A in parts.required_parts, \
                f"{car} should use Harness A"
        elif "KONA" in car.name and any(year in car.config.car_docs[0].name for year in ["2022", "2023"]):
            # Special case: All 2022-23 Kona models (including EV) use Harness O
            assert processor.HARNESS_O in parts.required_parts, \
                f"{car} should use Harness O"
        elif car.name == "HYUNDAI_KONA_HEV":
            # Special case: Kona Hybrid 2020 uses Harness I
            assert processor.HARNESS_I in parts.required_parts, \
                f"{car} should use Harness I"
        elif car.config.flags & HyundaiFlags.MANDO_RADAR:
            assert processor.HARNESS_D in parts.required_parts, \
                f"{car} should use Harness D"
        elif car.config.flags & (HyundaiFlags.HYBRID | HyundaiFlags.EV):
            if "IONIQ" in car.name or "2020" in car.config.car_docs[0].name:
                assert processor.HARNESS_H in parts.required_parts, \
                    f"{car} should use Harness H"
            else:
                assert processor.HARNESS_C in parts.required_parts, \
                    f"{car} should use Harness C"
        elif "GENESIS" in car.name:
            assert processor.HARNESS_F in parts.required_parts, \
                f"{car} should use Harness F"
        else:
            # Standard SCC models
            if any(year in car.config.car_docs[0].name for year in ["2020", "2021", "2022", "2023"]):
                assert processor.HARNESS_A in parts.required_parts, \
                    f"{car} should use Harness A"
            else:
                assert processor.HARNESS_B in parts.required_parts, \
                    f"{car} should use Harness B"
        
        # All should have pry tool
        assert processor.PRY_TOOL in parts.tools, \
            f"{car} missing pry tool"

def test_hyundai_specific_models():
    """Test specific model configurations."""
    processor = HyundaiPartProcessor()
    
    # Test Ioniq 6 with HDA II
    ioniq6 = next(c for c in CAR if c.name == "HYUNDAI_IONIQ_6")
    parts = processor.get_parts_for_platform(ioniq6.config)
    assert processor.HARNESS_P in parts.required_parts
    
    # Test Ioniq 5 with HDA II
    ioniq5 = next(c for c in CAR if "IONIQ_5" in c.name)
    parts = processor.get_parts_for_platform(ioniq5.config)
    assert processor.HARNESS_Q in parts.required_parts
    
    # Test Tucson 4th gen
    tucson = next(c for c in CAR if c.name == "HYUNDAI_TUCSON_4TH_GEN")
    parts = processor.get_parts_for_platform(tucson.config)
    assert processor.HARNESS_N in parts.required_parts
    
    # Test Genesis with CAN FD
    genesis = next(c for c in CAR if c.name == "GENESIS_GV60_EV_1ST_GEN")
    parts = processor.get_parts_for_platform(genesis.config)
    assert processor.HARNESS_K in parts.required_parts
    
    # Test Legacy model
    legacy = next(c for c in CAR if c.name == "HYUNDAI_VELOSTER")
    parts = processor.get_parts_for_platform(legacy.config)
    assert processor.HARNESS_E in parts.required_parts
    
    # Test Hybrid model (Sonata Hybrid uses Harness A)
    hybrid = next(c for c in CAR if c.name == "HYUNDAI_SONATA_HYBRID")
    parts = processor.get_parts_for_platform(hybrid.config)
    assert processor.HARNESS_A in parts.required_parts

def test_tools_always_included():
    """Test that required tools are always included."""
    processor = HyundaiPartProcessor()
    
    for car in CAR:
        if not isinstance(car.config, HyundaiPlatformConfig):
            continue
            
        parts = processor.get_parts_for_platform(car.config)
        assert processor.PRY_TOOL in parts.tools, \
            f"{car} missing pry tool" 
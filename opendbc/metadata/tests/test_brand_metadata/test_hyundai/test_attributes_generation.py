"""
Tests for the generation of Hyundai attributes.py file.

These tests verify that the attributes.py file is correctly generated from the values.py file,
particularly focusing on the correct propagation of flags to attributes.
"""

import pytest
from opendbc.car.hyundai.values import CAR, HyundaiFlags
from opendbc.metadata.brand_metadata.hyundai.scripts.generate_attributes import generate_model_data

def test_min_steer_speed_flag_propagation():
    """Test that the MIN_STEER_32_MPH flag is correctly propagated to min_steer_speed."""
    # Find platforms with the MIN_STEER_32_MPH flag
    platforms_with_min_speed = []
    for platform in CAR:
        if hasattr(platform.config, 'flags') and platform.config.flags & HyundaiFlags.MIN_STEER_32_MPH:
            platforms_with_min_speed.append(str(platform))
    
    # Ensure we found at least one platform with the flag
    assert len(platforms_with_min_speed) > 0, "No platforms found with MIN_STEER_32_MPH flag"
    
    # Generate the attributes
    model_data = generate_model_data()
    
    # Check that all models with these platforms have the correct min_steer_speed
    models_with_flag = []
    for model_id, data in model_data.items():
        if data["platform"] in platforms_with_min_speed:
            models_with_flag.append(model_id)
            assert data["min_steer_speed"] == 32 * 0.44704, f"Model {model_id} has incorrect min_steer_speed"
            assert "min_speed" in data["explicit_footnotes"], f"Model {model_id} is missing min_speed footnote"
    
    # Ensure we found at least one model with the flag
    assert len(models_with_flag) > 0, "No models found with MIN_STEER_32_MPH flag"

def test_radar_scc_flag_propagation():
    """Test that the RADAR_SCC flag is correctly propagated to explicit_footnotes."""
    # Find platforms with the RADAR_SCC flag
    platforms_with_radar_scc = []
    for platform in CAR:
        if hasattr(platform.config, 'flags') and platform.config.flags & HyundaiFlags.RADAR_SCC:
            platforms_with_radar_scc.append(str(platform))
    
    # Ensure we found at least one platform with the flag
    assert len(platforms_with_radar_scc) > 0, "No platforms found with RADAR_SCC flag"
    
    # Generate the attributes
    model_data = generate_model_data()
    
    # Check that all models with these platforms have the radar_scc footnote
    models_with_flag = []
    for model_id, data in model_data.items():
        if data["platform"] in platforms_with_radar_scc:
            models_with_flag.append(model_id)
            assert "radar_scc" in data["explicit_footnotes"], f"Model {model_id} is missing radar_scc footnote"
    
    # Ensure we found at least one model with the flag
    assert len(models_with_flag) > 0, "No models found with RADAR_SCC flag"

def test_canfd_flag_propagation():
    """Test that the CANFD flag is correctly propagated to explicit_parts."""
    # Find platforms with the CANFD flag
    platforms_with_canfd = []
    for platform in CAR:
        if hasattr(platform.config, 'flags') and platform.config.flags & HyundaiFlags.CANFD:
            platforms_with_canfd.append(str(platform))
    
    # Ensure we found at least one platform with the flag
    assert len(platforms_with_canfd) > 0, "No platforms found with CANFD flag"
    
    # Generate the attributes
    model_data = generate_model_data()
    
    # Check that all models with these platforms have the CANFD kit
    models_with_flag = []
    for model_id, data in model_data.items():
        if data["platform"] in platforms_with_canfd:
            models_with_flag.append(model_id)
            assert "Kit.CANFD_KIT" in data["explicit_parts"], f"Model {model_id} is missing CANFD kit"
    
    # Ensure we found at least one model with the flag
    assert len(models_with_flag) > 0, "No models found with CANFD flag"

def test_flag_to_attribute_consistency():
    """Test that all flags that should affect attributes are correctly propagated."""
    # Generate the attributes
    model_data = generate_model_data()
    
    # Check each model's attributes against its platform's flags
    for model_id, data in model_data.items():
        platform_str = data["platform"]
        if hasattr(CAR, platform_str):
            platform = getattr(CAR, platform_str)
            if hasattr(platform.config, 'flags'):
                flags = platform.config.flags
                
                # Check MIN_STEER_32_MPH flag
                if flags & HyundaiFlags.MIN_STEER_32_MPH:
                    assert data["min_steer_speed"] == 32 * 0.44704, f"Model {model_id} has incorrect min_steer_speed"
                    assert "min_speed" in data["explicit_footnotes"], f"Model {model_id} is missing min_speed footnote"
                else:
                    assert data["min_steer_speed"] == 0.0, f"Model {model_id} should have min_steer_speed of 0.0"
                
                # Check RADAR_SCC flag
                if flags & HyundaiFlags.RADAR_SCC:
                    assert "radar_scc" in data["explicit_footnotes"], f"Model {model_id} is missing radar_scc footnote"
                
                # Check CANFD flag
                if flags & HyundaiFlags.CANFD:
                    assert "Kit.CANFD_KIT" in data["explicit_parts"], f"Model {model_id} is missing CANFD kit"
                
                # Verify all fields match what we expect based on flags
                # This ensures we're checking all relevant fields
                
                # Check min_enable_speed - should be 0.0 by default unless specified otherwise
                assert "min_enable_speed" in data, f"Model {model_id} is missing min_enable_speed field"
                
                # Check auto_resume - should be True by default
                assert "auto_resume" in data, f"Model {model_id} is missing auto_resume field"
                assert data["auto_resume"] is True, f"Model {model_id} has incorrect auto_resume value"
                
                # Check visible_in_docs - should be True by default
                assert "visible_in_docs" in data, f"Model {model_id} is missing visible_in_docs field"
                assert data["visible_in_docs"] is True, f"Model {model_id} has incorrect visible_in_docs value"
                
                # Check that platform field matches the platform string
                assert data["platform"] == platform_str, f"Model {model_id} has incorrect platform value"
                
                # Check that make and model fields exist
                assert "make" in data, f"Model {model_id} is missing make field"
                assert "model" in data, f"Model {model_id} is missing model field"
                
                # Check that years field exists and is a list
                assert "years" in data, f"Model {model_id} is missing years field"
                assert isinstance(data["years"], list), f"Model {model_id} years field is not a list"
                
                # Check that package field exists
                assert "package" in data, f"Model {model_id} is missing package field"
                
                # Check that explicit_parts field exists and is a list
                assert "explicit_parts" in data, f"Model {model_id} is missing explicit_parts field"
                assert isinstance(data["explicit_parts"], list), f"Model {model_id} explicit_parts field is not a list"
                
                # Check that explicit_footnotes field exists and is a list
                assert "explicit_footnotes" in data, f"Model {model_id} is missing explicit_footnotes field"
                assert isinstance(data["explicit_footnotes"], list), f"Model {model_id} explicit_footnotes field is not a list"
                
                # Check that support_type field exists
                assert "support_type" in data, f"Model {model_id} is missing support_type field"
                
                # Check that video_link field exists
                assert "video_link" in data, f"Model {model_id} is missing video_link field"

def test_min_enable_speed_propagation():
    """Test that min_enable_speed is correctly propagated from the car documentation."""
    # Import the generated attributes.py file to check the actual values
    from opendbc.metadata.brand_metadata.hyundai.attributes import MODEL_DATA
    
    # Find models with non-zero min_enable_speed in values.py
    models_with_min_enable_speed = []
    for platform in CAR:
        if not hasattr(platform.config, 'car_docs'):
            continue
        
        for doc in platform.config.car_docs:
            if hasattr(doc, 'min_enable_speed') and doc.min_enable_speed is not None and doc.min_enable_speed > 0:
                # Find the corresponding model in the generated data
                model_name = doc.name
                for model_id, data in MODEL_DATA.items():
                    if model_name in model_id:
                        models_with_min_enable_speed.append((model_id, doc.min_enable_speed, data["min_enable_speed"]))
    
    # Ensure we found at least one model with non-zero min_enable_speed
    assert len(models_with_min_enable_speed) > 0, "No models found with non-zero min_enable_speed"
    
    # Check that min_enable_speed is correctly propagated
    for model_id, expected_speed, min_enable_speed_value in models_with_min_enable_speed:
        # Check if the min_enable_speed is using the explicit conversion
        if isinstance(min_enable_speed_value, str) and " * CV.MPH_TO_MS" in min_enable_speed_value:
            # Extract the mph value from the string
            mph_value = float(min_enable_speed_value.split(" * ")[0])
            
            # Calculate the expected mph value based on the m/s value
            # Common values are 19 mph (8.49376 m/s) and 5 mph (2.2352 m/s)
            expected_mph = None
            if abs(expected_speed - 8.49376) < 0.001:
                expected_mph = 19.0
            elif abs(expected_speed - 2.2352) < 0.001:
                expected_mph = 5.0
            elif abs(expected_speed - 2.6822400000000003) < 0.001:
                expected_mph = 6.0
            elif abs(expected_speed - 4.4704) < 0.001:
                expected_mph = 10.0
            
            if expected_mph is not None:
                assert abs(mph_value - expected_mph) < 0.001, f"Model {model_id} has incorrect mph value: expected {expected_mph}, got {mph_value}"
            
            # Verify that the expression evaluates to the expected value
            from opendbc.car.common.conversions import Conversions as CV
            actual_speed = eval(min_enable_speed_value)
            assert abs(expected_speed - actual_speed) < 0.001, f"Model {model_id} has incorrect min_enable_speed: expected {expected_speed}, got {actual_speed}"
        else:
            # If it's not using the explicit conversion, the value should match exactly
            assert abs(expected_speed - min_enable_speed_value) < 0.001, f"Model {model_id} has incorrect min_enable_speed: expected {expected_speed}, got {min_enable_speed_value}" 
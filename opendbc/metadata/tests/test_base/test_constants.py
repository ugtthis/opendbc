import pytest

def test_columns_structure():
    """Test that COLUMNS has the correct structure."""
    from opendbc.metadata.base.constants import COLUMNS
    
    # Check required columns
    assert "MAKE" in COLUMNS
    assert "MODEL" in COLUMNS
    assert "PACKAGE" in COLUMNS
    assert "LONGITUDINAL" in COLUMNS
    assert "HARDWARE" in COLUMNS
    
    # Check column values
    assert COLUMNS["MAKE"] == "Make"
    assert COLUMNS["MODEL"] == "Model"
    assert COLUMNS["PACKAGE"] == "Supported Package"

def test_stars_structure():
    """Test that STARS has the correct structure."""
    from opendbc.metadata.base.constants import STARS
    
    # Check star types
    assert "full" in STARS
    assert "half" in STARS
    assert "empty" in STARS
    
    # Check star values
    assert STARS["full"] == "★"
    assert STARS["half"] == "½"
    assert STARS["empty"] == "☆"

def test_support_types_structure():
    """Test that SUPPORT_TYPES has the correct structure."""
    from opendbc.metadata.base.constants import SUPPORT_TYPES
    
    # Check support types
    assert "upstream" in SUPPORT_TYPES
    assert "review" in SUPPORT_TYPES
    assert "dashcam" in SUPPORT_TYPES
    assert "community" in SUPPORT_TYPES
    assert "custom" in SUPPORT_TYPES
    assert "incompatible" in SUPPORT_TYPES
    
    # Check support type structure
    for support_type in SUPPORT_TYPES.values():
        assert "name" in support_type
        assert "description" in support_type
        assert "link" in support_type

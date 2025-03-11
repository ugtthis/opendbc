"""Tests for the metadata package's __init__.py file."""

import pytest

def test_metadata_imports():
    """Test that all components are properly exported from the metadata package."""
    # Import the metadata package
    import opendbc.metadata as metadata
    
    # Test constants
    assert hasattr(metadata, 'COLUMNS')
    assert hasattr(metadata, 'EXTRA_CARS_COLUMNS')
    assert hasattr(metadata, 'STARS')
    assert hasattr(metadata, 'SUPPORT_TYPES')
    assert hasattr(metadata, 'MS_TO_MPH')
    assert hasattr(metadata, 'GOOD_TORQUE_THRESHOLD')
    
    # Test parts
    assert hasattr(metadata, 'Part')
    assert hasattr(metadata, 'Tool')
    assert hasattr(metadata, 'CarParts')
    assert hasattr(metadata, 'PlatformParts')
    assert hasattr(metadata, 'BrandPartProcessor')
    assert hasattr(metadata, 'PartCategory')
    
    # Test footnotes
    assert hasattr(metadata, 'Footnote')
    assert hasattr(metadata, 'FootnoteCollection')
    
    # Test processors
    assert hasattr(metadata, 'BaseProcessor')
    assert hasattr(metadata, 'ModelData')
    assert hasattr(metadata, 'SubaruProcessor')
    assert hasattr(metadata, 'HyundaiProcessor')
    
    # Test parts catalog
    assert hasattr(metadata, 'PartsCatalog')
    assert hasattr(metadata, 'HarnessId')
    assert hasattr(metadata, 'ToolId')
    assert hasattr(metadata, 'AccessoryId')
    assert hasattr(metadata, 'CableId')
    assert hasattr(metadata, 'MountId')
    assert hasattr(metadata, 'DeviceId')
    assert hasattr(metadata, 'KitId')
    
    # Test that the components are the correct types
    from opendbc.metadata.base.parts import Part as BasePart
    from opendbc.metadata.base.footnotes import Footnote as BaseFootnote
    from opendbc.metadata.base.processor import BaseProcessor as BaseBaseProcessor
    from opendbc.metadata.base.parts_catalog import PartsCatalog as BasePartsCatalog
    
    assert isinstance(metadata.Part, type)
    assert metadata.Part == BasePart
    
    assert isinstance(metadata.Footnote, type)
    assert metadata.Footnote == BaseFootnote
    
    assert isinstance(metadata.BaseProcessor, type)
    assert metadata.BaseProcessor == BaseBaseProcessor
    
    assert metadata.PartsCatalog == BasePartsCatalog

def test_flag_based_processor_import():
    """Test that FlagBasedProcessor is imported if available."""
    import opendbc.metadata as metadata
    
    # Check if FlagBasedProcessor is available
    try:
        from opendbc.metadata.base import FlagBasedProcessor
        assert hasattr(metadata, 'FlagBasedProcessor')
        assert hasattr(metadata, 'FlagConfig')
    except ImportError:
        # If not available, the test should pass anyway
        pass 
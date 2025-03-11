"""Tests for the base processor module."""

import pytest
from opendbc.metadata.base.processor import BaseProcessor, ModelData
from opendbc.metadata.base.parts import CarParts, Part, Tool, PartCategory
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection

def test_model_data_creation():
    """Test creating a ModelData instance."""
    data = ModelData(
        make="Honda",
        model="Civic",
        years=[2016, 2017, 2018],
        platform="HONDA_CIVIC_2016",
        package="All"
    )
    assert data.make == "Honda"
    assert data.model == "Civic"
    assert data.years == [2016, 2017, 2018]
    assert data.platform == "HONDA_CIVIC_2016"
    assert data.package == "All"

def test_processor_initialization():
    """Test initializing the BaseProcessor."""
    processor = BaseProcessor()
    assert processor.model_data == {}
    assert processor.parts_data == {}
    assert processor.footnotes == {}

def test_split_name_basic():
    """Test basic name splitting functionality."""
    processor = BaseProcessor()
    make, model, years = processor.split_name("Honda Civic 2016-18")
    assert make == "Honda"
    assert model == "Civic"
    assert years == [2016, 2017, 2018]

def test_split_name_complex():
    """Test complex name splitting with multiple year ranges."""
    processor = BaseProcessor()
    make, model, years = processor.split_name("Toyota Camry 2018,2020-22")
    assert make == "Toyota"
    assert model == "Camry"
    assert years == [2018, 2020, 2021, 2022]

def test_split_name_invalid():
    """Test invalid name formats."""
    processor = BaseProcessor()
    
    with pytest.raises(ValueError, match="Invalid model name format"):
        processor.split_name("Honda")
        
    with pytest.raises(ValueError, match="Invalid model name format"):
        processor.split_name("Honda Civic")

def test_process_model():
    """Test processing a model."""
    processor = BaseProcessor()
    model_data = ModelData(
        make="Honda",
        model="Civic",
        years=[2016, 2017, 2018],
        platform="HONDA_CIVIC_2016"
    )
    processor.model_data["honda_civic_2016"] = model_data
    
    result = processor.process_model("honda_civic_2016")
    assert result == model_data
    assert processor.process_model("nonexistent") is None

def test_get_parts():
    """Test getting parts for a model."""
    processor = BaseProcessor()
    parts = CarParts.create(
        parts=[Part(id="test_part", name="Test Part", category=PartCategory.ACCESSORY, description="Description")],
        tools=[Tool("Test Tool", "Description")]
    )
    processor.parts_data["test_model"] = parts
    
    result = processor.get_parts("test_model")
    assert result == parts
    assert processor.get_parts("nonexistent") is None

def test_get_footnotes():
    """Test getting footnotes for a model."""
    processor = BaseProcessor()
    footnotes = FootnoteCollection.create({
        "1": Footnote("Test footnote", ["PACKAGE"])
    })
    processor.footnotes["test_model"] = footnotes
    
    result = processor.get_footnotes("test_model")
    assert result == footnotes
    assert processor.get_footnotes("nonexistent") is None

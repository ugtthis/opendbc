"""Tests for the parts module."""

import pytest
from opendbc.metadata.base.parts import Part, Tool, CarParts

def test_part_creation():
    """Test creating a Part instance."""
    part = Part(
        name="Test Part",
        description="A test part",
        url="https://example.com/part"
    )
    assert part.name == "Test Part"
    assert part.description == "A test part"
    assert part.url == "https://example.com/part"

def test_tool_creation():
    """Test creating a Tool instance."""
    tool = Tool(
        name="Test Tool",
        description="A test tool",
        url="https://example.com/tool"
    )
    assert tool.name == "Test Tool"
    assert tool.description == "A test tool"
    assert tool.url == "https://example.com/tool"

def test_car_parts_creation():
    """Test creating a CarParts instance."""
    parts = [
        Part("Part 1", "Description 1"),
        Part("Part 2", "Description 2", "https://example.com/part2")
    ]
    tools = [
        Tool("Tool 1", "Description 1"),
        Tool("Tool 2", "Description 2", "https://example.com/tool2")
    ]
    notes = "Test notes"
    
    car_parts = CarParts.create(parts=parts, tools=tools, notes=notes)
    
    assert len(car_parts.parts) == 2
    assert len(car_parts.tools) == 2
    assert car_parts.notes == notes
    assert car_parts.parts[0].name == "Part 1"
    assert car_parts.tools[1].url == "https://example.com/tool2"

def test_car_parts_optional_fields():
    """Test CarParts creation with optional fields."""
    parts = [Part("Part 1", "Description 1")]
    tools = [Tool("Tool 1", "Description 1")]
    
    car_parts = CarParts.create(parts=parts, tools=tools)
    
    assert car_parts.notes is None
    assert len(car_parts.parts) == 1
    assert len(car_parts.tools) == 1

"""Tests for the footnotes module."""

import pytest
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection
from opendbc.metadata.base.constants import COLUMNS

def test_footnote_creation():
    """Test creating a Footnote instance."""
    footnote = Footnote(
        text="Test footnote",
        columns=["PACKAGE", "LONGITUDINAL"]
    )
    assert footnote.text == "Test footnote"
    assert footnote.columns == ["PACKAGE", "LONGITUDINAL"]

def test_footnote_invalid_column():
    """Test that creating a Footnote with invalid column raises ValueError."""
    with pytest.raises(ValueError, match="Invalid column name: INVALID"):
        Footnote(
            text="Test footnote",
            columns=["PACKAGE", "INVALID"]
        )

def test_footnote_collection_creation():
    """Test creating a FootnoteCollection instance."""
    footnotes = {
        "1": Footnote("First footnote", ["PACKAGE"]),
        "2": Footnote("Second footnote", ["LONGITUDINAL", "HARDWARE"])
    }
    collection = FootnoteCollection.create(footnotes)
    
    assert len(collection.footnotes) == 2
    assert collection.get_footnote("1").text == "First footnote"
    assert collection.get_footnote("2").columns == ["LONGITUDINAL", "HARDWARE"]

def test_footnote_collection_get_nonexistent():
    """Test getting a nonexistent footnote returns None."""
    collection = FootnoteCollection.create({})
    assert collection.get_footnote("nonexistent") is None

def test_footnote_collection_get_by_column():
    """Test getting footnotes by column."""
    footnotes = {
        "1": Footnote("First footnote", ["PACKAGE"]),
        "2": Footnote("Second footnote", ["PACKAGE", "HARDWARE"]),
        "3": Footnote("Third footnote", ["HARDWARE"])
    }
    collection = FootnoteCollection.create(footnotes)
    
    package_footnotes = collection.get_footnotes_for_column("PACKAGE")
    assert len(package_footnotes) == 2
    assert all(f.text in ["First footnote", "Second footnote"] for f in package_footnotes)
    
    hardware_footnotes = collection.get_footnotes_for_column("HARDWARE")
    assert len(hardware_footnotes) == 2
    assert all(f.text in ["Second footnote", "Third footnote"] for f in hardware_footnotes)

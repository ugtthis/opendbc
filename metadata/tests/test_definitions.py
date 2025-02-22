#!/usr/bin/env python3
import pytest
from opendbc.metadata.lib.definitions import (
    CarDocs, ExtraCarDocs, Column, Star, 
    Cable, PartType, get_year_list, split_name
)

def test_split_name():
    """Test car name parsing"""
    make, model, years = split_name("Toyota Camry 2020")
    assert make == "Toyota"
    assert model == "Camry"
    assert years == "2020"

def test_year_list():
    """Test year range parsing"""
    assert get_year_list("2020") == ["2020"]
    assert get_year_list("2020-22") == ["2020", "2021", "2022"]
    with pytest.raises(Exception):
        get_year_list("invalid")

def test_car_docs_init():
    """Test CarDocs initialization and properties"""
    car = CarDocs(name="Toyota Camry 2020", package="All")
    assert car.make == "Toyota"
    assert car.model == "Camry"
    assert car.years == "2020"
    assert car.package == "All"
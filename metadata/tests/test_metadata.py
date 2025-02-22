#!/usr/bin/env python3
import pytest
from opendbc.metadata.lib.metadata import (
    get_all_car_docs,
    get_car_docs_with_extras,
    group_by_make
)

def test_get_all_car_docs():
    """Test main car docs interface"""
    cars = get_all_car_docs()
    assert len(cars) > 0
    assert all(hasattr(car, 'make') for car in cars)

def test_group_by_make():
    """Test grouping functionality"""
    cars = get_all_car_docs()
    grouped = group_by_make(cars)
    # Each car should be under its make
    for make, car_list in grouped.items():
        assert all(car.make == make for car in car_list)
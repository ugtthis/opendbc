#!/usr/bin/env python3
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from opendbc.car.docs import get_car_docs_with_extras as old_get_docs
from opendbc.metadata.lib.metadata_combiner import get_car_docs_with_extras as new_get_docs

def test_car_docs_match(subtests):
    """Verify car documentation data matches between old and new implementations."""

    old_cars = old_get_docs()
    new_cars = new_get_docs()
    
    assert len(old_cars) == len(new_cars), "Number of cars should match"
    
    for old_car, new_car in zip(old_cars, new_cars):
        with subtests.test(car=old_car.name):
            # Core data that must match
            assert old_car.name == new_car.name
            assert old_car.make == new_car.make
            assert old_car.model == new_car.model
            assert old_car.row == new_car.row 
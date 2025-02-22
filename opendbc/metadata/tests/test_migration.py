#!/usr/bin/env python3
import warnings

def test_migration():
    """Test that both old and new import paths work correctly"""

    # Test old imports (with deprecation warning)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        from opendbc.car.docs_definitions import Column, CarDocs
        assert Column.MAKE.value == "Make"
        car = CarDocs(name="Toyota Camry 2018", package="All")
        assert car.make == "Toyota"

    # Test new imports
    from opendbc.metadata.lib.definitions import Column, CarDocs
    assert Column.MAKE.value == "Make"
    car = CarDocs(name="Toyota Camry 2018", package="All")
    assert car.make == "Toyota"

if __name__ == "__main__":
    test_migration()
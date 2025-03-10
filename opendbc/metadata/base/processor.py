"""
Base processor for metadata handling.

This module provides the base processor class that handles metadata processing
for vehicle models, including parts, footnotes, and platform configurations.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from .parts import CarParts
from .footnotes import FootnoteCollection

@dataclass
class ModelData:
    """Core data structure for a vehicle model."""
    make: str
    model: str
    years: List[int]
    platform: str
    package: Optional[str] = None

class BaseProcessor:
    """Base class for processing vehicle metadata."""
    
    def __init__(self):
        """Initialize the processor."""
        self.model_data: Dict[str, ModelData] = {}
        self.parts_data: Dict[str, CarParts] = {}
        self.footnotes: Dict[str, FootnoteCollection] = {}
    
    def process_model(self, model_id: str) -> Optional[ModelData]:
        """Process metadata for a specific model."""
        return self.model_data.get(model_id)
    
    def get_parts(self, model_id: str) -> Optional[CarParts]:
        """Get parts information for a specific model."""
        return self.parts_data.get(model_id)
    
    def get_footnotes(self, model_id: str) -> Optional[FootnoteCollection]:
        """Get footnotes for a specific model."""
        return self.footnotes.get(model_id)
    
    @staticmethod
    def split_name(name: str) -> Tuple[str, str, List[int]]:
        """Split a model name into make, model, and years.
        
        Example: "Honda Civic 2016-18" -> ("Honda", "Civic", [2016, 2017, 2018])
        """
        # Split make and rest
        make, *rest = name.split(" ", 1)
        if not rest:
            raise ValueError(f"Invalid model name format: {name}")
            
        # Split model and years
        parts = rest[0].rsplit(" ", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid model name format: {name}")
            
        model, year_str = parts
        
        # Parse years
        years = []
        for year_range in year_str.split(","):
            year_range = year_range.strip()
            if "-" in year_range:
                start, end = year_range.split("-")
                # Handle two-digit year ranges
                if len(end) == 2:
                    end = f"{start[:2]}{end}"
                years.extend(range(int(start), int(end) + 1))
            else:
                years.append(int(year_range))
                
        return make, model, sorted(years)

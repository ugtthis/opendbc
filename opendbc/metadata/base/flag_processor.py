"""
Flag-based processor for metadata handling.

This module provides base classes for processors that use flags to determine
metadata like footnotes and parts.
"""

from dataclasses import dataclass
from typing import Optional, Type
from enum import IntFlag

from opendbc.metadata.base.processor import BaseProcessor
from opendbc.metadata.base.footnotes import Footnote, FootnoteCollection

@dataclass
class FlagConfig:
    """Configuration for a flag-based feature."""
    flag_name: str
    footnote_key: str
    footnote_text: str
    footnote_column: str
    part_required: Optional[str] = None

class FlagBasedProcessor(BaseProcessor):
    """Base class for processors that use flags to determine metadata."""
    
    # These should be overridden by subclasses
    FLAGS: Type[IntFlag] = None
    FLAG_CONFIGS: list[FlagConfig] = []
    
    def __init__(self):
        """Initialize the processor."""
        super().__init__()
        if not self.FLAGS or not self.FLAG_CONFIGS:
            raise ValueError("Subclasses must define FLAGS and FLAG_CONFIGS")
        
        self._initialize_flag_configs()
    
    def _initialize_flag_configs(self):
        """Initialize flag configurations."""
        self.flag_configs = {}
        for config in self.FLAG_CONFIGS:
            flag_value = getattr(self.FLAGS, config.flag_name)
            self.flag_configs[flag_value] = config
    
    def _get_model_footnotes(self, model_data) -> Optional[FootnoteCollection]:
        """Get footnotes based on platform flags."""
        footnotes = {}
        
        # Get platform configuration from CAR enum
        platform_config = getattr(self.CAR, model_data.platform).config
        
        # Add footnotes based on flags
        for flag_value, config in self.flag_configs.items():
            if platform_config.flags & flag_value:
                footnotes[config.footnote_key] = Footnote(
                    text=config.footnote_text,
                    columns=[config.footnote_column]
                )
        
        return FootnoteCollection.create(footnotes) if footnotes else None 
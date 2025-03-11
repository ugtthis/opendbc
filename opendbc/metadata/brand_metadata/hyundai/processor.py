"""
Hyundai metadata processor.

This module handles Hyundai vehicle metadata for documentation and UI purposes.
Focuses on harness selection and relevant footnotes based on model/year.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from metadata.base.processor import BaseProcessor, ModelData
from metadata.base.parts import Part, CarParts, Tool
from metadata.base.footnotes import Footnote, FootnoteCollection
from metadata.base.constants import COLUMNS
from opendbc.car.hyundai.values import Footnote as HyundaiFootnote

@dataclass
class HyundaiProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self._initialize_common_parts()
        self._initialize_common_footnotes()

    def _initialize_common_parts(self):
        """Initialize parts catalog."""
        self.common_parts = {
            'harness_a': Part('Hyundai A Harness', 'For 2020+ Sonata and similar models'),
            'harness_b': Part('Hyundai B Harness', 'For older models with basic SCC'),
            'harness_g': Part('Hyundai G Harness', 'For 2019 Elantra and similar models'),
            'harness_k': Part('Hyundai K Harness', 'For 2021+ Elantra and similar models'),
            'canfd_kit': Part('CAN FD Kit', 'Required for CAN FD vehicles'),
        }

        self.common_tools = [
            Tool('Trim Removal Tool', 'For removing interior trim pieces')
        ]

    def _initialize_common_footnotes(self):
        """Initialize relevant footnotes."""
        self.common_footnotes = {
            'scc': Footnote('Requires Smart Cruise Control (SCC)', ['LONGITUDINAL']),
            'canfd': Footnote(HyundaiFootnote.CANFD.value.text, ['MODEL']),
            'min_speed': Footnote('Minimum engage speed applies', ['FSR_LONGITUDINAL']),
            'camera_scc': Footnote('Uses camera-based Smart Cruise Control', ['LONGITUDINAL']),
            'radar_scc': Footnote('Uses radar-based Smart Cruise Control', ['LONGITUDINAL']),
        }

    def process_model(self, model_id: str) -> Optional[Dict[str, str]]:
        """Process metadata for a specific model."""
        model_data = super().process_model(model_id)
        if not model_data:
            return None

        parts = self._get_parts(model_data)
        footnotes = self._get_footnotes(model_data)

        if not parts or not footnotes:
            return None

        # Store the results
        self.parts_data[model_id] = parts
        self.footnotes[model_id] = footnotes

        return model_data

    def _get_parts(self, model_data: ModelData) -> Optional[CarParts]:
        """Get required parts based on model and year."""
        model = model_data.model.lower()
        year = model_data.years[0]  # Use first year for harness selection
        
        parts = []

        # Match values.py harness selection exactly
        if model == 'elantra':
            if year >= 2021:
                parts.append(self.common_parts['harness_k'])  # HYUNDAI_ELANTRA_2021
            elif year == 2019:
                parts.append(self.common_parts['harness_g'])  # HYUNDAI_ELANTRA
            elif year <= 2018:
                parts.append(self.common_parts['harness_b'])  # HYUNDAI_ELANTRA
        elif model == 'sonata' and year >= 2020:
            parts.append(self.common_parts['harness_a'])  # HYUNDAI_SONATA
        else:
            return None

        return CarParts.create(parts=parts, tools=self.common_tools)

    def _get_footnotes(self, model_data: ModelData) -> Optional[FootnoteCollection]:
        """Get relevant footnotes based on model and year."""
        model = model_data.model.lower()
        year = model_data.years[0]  # Use first year for footnote selection
        
        footnotes = {}
        
        # All supported Hyundai models require SCC
        footnotes['scc'] = self.common_footnotes['scc']

        # Add minimum speed footnote for models with MIN_STEER_32_MPH flag
        if model == 'elantra' and year <= 2019:  # HYUNDAI_ELANTRA has MIN_STEER_32_MPH
            footnotes['min_speed'] = self.common_footnotes['min_speed']

        # Add SCC type footnote based on flags
        if model == 'sonata' and year >= 2020:  # HYUNDAI_SONATA has MANDO_RADAR
            footnotes['radar_scc'] = self.common_footnotes['radar_scc']

        return FootnoteCollection.create(footnotes) 
from typing import Dict, List
from opendbc.car.docs_definitions import CarDocs, SupportType

class MetadataRegistry:
    def __init__(self):
        self._metadata: Dict[str, List[CarDocs]] = {}
    
    def register(self, metadata_dict: Dict[str, List[CarDocs]]):
        """Register metadata for multiple platforms"""
        self._metadata.update(metadata_dict)
    
    def get_platform_metadata(self, platform_name: str) -> List[CarDocs]:
        """Get metadata for all models under a specific platform"""
        return self._metadata.get(platform_name, [])
    
    def filter_by_support(self, support_level: SupportType) -> List[CarDocs]:
        """Find all car models matching a support level"""
        result = []
        for platform_metadata in self._metadata.values():
            for car_doc in platform_metadata:
                if car_doc.support_type == support_level:
                    result.append(car_doc)
        return result
    
    def get_all_models(self) -> List[CarDocs]:
        """Get all car model metadata from all registered platforms"""
        result = []
        for platform_metadata in self._metadata.values():
            result.extend(platform_metadata)
        return result

# Global main registry instance
metadata_registry = MetadataRegistry()

# Auto-import and register manufacturer metadata
# Manufacturers will be added here as they migrate to the registry system 
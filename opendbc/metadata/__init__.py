from opendbc.metadata.honda.attributes import METADATA as HONDA_METADATA
from opendbc.metadata.hyundai.attributes import METADATA as HYUNDAI_METADATA
from opendbc.metadata.tesla.attributes import METADATA as TESLA_METADATA

METADATA = {
  **HONDA_METADATA,
  **HYUNDAI_METADATA,
  **TESLA_METADATA,
}

def get_brand_metadata(platform):
  return METADATA.get(str(platform)) 
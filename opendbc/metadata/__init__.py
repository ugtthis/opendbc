from opendbc.metadata.toyota.attributes import METADATA as TOYOTA_METADATA

METADATA = {
  **TOYOTA_METADATA,
}

def get_brand_metadata(platform_name: str):
  return METADATA.get(platform_name) 
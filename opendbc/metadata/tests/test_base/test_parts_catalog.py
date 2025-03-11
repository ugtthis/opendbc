"""Tests for the parts catalog module."""

import pytest
from opendbc.metadata.base.parts_catalog import (
    PartsCatalog, HarnessId, ToolId, AccessoryId,
    CableId, MountId, DeviceId, KitId
)
from opendbc.metadata.base.parts import Part, Tool, PartCategory

def test_parts_catalog_initialization():
    """Test that the parts catalog initializes correctly."""
    # The catalog should initialize automatically when imported
    assert PartsCatalog._harnesses
    assert PartsCatalog._tools
    assert PartsCatalog._accessories
    assert PartsCatalog._cables
    assert PartsCatalog._mounts
    assert PartsCatalog._devices
    assert PartsCatalog._kits

def test_get_harness():
    """Test retrieving a harness from the catalog."""
    harness = PartsCatalog.get_harness(HarnessId.SUBARU_A)
    
    assert harness.id == "subaru_a"
    assert harness.name == "Subaru A Harness"
    assert harness.category == PartCategory.HARNESS
    assert "pre-2020" in harness.description
    assert "subaru-a" in harness.url

def test_get_tool():
    """Test retrieving a tool from the catalog."""
    tool = PartsCatalog.get_tool(ToolId.SOCKET_8MM_DEEP)
    
    assert tool.name == "Socket 8mm Deep"
    assert "bolts" in tool.description
    assert tool.url is None

def test_get_accessory():
    """Test retrieving an accessory from the catalog."""
    accessory = PartsCatalog.get_accessory(AccessoryId.COMMA_POWER_V2)
    
    assert accessory.id == "comma_power_v2"
    assert accessory.name == "Comma Power V2"
    assert accessory.category == PartCategory.ACCESSORY
    assert "power" in accessory.description.lower()
    assert "comma.ai/shop/comma-power" in accessory.url

def test_get_cable():
    """Test retrieving a cable from the catalog."""
    cable = PartsCatalog.get_cable(CableId.LONG_OBD_C_CABLE)
    
    assert cable.id == "long_obd_c_cable"
    assert cable.name == "Long OBD-C Cable"
    assert cable.category == PartCategory.ACCESSORY
    assert "Extended" in cable.description
    assert cable.url is None

def test_get_mount():
    """Test retrieving a mount from the catalog."""
    mount = PartsCatalog.get_mount(MountId.STANDARD_MOUNT)
    
    assert mount.id == "standard_mount"
    assert mount.name == "Standard Mount"
    assert mount.category == PartCategory.ACCESSORY
    assert "Standard mount" in mount.description
    assert mount.url is None

def test_get_device():
    """Test retrieving a device from the catalog."""
    device = PartsCatalog.get_device(DeviceId.COMMA_3X)
    
    assert device.id == "comma_3x"
    assert device.name == "comma 3X"
    assert device.category == PartCategory.ACCESSORY
    assert "comma 3X device" in device.description
    assert "comma.ai/shop/comma-3x" in device.url

def test_get_kit():
    """Test retrieving a kit from the catalog."""
    kit = PartsCatalog.get_kit(KitId.CANFD_KIT)
    
    assert kit.id == "canfd_kit"
    assert kit.name == "CAN FD Kit"
    assert kit.category == PartCategory.ACCESSORY
    assert "CAN FD" in kit.description
    assert "can-fd-panda" in kit.url

def test_catalog_consistency():
    """Test that the catalog is consistent across multiple calls."""
    harness1 = PartsCatalog.get_harness(HarnessId.SUBARU_A)
    harness2 = PartsCatalog.get_harness(HarnessId.SUBARU_A)
    
    # Should be the same object
    assert harness1 is harness2
    
    # Reinitializing should not change existing objects
    PartsCatalog.initialize()
    harness3 = PartsCatalog.get_harness(HarnessId.SUBARU_A)
    
    assert harness1 is harness3 
"""
Central catalog of parts for the metadata framework.

This module provides a centralized repository of all parts, tools, and accessories
used across different vehicle brands, ensuring consistency and reducing redundancy.
"""

from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set

from opendbc.metadata.base.parts import Part, Tool, PartCategory

# ===== HARNESSES =====

class HarnessId(Enum):
    """Unique identifiers for harnesses."""
    HONDA_NIDEC = auto()
    HONDA_BOSCH_A = auto()
    HONDA_BOSCH_B = auto()
    HONDA_BOSCH_C = auto()
    TOYOTA_A = auto()
    TOYOTA_B = auto()
    SUBARU_A = auto()
    SUBARU_B = auto()
    SUBARU_C = auto()
    SUBARU_D = auto()
    FCA = auto()
    RAM = auto()
    VW_A = auto()
    VW_J533 = auto()
    HYUNDAI_A = auto()
    HYUNDAI_B = auto()
    HYUNDAI_C = auto()
    HYUNDAI_D = auto()
    HYUNDAI_E = auto()
    HYUNDAI_F = auto()
    HYUNDAI_G = auto()
    HYUNDAI_H = auto()
    HYUNDAI_I = auto()
    HYUNDAI_J = auto()
    HYUNDAI_K = auto()
    HYUNDAI_L = auto()
    HYUNDAI_M = auto()
    HYUNDAI_N = auto()
    HYUNDAI_O = auto()
    HYUNDAI_P = auto()
    HYUNDAI_Q = auto()
    HYUNDAI_R = auto()
    CUSTOM = auto()
    OBD_II = auto()
    GM = auto()
    GMSDGM = auto()
    NISSAN_A = auto()
    NISSAN_B = auto()
    MAZDA = auto()
    FORD_Q3 = auto()
    FORD_Q4 = auto()
    RIVIAN = auto()
    TESLA_A = auto()
    TESLA_B = auto()

# ===== TOOLS =====

class ToolId(Enum):
    """Unique identifiers for tools."""
    SOCKET_8MM_DEEP = auto()
    PRY_TOOL = auto()
    PHILLIPS_SCREWDRIVER = auto()
    TORX_T20 = auto()
    TORX_T30 = auto()
    PLIERS = auto()
    WIRE_STRIPPER = auto()
    ELECTRICAL_TAPE = auto()

# ===== ACCESSORIES =====

class AccessoryId(Enum):
    """Unique identifiers for accessories."""
    HARNESS_BOX = auto()
    COMMA_POWER_V2 = auto()
    LONG_OBD_C_CABLE = auto()
    USB_C_COUPLER = auto()
    CANFD_KIT = auto()

# ===== CABLES =====

class CableId(Enum):
    """Unique identifiers for cables."""
    LONG_OBD_C_CABLE = auto()
    USB_A_2_A_CABLE = auto()
    USBC_OTG_CABLE = auto()
    USBC_COUPLER = auto()
    OBD_C_CABLE_1_5FT = auto()
    RIGHT_ANGLE_OBD_C_CABLE_1_5FT = auto()

# ===== MOUNTS =====

class MountId(Enum):
    """Unique identifiers for mounts."""
    STANDARD_MOUNT = auto()
    ANGLED_MOUNT_8_DEGREES = auto()

# ===== DEVICES =====

class DeviceId(Enum):
    """Unique identifiers for devices."""
    COMMA_3X = auto()
    COMMA_3X_ANGLED_MOUNT = auto()
    RED_PANDA = auto()

# ===== KITS =====

class KitId(Enum):
    """Unique identifiers for kits."""
    RED_PANDA_KIT = auto()
    CANFD_KIT = auto()

# ===== PART DEFINITIONS =====

class PartsCatalog:
    """Central catalog of all parts used in the metadata framework."""
    
    _harnesses: Dict[HarnessId, Part] = {}
    _tools: Dict[ToolId, Tool] = {}
    _accessories: Dict[AccessoryId, Part] = {}
    _cables: Dict[CableId, Part] = {}
    _mounts: Dict[MountId, Part] = {}
    _devices: Dict[DeviceId, Part] = {}
    _kits: Dict[KitId, Part] = {}
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """Initialize the parts catalog with all known parts."""
        # Only initialize once
        if cls._initialized:
            return
            
        # Initialize harnesses
        cls._harnesses = {
            HarnessId.HONDA_NIDEC: Part(
                id="honda_nidec",
                name="Honda Nidec Harness",
                category=PartCategory.HARNESS,
                description="For Honda vehicles with Nidec ADAS",
                url="https://comma.ai/shop/harnesses/honda-nidec"
            ),
            HarnessId.HONDA_BOSCH_A: Part(
                id="honda_bosch_a",
                name="Honda Bosch A Harness",
                category=PartCategory.HARNESS,
                description="For Honda vehicles with Bosch ADAS (Type A)",
                url="https://comma.ai/shop/harnesses/honda-bosch-a"
            ),
            HarnessId.HONDA_BOSCH_B: Part(
                id="honda_bosch_b",
                name="Honda Bosch B Harness",
                category=PartCategory.HARNESS,
                description="For Honda vehicles with Bosch ADAS (Type B)",
                url="https://comma.ai/shop/harnesses/honda-bosch-b"
            ),
            HarnessId.HONDA_BOSCH_C: Part(
                id="honda_bosch_c",
                name="Honda Bosch C Harness",
                category=PartCategory.HARNESS,
                description="For Honda vehicles with Bosch ADAS (Type C)",
                url="https://comma.ai/shop/harnesses/honda-bosch-c"
            ),
            HarnessId.TOYOTA_A: Part(
                id="toyota_a",
                name="Toyota A Harness",
                category=PartCategory.HARNESS,
                description="For Toyota vehicles (Type A)",
                url="https://comma.ai/shop/harnesses/toyota-a"
            ),
            HarnessId.TOYOTA_B: Part(
                id="toyota_b",
                name="Toyota B Harness",
                category=PartCategory.HARNESS,
                description="For Toyota vehicles (Type B)",
                url="https://comma.ai/shop/harnesses/toyota-b"
            ),
            HarnessId.SUBARU_A: Part(
                id="subaru_a",
                name="Subaru A Harness",
                category=PartCategory.HARNESS,
                description="For pre-2020 models with torque-based LKAS",
                url="https://comma.ai/shop/harnesses/subaru-a"
            ),
            HarnessId.SUBARU_B: Part(
                id="subaru_b",
                name="Subaru B Harness",
                category=PartCategory.HARNESS,
                description="For 2020-22 Outback/Legacy and 2020 Crosstrek Hybrid",
                url="https://comma.ai/shop/harnesses/subaru-b"
            ),
            HarnessId.SUBARU_C: Part(
                id="subaru_c",
                name="Subaru C Harness",
                category=PartCategory.HARNESS,
                description="For 2022-24 Forester",
                url="https://comma.ai/shop/harnesses/subaru-c"
            ),
            HarnessId.SUBARU_D: Part(
                id="subaru_d",
                name="Subaru D Harness",
                category=PartCategory.HARNESS,
                description="For 2023 Outback",
                url="https://comma.ai/shop/harnesses/subaru-d"
            ),
            HarnessId.HYUNDAI_A: Part(
                id="hyundai_a",
                name="Hyundai A Harness",
                category=PartCategory.HARNESS,
                description="For Hyundai/Kia vehicles (Type A)",
                url="https://comma.ai/shop/harnesses/hyundai-a"
            ),
            HarnessId.HYUNDAI_B: Part(
                id="hyundai_b",
                name="Hyundai B Harness",
                category=PartCategory.HARNESS,
                description="For Hyundai/Kia vehicles (Type B)",
                url="https://comma.ai/shop/harnesses/hyundai-b"
            ),
            HarnessId.HYUNDAI_C: Part(
                id="hyundai_c",
                name="Hyundai C Harness",
                category=PartCategory.HARNESS,
                description="For Hyundai/Kia vehicles (Type C)",
                url="https://comma.ai/shop/harnesses/hyundai-c"
            ),
            HarnessId.HYUNDAI_G: Part(
                id="hyundai_g",
                name="Hyundai G Harness",
                category=PartCategory.HARNESS,
                description="For Hyundai/Kia vehicles (Type G)",
                url="https://comma.ai/shop/harnesses/hyundai-g"
            ),
            HarnessId.HYUNDAI_K: Part(
                id="hyundai_k",
                name="Hyundai K Harness",
                category=PartCategory.HARNESS,
                description="For Hyundai/Kia vehicles (Type K)",
                url="https://comma.ai/shop/harnesses/hyundai-k"
            ),
            # Add other harnesses as needed
        }
        
        # Initialize tools
        cls._tools = {
            ToolId.SOCKET_8MM_DEEP: Tool(
                name="Socket 8mm Deep",
                description="For removing bolts during installation",
                url=None
            ),
            ToolId.PRY_TOOL: Tool(
                name="Trim Removal Tool",
                description="For removing interior trim pieces",
                url=None
            ),
            ToolId.PHILLIPS_SCREWDRIVER: Tool(
                name="Phillips Screwdriver",
                description="For removing screws during installation",
                url=None
            ),
            ToolId.TORX_T20: Tool(
                name="Torx T20 Screwdriver",
                description="For Torx T20 screws",
                url=None
            ),
            # Add other tools as needed
        }
        
        # Initialize accessories
        cls._accessories = {
            AccessoryId.HARNESS_BOX: Part(
                id="harness_box",
                name="Harness Box",
                category=PartCategory.ACCESSORY,
                description="Protective box for the harness connection",
                url=None
            ),
            AccessoryId.COMMA_POWER_V2: Part(
                id="comma_power_v2",
                name="Comma Power V2",
                category=PartCategory.ACCESSORY,
                description="Power management for comma devices",
                url="https://comma.ai/shop/comma-power"
            ),
            AccessoryId.CANFD_KIT: Part(
                id="canfd_kit",
                name="CAN FD Kit",
                category=PartCategory.ACCESSORY,
                description="Required for vehicles with CAN FD",
                url="https://comma.ai/shop/can-fd-panda"
            ),
            # Add other accessories as needed
        }
        
        # Initialize cables
        cls._cables = {
            CableId.LONG_OBD_C_CABLE: Part(
                id="long_obd_c_cable",
                name="Long OBD-C Cable",
                category=PartCategory.ACCESSORY,
                description="Extended cable for OBD-C connections",
                url=None
            ),
            CableId.USB_A_2_A_CABLE: Part(
                id="usb_a_2_a_cable",
                name="USB A-A Cable",
                category=PartCategory.ACCESSORY,
                description="USB A to A cable",
                url=None
            ),
            CableId.USBC_OTG_CABLE: Part(
                id="usbc_otg_cable",
                name="USB-C OTG Cable",
                category=PartCategory.ACCESSORY,
                description="USB-C On-The-Go cable",
                url=None
            ),
            CableId.USBC_COUPLER: Part(
                id="usb_c_coupler",
                name="USB-C Coupler",
                category=PartCategory.ACCESSORY,
                description="Connects USB-C cables together",
                url=None
            ),
            CableId.OBD_C_CABLE_1_5FT: Part(
                id="obd_c_cable_1_5ft",
                name="OBD-C Cable (1.5 ft)",
                category=PartCategory.ACCESSORY,
                description="Short OBD-C cable",
                url=None
            ),
            CableId.RIGHT_ANGLE_OBD_C_CABLE_1_5FT: Part(
                id="right_angle_obd_c_cable_1_5ft",
                name="Right Angle OBD-C Cable (1.5 ft)",
                category=PartCategory.ACCESSORY,
                description="Short right-angle OBD-C cable",
                url=None
            ),
            # Add other cables as needed
        }
        
        # Initialize mounts
        cls._mounts = {
            MountId.STANDARD_MOUNT: Part(
                id="standard_mount",
                name="Standard Mount",
                category=PartCategory.ACCESSORY,
                description="Standard mount for comma devices",
                url=None
            ),
            MountId.ANGLED_MOUNT_8_DEGREES: Part(
                id="angled_mount_8_degrees",
                name="Angled Mount (8 degrees)",
                category=PartCategory.ACCESSORY,
                description="Angled mount for comma devices",
                url=None
            ),
            # Add other mounts as needed
        }
        
        # Initialize devices
        cls._devices = {
            DeviceId.COMMA_3X: Part(
                id="comma_3x",
                name="comma 3X",
                category=PartCategory.ACCESSORY,
                description="The comma 3X device",
                url="https://comma.ai/shop/comma-3x"
            ),
            DeviceId.RED_PANDA: Part(
                id="red_panda",
                name="Red Panda",
                category=PartCategory.ACCESSORY,
                description="CAN interface for comma devices",
                url="https://comma.ai/shop/red-panda"
            ),
            # Add other devices as needed
        }
        
        # Initialize kits
        cls._kits = {
            KitId.RED_PANDA_KIT: Part(
                id="red_panda_kit",
                name="Red Panda Kit",
                category=PartCategory.ACCESSORY,
                description="Complete kit with Red Panda",
                url="https://comma.ai/shop/red-panda"
            ),
            KitId.CANFD_KIT: Part(
                id="canfd_kit",
                name="CAN FD Kit",
                category=PartCategory.ACCESSORY,
                description="Kit for vehicles with CAN FD",
                url="https://comma.ai/shop/can-fd-panda"
            ),
            # Add other kits as needed
        }
        
        cls._initialized = True
    
    @classmethod
    def get_harness(cls, harness_id: HarnessId) -> Part:
        """Get a harness by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._harnesses[harness_id]
    
    @classmethod
    def get_tool(cls, tool_id: ToolId) -> Tool:
        """Get a tool by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._tools[tool_id]
    
    @classmethod
    def get_accessory(cls, accessory_id: AccessoryId) -> Part:
        """Get an accessory by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._accessories[accessory_id]
    
    @classmethod
    def get_cable(cls, cable_id: CableId) -> Part:
        """Get a cable by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._cables[cable_id]
    
    @classmethod
    def get_mount(cls, mount_id: MountId) -> Part:
        """Get a mount by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._mounts[mount_id]
    
    @classmethod
    def get_device(cls, device_id: DeviceId) -> Part:
        """Get a device by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._devices[device_id]
    
    @classmethod
    def get_kit(cls, kit_id: KitId) -> Part:
        """Get a kit by its ID."""
        if not cls._initialized:
            cls.initialize()
        return cls._kits[kit_id]

# Initialize the catalog when the module is imported
PartsCatalog.initialize() 
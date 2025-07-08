from enum import IntFlag

from opendbc.car import Bus, CarSpecs, PlatformConfig, Platforms, structs, uds
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.fw_query_definitions import FwQueryConfig, Request, StdQueries, p16

Ecu = structs.CarParams.Ecu
VisualAlert = structs.CarControl.HUDControl.VisualAlert
GearShifter = structs.CarState.GearShifter

class CarControllerParams:
  # Allow small margin below -3.5 m/s^2 from ISO 15622:2018 since we
  # perform the closed loop control, and might need some
  # to apply some more braking if we're on a downhill slope.
  # Our controller should still keep the 2 second average above
  # -3.5 m/s^2 as per planner limits
  NIDEC_ACCEL_MIN = -4.0  # m/s^2
  NIDEC_ACCEL_MAX = 1.6  # m/s^2, lower than 2.0 m/s^2 for tuning reasons

  NIDEC_ACCEL_LOOKUP_BP = [-1., 0., .6]
  NIDEC_ACCEL_LOOKUP_V = [-4.8, 0., 2.0]

  NIDEC_MAX_ACCEL_V = [0.5, 2.4, 1.4, 0.6]
  NIDEC_MAX_ACCEL_BP = [0.0, 4.0, 10., 20.]

  NIDEC_GAS_MAX = 198  # 0xc6
  NIDEC_BRAKE_MAX = 1024 // 4

  BOSCH_ACCEL_MIN = -3.5  # m/s^2
  BOSCH_ACCEL_MAX = 2.0  # m/s^2

  BOSCH_GAS_LOOKUP_BP = [-0.2, 2.0]  # 2m/s^2
  BOSCH_GAS_LOOKUP_V = [0, 1600]

  STEER_STEP = 1  # 100 Hz
  STEER_DELTA_UP = 3  # min/max in 0.33s for all Honda
  STEER_DELTA_DOWN = 3

  def __init__(self, CP):
    self.STEER_MAX = CP.lateralParams.torqueBP[-1]
    # mirror of list (assuming first item is zero) for interp of signed request
    # values and verify that both arrays begin at zero
    assert CP.lateralParams.torqueBP[0] == 0
    assert CP.lateralParams.torqueV[0] == 0
    self.STEER_LOOKUP_BP = [v * -1 for v in CP.lateralParams.torqueBP][1:][::-1] + list(CP.lateralParams.torqueBP)
    self.STEER_LOOKUP_V = [v * -1 for v in CP.lateralParams.torqueV][1:][::-1] + list(CP.lateralParams.torqueV)


class HondaSafetyFlags(IntFlag):
  ALT_BRAKE = 1
  BOSCH_LONG = 2
  NIDEC_ALT = 4
  RADARLESS = 8


class HondaFlags(IntFlag):
  # Detected flags
  # Bosch models with alternate set of LKAS_HUD messages
  BOSCH_EXT_HUD = 1
  BOSCH_ALT_BRAKE = 2

  # Static flags
  BOSCH = 4
  BOSCH_RADARLESS = 8

  NIDEC = 16
  NIDEC_ALT_PCM_ACCEL = 32
  NIDEC_ALT_SCM_MESSAGES = 64

  BOSCH_CANFD = 128

# Car button codes
class CruiseButtons:
  RES_ACCEL = 4
  DECEL_SET = 3
  CANCEL = 2
  MAIN = 1


class CruiseSettings:
  DISTANCE = 3
  LKAS = 1


# See dbc files for info on values
VISUAL_HUD = {
  VisualAlert.none: 0,
  VisualAlert.fcw: 1,
  VisualAlert.steerRequired: 1,
  VisualAlert.ldw: 1,
  VisualAlert.brakePressed: 10,
  VisualAlert.wrongGear: 6,
  VisualAlert.seatbeltUnbuckled: 5,
  VisualAlert.speedTooHigh: 8
}



class HondaBoschPlatformConfig(PlatformConfig):
  def init(self):
    self.flags |= HondaFlags.BOSCH


class HondaNidecPlatformConfig(PlatformConfig):
  def init(self):
    self.flags |= HondaFlags.NIDEC


def radar_dbc_dict(pt_dict):
  return {Bus.pt: pt_dict, Bus.radar: 'acura_ilx_2016_nidec'}


class CAR(Platforms):
  # Bosch Cars
  HONDA_ACCORD = HondaBoschPlatformConfig(
    [],
    # steerRatio: 11.82 is spec end-to-end
    CarSpecs(mass=3279 * CV.LB_TO_KG, wheelbase=2.83, steerRatio=16.33, centerToFrontRatio=0.39, tireStiffnessFactor=0.8467),
    {Bus.pt: 'honda_accord_2018_can_generated'},
  )
  HONDA_CIVIC_BOSCH = HondaBoschPlatformConfig(
    [],
    CarSpecs(mass=1326, wheelbase=2.7, steerRatio=15.38, centerToFrontRatio=0.4),  # steerRatio: 10.93 is end-to-end spec
    {Bus.pt: 'honda_civic_hatchback_ex_2017_can_generated'},
  )
  HONDA_CIVIC_BOSCH_DIESEL = HondaBoschPlatformConfig(
    [],  # don't show in docs
    HONDA_CIVIC_BOSCH.specs,
    {Bus.pt: 'honda_accord_2018_can_generated'},
  )
  HONDA_CIVIC_2022 = HondaBoschPlatformConfig(
    [],
    HONDA_CIVIC_BOSCH.specs,
    {Bus.pt: 'honda_civic_ex_2022_can_generated'},
    flags=HondaFlags.BOSCH_RADARLESS,
  )
  HONDA_CRV_5G = HondaBoschPlatformConfig(
    [],
    # steerRatio: 12.3 is spec end-to-end
    CarSpecs(mass=3410 * CV.LB_TO_KG, wheelbase=2.66, steerRatio=16.0, centerToFrontRatio=0.41, tireStiffnessFactor=0.677),
    {Bus.pt: 'honda_crv_ex_2017_can_generated', Bus.body: 'honda_crv_ex_2017_body_generated'},
    flags=HondaFlags.BOSCH_ALT_BRAKE,
  )
  HONDA_CRV_HYBRID = HondaBoschPlatformConfig(
    [],
    # mass: mean of 4 models in kg, steerRatio: 12.3 is spec end-to-end
    CarSpecs(mass=1667, wheelbase=2.66, steerRatio=16, centerToFrontRatio=0.41, tireStiffnessFactor=0.677),
    {Bus.pt: 'honda_accord_2018_can_generated'},
  )
  HONDA_HRV_3G = HondaBoschPlatformConfig(
    [],
    CarSpecs(mass=3125 * CV.LB_TO_KG, wheelbase=2.61, steerRatio=15.2, centerToFrontRatio=0.41, tireStiffnessFactor=0.5),
    {Bus.pt: 'honda_civic_ex_2022_can_generated'},
    flags=HondaFlags.BOSCH_RADARLESS,
  )
  ACURA_RDX_3G = HondaBoschPlatformConfig(
    [],
    CarSpecs(mass=4068 * CV.LB_TO_KG, wheelbase=2.75, steerRatio=11.95, centerToFrontRatio=0.41, tireStiffnessFactor=0.677),  # as spec
    {Bus.pt: 'acura_rdx_2020_can_generated'},
    flags=HondaFlags.BOSCH_ALT_BRAKE,
  )
  HONDA_INSIGHT = HondaBoschPlatformConfig(
    [],
    CarSpecs(mass=2987 * CV.LB_TO_KG, wheelbase=2.7, steerRatio=15.0, centerToFrontRatio=0.39, tireStiffnessFactor=0.82),  # as spec
    {Bus.pt: 'honda_insight_ex_2019_can_generated'},
  )
  HONDA_E = HondaBoschPlatformConfig(
    [],
    CarSpecs(mass=3338.8 * CV.LB_TO_KG, wheelbase=2.5, centerToFrontRatio=0.5, steerRatio=16.71, tireStiffnessFactor=0.82),
    {Bus.pt: 'acura_rdx_2020_can_generated'},
  )
  HONDA_PILOT_4G = HondaBoschPlatformConfig(
    [],
    CarSpecs(mass=4278 * CV.LB_TO_KG, wheelbase=2.86, centerToFrontRatio=0.428, steerRatio=16.0, tireStiffnessFactor=0.444),  # as spec
    {Bus.pt: 'honda_pilot_2023_can_generated'},
    flags=HondaFlags.BOSCH_CANFD | HondaFlags.BOSCH_ALT_BRAKE,
  )

  # Nidec Cars
  ACURA_ILX = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=3095 * CV.LB_TO_KG, wheelbase=2.67, steerRatio=18.61, centerToFrontRatio=0.37, tireStiffnessFactor=0.72),  # 15.3 is spec end-to-end
    radar_dbc_dict('acura_ilx_2016_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_CRV = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=3572 * CV.LB_TO_KG, wheelbase=2.62, steerRatio=16.89, centerToFrontRatio=0.41, tireStiffnessFactor=0.444),  # as spec
    radar_dbc_dict('honda_crv_touring_2016_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_CRV_EU = HondaNidecPlatformConfig(
    [],  # Euro version of CRV Touring, don't show in docs
    HONDA_CRV.specs,
    radar_dbc_dict('honda_crv_executive_2016_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_FIT = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=2644 * CV.LB_TO_KG, wheelbase=2.53, steerRatio=13.06, centerToFrontRatio=0.39, tireStiffnessFactor=0.75),
    radar_dbc_dict('honda_fit_ex_2018_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_FREED = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=3086. * CV.LB_TO_KG, wheelbase=2.74, steerRatio=13.06, centerToFrontRatio=0.39, tireStiffnessFactor=0.75),  # mostly copied from FIT
    radar_dbc_dict('honda_fit_ex_2018_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_HRV = HondaNidecPlatformConfig(
    [],
    HONDA_HRV_3G.specs,
    radar_dbc_dict('honda_fit_ex_2018_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_ODYSSEY = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=1900, wheelbase=3.0, steerRatio=14.35, centerToFrontRatio=0.41, tireStiffnessFactor=0.82),
    radar_dbc_dict('honda_odyssey_exl_2018_generated'),
    flags=HondaFlags.NIDEC_ALT_PCM_ACCEL,
  )
  HONDA_ODYSSEY_CHN = HondaNidecPlatformConfig(
    [],  # Chinese version of Odyssey, don't show in docs
    HONDA_ODYSSEY.specs,
    radar_dbc_dict('honda_odyssey_extreme_edition_2018_china_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  ACURA_RDX = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=3925 * CV.LB_TO_KG, wheelbase=2.68, steerRatio=15.0, centerToFrontRatio=0.38, tireStiffnessFactor=0.444),  # as spec
    radar_dbc_dict('acura_rdx_2018_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_PILOT = HondaNidecPlatformConfig(
    [],
    HONDA_PILOT_4G.specs,
    radar_dbc_dict('acura_ilx_2016_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_RIDGELINE = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=4515 * CV.LB_TO_KG, wheelbase=3.18, centerToFrontRatio=0.41, steerRatio=15.59, tireStiffnessFactor=0.444),  # as spec
    radar_dbc_dict('acura_ilx_2016_can_generated'),
    flags=HondaFlags.NIDEC_ALT_SCM_MESSAGES,
  )
  HONDA_CIVIC = HondaNidecPlatformConfig(
    [],
    CarSpecs(mass=1326, wheelbase=2.70, centerToFrontRatio=0.4, steerRatio=15.38),  # 10.93 is end-to-end spec
    radar_dbc_dict('honda_civic_touring_2016_can_generated'),
  )


HONDA_ALT_VERSION_REQUEST = bytes([uds.SERVICE_TYPE.READ_DATA_BY_IDENTIFIER]) + \
  p16(0xF112)
HONDA_ALT_VERSION_RESPONSE = bytes([uds.SERVICE_TYPE.READ_DATA_BY_IDENTIFIER + 0x40]) + \
  p16(0xF112)

FW_QUERY_CONFIG = FwQueryConfig(
  requests=[
    # Currently used to fingerprint
    Request(
      [StdQueries.UDS_VERSION_REQUEST],
      [StdQueries.UDS_VERSION_RESPONSE],
      bus=1,
    ),

    # Data collection requests:
    # Log manufacturer-specific identifier for current ECUs
    Request(
      [HONDA_ALT_VERSION_REQUEST],
      [HONDA_ALT_VERSION_RESPONSE],
      bus=1,
      logging=True,
    ),
    # Nidec PT bus
    Request(
      [StdQueries.UDS_VERSION_REQUEST],
      [StdQueries.UDS_VERSION_RESPONSE],
      bus=0,
    ),
    # Bosch PT bus
    Request(
      [StdQueries.UDS_VERSION_REQUEST],
      [StdQueries.UDS_VERSION_RESPONSE],
      bus=1,
      obd_multiplexing=False,
    ),
  ],
  # We lose these ECUs without the comma power on these cars.
  # Note that we still attempt to match with them when they are present
  # This is or'd with (ALL_ECUS - ESSENTIAL_ECUS) from fw_versions.py
  non_essential_ecus={
    Ecu.eps: [CAR.ACURA_RDX_3G, CAR.HONDA_ACCORD, CAR.HONDA_CIVIC_2022, CAR.HONDA_E, CAR.HONDA_HRV_3G],
    Ecu.vsa: [CAR.ACURA_RDX_3G, CAR.HONDA_ACCORD, CAR.HONDA_CIVIC, CAR.HONDA_CIVIC_BOSCH, CAR.HONDA_CIVIC_2022, CAR.HONDA_CRV_5G, CAR.HONDA_CRV_HYBRID,
              CAR.HONDA_E, CAR.HONDA_HRV_3G, CAR.HONDA_INSIGHT],
  },
  extra_ecus=[
    (Ecu.combinationMeter, 0x18da60f1, None),
    (Ecu.programmedFuelInjection, 0x18da10f1, None),
    # The only other ECU on PT bus accessible by camera on radarless Civic
    # This is likely a manufacturer-specific sub-address implementation: the camera responds to this and 0x18dab0f1
    # Unclear what the part number refers to: 8S103 is 'Camera Set Mono', while 36160 is 'Camera Monocular - Honda'
    # TODO: add query back, camera does not support querying both in parallel and 0x18dab0f1 often fails to respond
    # (Ecu.unknown, 0x18DAB3F1, None),
  ],
)

STEER_THRESHOLD = {
  # default is 1200, overrides go here
  CAR.ACURA_RDX: 400,
  CAR.HONDA_CRV_EU: 400,
}

HONDA_NIDEC_ALT_PCM_ACCEL = CAR.with_flags(HondaFlags.NIDEC_ALT_PCM_ACCEL)
HONDA_NIDEC_ALT_SCM_MESSAGES = CAR.with_flags(HondaFlags.NIDEC_ALT_SCM_MESSAGES)
HONDA_BOSCH = CAR.with_flags(HondaFlags.BOSCH)
HONDA_BOSCH_RADARLESS = CAR.with_flags(HondaFlags.BOSCH_RADARLESS)
HONDA_BOSCH_CANFD = CAR.with_flags(HondaFlags.BOSCH_CANFD)


DBC = CAR.create_dbc_map()

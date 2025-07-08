from dataclasses import dataclass
from enum import Enum

from opendbc.car import structs
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.docs_definitions import CarFootnote, CarHarness, CarDocs, CarParts, Column, Device
from opendbc.car.honda.values import HondaFlags


@dataclass
class HondaCarDocs(CarDocs):
  package: str = "Honda Sensing"

  def init_make(self, CP: structs.CarParams):
    if CP.flags & HondaFlags.BOSCH:
      if CP.flags & HondaFlags.BOSCH_CANFD:
        harness = CarHarness.bosch_c
      elif CP.flags & HondaFlags.BOSCH_RADARLESS:
        harness = CarHarness.bosch_b
      else:
        harness = CarHarness.bosch_a
    else:
      harness = CarHarness.nidec

    # EXACT COPY: Import CAR here to avoid circular imports
    from opendbc.car.honda.values import CAR
    if CP.carFingerprint in (CAR.HONDA_PILOT_4G,):
      self.car_parts = CarParts([Device.threex_angled_mount, harness])
    else:
      self.car_parts = CarParts.common([harness])


class Footnote(Enum):
  CIVIC_DIESEL = CarFootnote(
    "2019 Honda Civic 1.6L Diesel Sedan does not have ALC below 12mph.",
    Column.FSR_STEERING)


METADATA = {
  # Bosch Cars
  "HONDA_ACCORD": [
    HondaCarDocs(
      name="Honda Accord 2018-22",
      package="All",
      video="https://www.youtube.com/watch?v=mrUwlj3Mi58",
      min_steer_speed=3. * CV.MPH_TO_MS,
    ),
    HondaCarDocs(
      name="Honda Inspire 2018",
      package="All",
      min_steer_speed=3. * CV.MPH_TO_MS,
    ),
    HondaCarDocs(
      name="Honda Accord Hybrid 2018-22",
      package="All",
      min_steer_speed=3. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_CIVIC_BOSCH": [
    HondaCarDocs(
      name="Honda Civic 2019-21",
      package="All",
      video="https://www.youtube.com/watch?v=4Iz1Mz5LGF8",
      footnotes=[Footnote.CIVIC_DIESEL],
      min_steer_speed=2. * CV.MPH_TO_MS,
    ),
    HondaCarDocs(
      name="Honda Civic Hatchback 2017-21",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_CIVIC_BOSCH_DIESEL": [],  # don't show in docs

  "HONDA_CIVIC_2022": [
    HondaCarDocs(
      name="Honda Civic 2022-24",
      package="All",
      video="https://youtu.be/ytiOT5lcp6Q",
    ),
    HondaCarDocs(
      name="Honda Civic Hatchback 2022-24",
      package="All",
      video="https://youtu.be/ytiOT5lcp6Q",
    ),
    HondaCarDocs(
      name="Honda Civic Hatchback Hybrid (Europe only) 2023",
      package="All",
    ),
    # TODO: Confirm 2024
    HondaCarDocs(
      name="Honda Civic Hatchback Hybrid 2025",
      package="All",
    ),
  ],

  "HONDA_CRV_5G": [
    HondaCarDocs(
      name="Honda CR-V 2017-22",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_CRV_HYBRID": [
    HondaCarDocs(
      name="Honda CR-V Hybrid 2017-22",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_HRV_3G": [
    HondaCarDocs(
      name="Honda HR-V 2023-25",
      package="All",
    ),
  ],

  "ACURA_RDX_3G": [
    HondaCarDocs(
      name="Acura RDX 2019-21",
      package="All",
      min_steer_speed=3. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_INSIGHT": [
    HondaCarDocs(
      name="Honda Insight 2019-22",
      package="All",
      min_steer_speed=3. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_E": [
    HondaCarDocs(
      name="Honda e 2020",
      package="All",
      min_steer_speed=3. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_PILOT_4G": [
    HondaCarDocs(
      name="Honda Pilot 2023",
      package="All",
    ),
  ],

  # Nidec Cars
  "ACURA_ILX": [
    HondaCarDocs(
      name="Acura ILX 2016-18",
      package="Technology Plus Package or AcuraWatch Plus",
      min_steer_speed=25. * CV.MPH_TO_MS,
    ),
    HondaCarDocs(
      name="Acura ILX 2019",
      package="All",
      min_steer_speed=25. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_CRV": [
    HondaCarDocs(
      name="Honda CR-V 2015-16",
      package="Touring Trim",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_CRV_EU": [],  # Euro version of CRV Touring, don't show in docs

  "HONDA_FIT": [
    HondaCarDocs(
      name="Honda Fit 2018-20",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_FREED": [
    HondaCarDocs(
      name="Honda Freed 2020",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_HRV": [
    HondaCarDocs(
      name="Honda HR-V 2019-22",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_ODYSSEY": [
    HondaCarDocs(
      name="Honda Odyssey 2018-20",
    ),
  ],

  "HONDA_ODYSSEY_CHN": [],  # Chinese version of Odyssey, don't show in docs

  "ACURA_RDX": [
    HondaCarDocs(
      name="Acura RDX 2016-18",
      package="AcuraWatch Plus or Advance Package",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_PILOT": [
    HondaCarDocs(
      name="Honda Pilot 2016-22",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
    HondaCarDocs(
      name="Honda Passport 2019-25",
      package="All",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_RIDGELINE": [
    HondaCarDocs(
      name="Honda Ridgeline 2017-25",
      min_steer_speed=12. * CV.MPH_TO_MS,
    ),
  ],

  "HONDA_CIVIC": [
    HondaCarDocs(
      name="Honda Civic 2016-18",
      min_steer_speed=12. * CV.MPH_TO_MS,
      video="https://youtu.be/-IkImTe1NYE",
    ),
  ],
} 
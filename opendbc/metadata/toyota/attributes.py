from dataclasses import dataclass, field
from enum import Enum

from opendbc.car.docs_definitions import CarFootnote, CarDocs, Column, CarParts, CarHarness, SupportType
from opendbc.car.common.conversions import Conversions as CV

MIN_ACC_SPEED = 19. * CV.MPH_TO_MS

class Footnote(Enum):
  CAMRY = CarFootnote(
    "openpilot operates above 28mph for Camry 4CYL L, 4CYL LE and 4CYL SE which don't have Full-Speed Range Dynamic Radar Cruise Control.",
    Column.FSR_LONGITUDINAL)

@dataclass
class ToyotaCarDocs(CarDocs):
  package: str = "All"
  car_parts: CarParts = field(default_factory=CarParts.common([CarHarness.toyota_a]))

@dataclass
class ToyotaCommunityCarDocs(ToyotaCarDocs):
  support_type: SupportType = SupportType.COMMUNITY
  support_link: str = "#community"


METADATA = {
  "TOYOTA_ALPHARD_TSS2": [
    ToyotaCarDocs(
      name="Toyota Alphard 2019-20",
    ),
    ToyotaCarDocs(
      name="Toyota Alphard Hybrid 2021",
    ),
  ],
  
  "TOYOTA_AVALON": [
    ToyotaCarDocs(
      name="Toyota Avalon 2016",
      package="Toyota Safety Sense P",
    ),
    ToyotaCarDocs(
      name="Toyota Avalon 2017-18",
    ),
  ],
  
  "TOYOTA_AVALON_2019": [
    ToyotaCarDocs(
      name="Toyota Avalon 2019-21",
    ),
    ToyotaCarDocs(
      name="Toyota Avalon Hybrid 2019-21",
    ),
  ],
  
  "TOYOTA_AVALON_TSS2": [
    ToyotaCarDocs(
      name="Toyota Avalon 2022",
    ),
    ToyotaCarDocs(
      name="Toyota Avalon Hybrid 2022",
    ),
  ],
  
  "TOYOTA_CAMRY": [
    ToyotaCarDocs(
      name="Toyota Camry 2018-20",
      video="https://www.youtube.com/watch?v=fkcjviZY9CM",
      footnotes=[Footnote.CAMRY],
    ),
    ToyotaCarDocs(
      name="Toyota Camry Hybrid 2018-20",
      video="https://www.youtube.com/watch?v=Q2DYY0AWKgk",
    ),
  ],
  
  "TOYOTA_CAMRY_TSS2": [
    ToyotaCarDocs(
      name="Toyota Camry 2021-24",
      footnotes=[Footnote.CAMRY],
    ),
    ToyotaCarDocs(
      name="Toyota Camry Hybrid 2021-24",
    ),
  ],
  
  "TOYOTA_CHR": [
    ToyotaCarDocs(
      name="Toyota C-HR 2017-20",
    ),
    ToyotaCarDocs(
      name="Toyota C-HR Hybrid 2017-20",
    ),
  ],
  
  "TOYOTA_CHR_TSS2": [
    ToyotaCarDocs(
      name="Toyota C-HR 2021",
    ),
    ToyotaCarDocs(
      name="Toyota C-HR Hybrid 2021-22",
    ),
  ],
  
  "TOYOTA_COROLLA": [
    ToyotaCarDocs(
      name="Toyota Corolla 2017-19",
    ),
  ],
  
  "TOYOTA_COROLLA_TSS2": [
    ToyotaCarDocs(
      name="Toyota Corolla 2020-22",
      video="https://www.youtube.com/watch?v=_66pXk0CBYA",
    ),
    ToyotaCarDocs(
      name="Toyota Corolla Cross (Non-US only) 2020-23",
      min_enable_speed=7.5,
    ),
    ToyotaCarDocs(
      name="Toyota Corolla Hatchback 2019-22",
      video="https://www.youtube.com/watch?v=_66pXk0CBYA",
    ),
    # Hybrid platforms
    ToyotaCarDocs(
      name="Toyota Corolla Hybrid 2020-22",
    ),
    ToyotaCarDocs(
      name="Toyota Corolla Hybrid (South America only) 2020-23",
      min_enable_speed=7.5,
    ),
    ToyotaCarDocs(
      name="Toyota Corolla Cross Hybrid (Non-US only) 2020-22",
      min_enable_speed=7.5,
    ),
    ToyotaCarDocs(
      name="Lexus UX Hybrid 2019-24",
    ),
  ],
  
  "TOYOTA_HIGHLANDER": [
    ToyotaCarDocs(
      name="Toyota Highlander 2017-19",
      video="https://www.youtube.com/watch?v=0wS0wXSLzoo",
    ),
    ToyotaCarDocs(
      name="Toyota Highlander Hybrid 2017-19",
    ),
  ],
  
  "TOYOTA_HIGHLANDER_TSS2": [
    ToyotaCarDocs(
      name="Toyota Highlander 2020-23",
    ),
    ToyotaCarDocs(
      name="Toyota Highlander Hybrid 2020-23",
    ),
  ],
  
  "TOYOTA_PRIUS": [
    ToyotaCarDocs(
      name="Toyota Prius 2016",
      package="Toyota Safety Sense P",
      video="https://www.youtube.com/watch?v=8zopPJI8XQ0",
    ),
    ToyotaCarDocs(
      name="Toyota Prius 2017-20",
      video="https://www.youtube.com/watch?v=8zopPJI8XQ0",
    ),
    ToyotaCarDocs(
      name="Toyota Prius Prime 2017-20",
      video="https://www.youtube.com/watch?v=8zopPJI8XQ0",
    ),
  ],
  
  "TOYOTA_PRIUS_V": [
    ToyotaCarDocs(
      name="Toyota Prius v 2017",
      package="Toyota Safety Sense P",
      min_enable_speed=MIN_ACC_SPEED,
    ),
  ],
  
  "TOYOTA_PRIUS_TSS2": [
    ToyotaCarDocs(
      name="Toyota Prius 2021-22",
      video="https://www.youtube.com/watch?v=J58TvCpUd4U",
    ),
    ToyotaCarDocs(
      name="Toyota Prius Prime 2021-22",
      video="https://www.youtube.com/watch?v=J58TvCpUd4U",
    ),
  ],
  
  "TOYOTA_RAV4": [
    ToyotaCarDocs(
      name="Toyota RAV4 2016",
      package="Toyota Safety Sense P",
    ),
    ToyotaCarDocs(
      name="Toyota RAV4 2017-18",
    ),
  ],
  
  "TOYOTA_RAV4H": [
    ToyotaCarDocs(
      name="Toyota RAV4 Hybrid 2016",
      package="Toyota Safety Sense P",
      video="https://youtu.be/LhT5VzJVfNI?t=26",
    ),
    ToyotaCarDocs(
      name="Toyota RAV4 Hybrid 2017-18",
      video="https://youtu.be/LhT5VzJVfNI?t=26",
    ),
  ],
  
  "TOYOTA_RAV4_TSS2": [
    ToyotaCarDocs(
      name="Toyota RAV4 2019-21",
      video="https://www.youtube.com/watch?v=wJxjDd42gGA",
    ),
    ToyotaCarDocs(
      name="Toyota RAV4 Hybrid 2019-21",
    ),
  ],
  
  "TOYOTA_RAV4_TSS2_2022": [
    ToyotaCarDocs(
      name="Toyota RAV4 2022",
    ),
    ToyotaCarDocs(
      name="Toyota RAV4 Hybrid 2022",
      video="https://youtu.be/U0nH9cnrFB0",
    ),
  ],
  
  "TOYOTA_RAV4_TSS2_2023": [
    ToyotaCarDocs(
      name="Toyota RAV4 2023-25",
    ),
    ToyotaCarDocs(
      name="Toyota RAV4 Hybrid 2023-25",
      video="https://youtu.be/4eIsEq4L4Ng",
    ),
  ],
  
  "TOYOTA_RAV4_PRIME": [
    ToyotaCommunityCarDocs(
      name="Toyota RAV4 Prime 2021-23",
      min_enable_speed=MIN_ACC_SPEED,
    ),
  ],
  
  "TOYOTA_YARIS": [
    ToyotaCommunityCarDocs(
      name="Toyota Yaris (Non-US only) 2023",
      min_enable_speed=MIN_ACC_SPEED,
    ),
  ],
  
  "TOYOTA_MIRAI": [
    ToyotaCarDocs(
      name="Toyota Mirai 2021",
    ),
  ],
  
  "TOYOTA_SIENNA": [
    ToyotaCarDocs(
      name="Toyota Sienna 2018-20",
      video="https://www.youtube.com/watch?v=q1UPOo4Sh68",
      min_enable_speed=MIN_ACC_SPEED,
    ),
  ],
  
  "TOYOTA_SIENNA_4TH_GEN": [
    ToyotaCommunityCarDocs(
      name="Toyota Sienna 2021-23",
      min_enable_speed=MIN_ACC_SPEED,
    ),
  ],

  # Lexus
  "LEXUS_CTH": [
    ToyotaCarDocs(
      name="Lexus CT Hybrid 2017-18",
      package="Lexus Safety System+",
    ),
  ],
  
  "LEXUS_ES": [
    ToyotaCarDocs(
      name="Lexus ES 2017-18",
    ),
    ToyotaCarDocs(
      name="Lexus ES Hybrid 2017-18",
    ),
  ],
  
  "LEXUS_ES_TSS2": [
    ToyotaCarDocs(
      name="Lexus ES 2019-25",
    ),
    ToyotaCarDocs(
      name="Lexus ES Hybrid 2019-25",
      video="https://youtu.be/BZ29osRVJeg?t=12",
    ),
  ],
  
  "LEXUS_IS": [
    ToyotaCarDocs(
      name="Lexus IS 2017-19",
    ),
  ],
  
  "LEXUS_IS_TSS2": [
    ToyotaCarDocs(
      name="Lexus IS 2022-24",
    ),
  ],
  
  "LEXUS_NX": [
    ToyotaCarDocs(
      name="Lexus NX 2018-19",
    ),
    ToyotaCarDocs(
      name="Lexus NX Hybrid 2018-19",
    ),
  ],
  
  "LEXUS_NX_TSS2": [
    ToyotaCarDocs(
      name="Lexus NX 2020-21",
    ),
    ToyotaCarDocs(
      name="Lexus NX Hybrid 2020-21",
    ),
  ],
  
  "LEXUS_LC_TSS2": [
    ToyotaCarDocs(
      name="Lexus LC 2024",
    ),
  ],
  
  "LEXUS_RC": [
    ToyotaCarDocs(
      name="Lexus RC 2018-20",
    ),
  ],
  
  "LEXUS_RC_TSS2": [
    ToyotaCarDocs(
      name="Lexus RC 2023",
    ),
  ],
  
  "LEXUS_RX": [
    ToyotaCarDocs(
      name="Lexus RX 2016",
      package="Lexus Safety System+",
    ),
    ToyotaCarDocs(
      name="Lexus RX 2017-19",
    ),
    # Hybrid platforms
    ToyotaCarDocs(
      name="Lexus RX Hybrid 2016",
      package="Lexus Safety System+",
    ),
    ToyotaCarDocs(
      name="Lexus RX Hybrid 2017-19",
    ),
  ],
  
  "LEXUS_RX_TSS2": [
    ToyotaCarDocs(
      name="Lexus RX 2020-22",
    ),
    ToyotaCarDocs(
      name="Lexus RX Hybrid 2020-22",
    ),
  ],
  
  "LEXUS_GS_F": [
    ToyotaCarDocs(
      name="Lexus GS F 2016",
    ),
  ],
}





 
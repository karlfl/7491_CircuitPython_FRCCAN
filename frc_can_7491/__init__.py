# SPDX-FileCopyrightText: Copyright (c) 2024 Karl Fleischmann for Team 7491 Cyber Soldiers
#
# SPDX-License-Identifier: MIT
"""
`7491_frccan`
================================================================================

Circuit Python Library for managing devices using the FIRST Robotics Competition (FRC) CAN Bus communications.  Written by the programming team of Team 7491 Cyber Soldiers in Burton, MI


* Author(s): Karl Fleischmann

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

from frc_can_7491.CANDevice import CANDevice
from frc_can_7491.CANMessage import CANMessage, RobotHeartbeat
from frc_can_7491.frc_enums import (
    frc_device_type,
    frc_manufacturer,
    frc_api_class,
    frc_api_index,
    frc_broadcast_message,
)
from frc_can_7491.frc_utils import frc_can
from frc_can_7491.can_enums_7491 import (
    can_7491_class,
    can_7419_index_info,
    can_7491_index_misc,
)

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/karlfl/7491_CircuitPython_FRCCAN.git"

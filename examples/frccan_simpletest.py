# SPDX-FileCopyrightText: Copyright (c) 2024 Karl Fleischmann for Team 7491 Cyber Soldiers
#
# SPDX-License-Identifier: MIT
import board
from digitalio import DigitalInOut, Direction

from frc_can_7491 import can_7491_class, can_7419_index_info
from frc_can_7491 import frc_device_type, frc_manufacturer
from frc_can_7491 import CANDevice
from frc_can_7491 import CANMessage

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

canDevice = CANDevice(
    dev_type=frc_device_type.IOBreakout,
    dev_manufacturer=frc_manufacturer.TeamUse,
    dev_number=5,
)

# TODO add routes to handle device number changes
# TODO define API IDs

# 'Heartbeat' messages
@canDevice.route(msg_type=CANMessage.Type.Heartbeat)
def heartbeat(message:CANMessage):  # pylint: disable=unused-argument
    # print("Heartbeat")
    # print("System Watchdog", message.Heartbeat.SystemWatchdog)
    return

# 'Broadcast' messages
@canDevice.route(msg_type=CANMessage.Type.Broadcast)
def broadcast(message:CANMessage):  # pylint: disable=unused-argument
    print("Broadcast")
    # print(bin(message.api_id))
    return

# Status Request 
@canDevice.route(api_id=0x00)
def update_status(message:CANMessage):  # pylint: disable=unused-argu4117
    # immediately send a status update 
    canDevice.send_message(
        can_7491_class.Informational, can_7419_index_info.StatusPost, message=b"Status01"
    )
    print("Device", hex(message.api_id))
    return

canDevice.start_listener()

while True:
    # Handle all imcoming messages using routes defined above
    canDevice.receive_messages()

    led.value = not led.value
    
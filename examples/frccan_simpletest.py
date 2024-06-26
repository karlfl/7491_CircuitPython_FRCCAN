# SPDX-FileCopyrightText: Copyright (c) 2024 Karl Fleischmann for Team 7491 Cyber Soldiers
#
# SPDX-License-Identifier: MIT
import board
from digitalio import DigitalInOut, Direction

from frc_can_7491 import CANDevice, FRCDeviceType, FRCManufacturer, CANMessage

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

canDevice = CANDevice(
    dev_type=FRCDeviceType.IOBreakout,
    dev_manufacturer=FRCManufacturer.TeamUse,
    dev_number=5,
)

# Heartbeat messages
@canDevice.route(msg_type=CANMessage.Type.Heartbeat)
def heartbeat(message: CANMessage):  # pylint: disable=unused-argument
    print("Heartbeat")
    # print("System Watchdog", message.Heartbeat.SystemWatchdog)


# Broadcast messages
@canDevice.route(msg_type=CANMessage.Type.Broadcast)
def broadcast(message: CANMessage):  # pylint: disable=unused-argument
    print("Broadcast")
    # print(bin(message.api_id))


# Status Request
@canDevice.route(api_id=0x00)
def update_status(message: CANMessage):  # pylint: disable=unused-argument
    # immediately send a status update
    canDevice.send_message(0, 1, message=b"Status01")
    print("Device", hex(message.api_id))


canDevice.start_listener()

while True:
    # Handle all imcoming messages using routes defined above
    canDevice.receive_messages()

    led.value = not led.value

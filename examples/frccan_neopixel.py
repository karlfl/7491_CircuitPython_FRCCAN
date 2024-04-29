# SPDX-FileCopyrightText: Copyright (c) 2024 Karl Fleischmann for Team 7491 Cyber Soldiers
#
# SPDX-License-Identifier: MIT
import board
from digitalio import DigitalInOut, Direction

from frc_can_7491 import frc_device_type, frc_manufacturer
from frc_can_7491 import CANDevice
from frc_can_7491 import CANMessage, RobotHeartbeat

is_enabled = False

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

# TODO read these values from a config file on the device
canDevice = CANDevice(
    dev_type=frc_device_type.IOBreakout,
    dev_manufacturer=frc_manufacturer.TeamUse,
    dev_number=5,
)

# TODO add routes to handle device number changes
# TODO define API IDs


# 'Heartbeat' messages
@canDevice.route(msg_type=CANMessage.Type.Heartbeat)
def heartbeat(message: CANMessage):  # pylint: disable=unused-argument
    global is_enabled 
    is_enabled = message.Heartbeat.IsEnabled
    print(message.Heartbeat.IsEnabled)
    # print(message.Heartbeat.SystemWatchdog)
    # print(bin(int.from_bytes(message.Data, sys.byteorder)))
    # print('\t', message.heartbeat.red_alliance)
    # print([int(v) for v in message.msg_data])
    # print("Heartbeat")
    return


# 'Broadcast' messages
@canDevice.route(msg_type=CANMessage.Type.Broadcast)
def broadcast(message: CANMessage):  # pylint: disable=unused-argument
    print("Broadcast")
    # print(bin(message.api_id))
    return


# Status Request
@canDevice.route(api_id=0x00)
def update_status(message: CANMessage):  # pylint: disable=unused-argu4117
    print("Status Requested")

    # immediately send a status update
    statusMessage = "Team7491"
    canDevice.send_message(0, 1, message=bytes(statusMessage, "utf-8"))
    print("Status Sent: ", statusMessage)
    # print('\t', message)
    return


# Set Device ID
@canDevice.route(api_id=0x10)
def set_device_number(message: CANMessage):  # pylint: disable=unused-argu4117
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Set Number of LEDs
@canDevice.route(api_id=0x11)
def set_num_leds(message: CANMessage):  # pylint: disable=unused-argument
    # pixel_num = int(CANMessage.Data)
    # pixels = AddressableLED(pixel_pin,pixel_num)

    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Chaos
@canDevice.route(api_id=0x20)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Rainbow
@canDevice.route(api_id=0x21)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Solid
@canDevice.route(api_id=0x22)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Blink
@canDevice.route(api_id=0x23)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Intensity
@canDevice.route(api_id=0x24)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Scanner
@canDevice.route(api_id=0x25)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Alternating
@canDevice.route(api_id=0x26)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return


# Pattern Chase
@canDevice.route(api_id=0x27)
def base(message: CANMessage):  # pylint: disable=unused-argument
    # print("Device", hex(message.api_id))
    # print('\t', message)
    return

canDevice.start_listener()

while True:
    # canDevice.send_message(
    #     frc_api_class.Ack, frc_api_index.SetReference, message=b"Team7491"
    # )

    # Handle all imcoming messages using routes defined above
    canDevice.receive_messages()

    led.value = not led.value

    # sleep(0.5)
    # print("Free", gc.mem_free())

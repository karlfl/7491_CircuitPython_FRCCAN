# SPDX-FileCopyrightText: Copyright (c) 2024 Karl Fleischmann for FRC Team 7411 Cyber Soldiers
#
# SPDX-License-Identifier: MIT
"""
`frc_can.CANRequest`
====================================================
FRC CAN Bus CAN Message class.

* Author(s): Karl Fleischmann
"""

from .frc_utils import frc_can
from .frc_enums import frc_manufacturer


class RobotHeartbeat:
    def __init__(self, data):
        self.raw_data = data
        self.raw_heartbeat = frc_can.parse_heartbeat(data)
        (
            match_time,
            match_number,
            replay_number,
            system_watchdog,
            test_mode,
            auto_mode,
            enabled,
            red_alliance,
        ) = self.raw_heartbeat

        self.system_watchdog = system_watchdog
        self.test_mode = test_mode
        self.auto_mode = auto_mode
        self.enabled = enabled
        self.red_alliance = red_alliance

    @property
    def SystemWatchdog(self):
        return self.system_watchdog

    @property
    def IsTestMode(self):
        return self.test_mode

    @property
    def IsAutoMode(self):
        return self.auto_mode

    @property
    def IsEnabled(self):
        return self.enabled

    @property
    def OnRedAlliance(self):
        return self.red_alliance

    def __repr__(self) -> str:
        return f"RobotHeartbeat{self.raw_heartbeat}"


class CANMessage:

    class Type:
        Broadcast = 0
        Heartbeat = 1
        Device = 2

    def __init__(
        self,
        api_id: int = 0x00,
        msg_type: Type = Type.Broadcast,
        raw_msg_id: bytes = None,
        raw_msg_data: bytes = None,
    ) -> None:
        self.msg_type = msg_type
        self.msg_data = raw_msg_data
        self.api_class = 0
        self.api_index = 0

        if raw_msg_id is None:
            self.api_id = api_id
            self.msg_type = msg_type
        else:
            # Parse message details from raw message id
            try:
                (
                    device_type,
                    mfg_code,
                    api_class,
                    api_index,
                    api_id,
                    device_number,
                ) = frc_can.can_id.parse(raw_msg_id)
            except:
                raise ValueError("Unparseable raw_msg_id: ", raw_msg_id)

            if mfg_code == frc_manufacturer.NI:
                self.api_id = 0x01
                self.msg_type = CANMessage.Type.Heartbeat
                self.heartbeat = RobotHeartbeat(self.msg_data)
            elif mfg_code == frc_manufacturer.Broadcast:
                self.api_id = 0x0
                self.msg_type = CANMessage.Type.Broadcast
            else:
                self.msg_type = CANMessage.Type.Device

            self.api_id = api_id
            self.api_class = api_class
            self.api_index = api_index

    @property
    def APIId(self):
        return self.api_id

    @property
    def APIClass(self):
        return self.api_class

    @property
    def APIIndex(self):
        return self.api_index

    @property
    def Data(self):
        return self.msg_data

    @property
    def Heartbeat(self) -> RobotHeartbeat:
        return self.heartbeat
    
    def __hash__(self) -> int:
        return hash(self.api_id) ^ hash(self.msg_type)

    def __eq__(self, other: "CANMessage") -> bool:
        return self.api_id == other.api_id and self.msg_type == other.msg_type

    def __repr__(self) -> str:
        return f"CANMessage(api_id={repr(self.api_id)}, msg_type={repr(self.msg_type)})"

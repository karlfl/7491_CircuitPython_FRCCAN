import board
import sys
from digitalio import DigitalInOut

try:
    from typing import Callable
except ImportError:
    pass

from adafruit_mcp2515 import MCP2515 as CAN
from adafruit_mcp2515.canio import Message, RemoteTransmissionRequest, Match, BusState

from .CANMessage import CANMessage
from .frc_enums import frc_app_ids
from .frc_utils import frc_can


class CANDevice:
    def __init__(
        self,
        dev_type: int,
        dev_manufacturer: int,
        dev_number: int,
        baud_rate=1_000_000,
        spi=board.SPI(),
        cs=board.CAN_CS,
    ) -> None:

        print("******************************************************")
        print("***  FRC CAN Device Initialization")
        print("******************************************************")
        print(f"***  Type:         {int(dev_type)}")
        print(f"***  Manufacturer: {int(dev_manufacturer)}")
        print(f"***  Number:       {int(dev_number)}")
        print("******************************************************")
        print("")

        # setup the CAN Bus
        self.cs = DigitalInOut(cs)
        self.cs.switch_to_output()
        self.can_bus = CAN(spi, self.cs, baudrate=baud_rate, debug=False)

        self.handlers = {}

        self.dev_mfg = dev_manufacturer
        self.dev_type = dev_type
        self.dev_num = dev_number

        self.enabled = False

        # create a device filter (type, mfg and number) to use when listening for packets
        # this will ignore the API_ID portion of the extended CAN id used by FRC
        # see https://docs.wpilib.org/en/stable/docs/software/can-devices/can-addressing.html for more details
        self.device_filter = frc_can.build_device_filter(
            dev_manufacturer, dev_type, dev_number
        )

    def get_device_filter_bin(self):
        return bin(self.device_filter)

    def route(
        self,
        api_id: int = frc_app_ids.heartbeat,
        msg_type: CANMessage.Type = CANMessage.Type.Device,
    ):
        """Decorator used to add a route to handle incoming CAN Messages.

        Parameters::
        :param int               api_id: API Class and API Index that this route will handle
        :param CANMessage.Type   method: Type of CAN message to handle for (i.e. Heartbeat, Device or Broadcast)

        Example::

            @server.route(path, method)
            def route_func(message):
                # route body handling message
        """

        if msg_type == CANMessage.Type.Broadcast:
            api_id = frc_app_ids.broadcast

        def route_decorator(func: Callable) -> Callable:
            self.handlers[CANMessage(api_id, msg_type)] = func
            return func

        return route_decorator

    def send_message(self, apiClass: int, apiIndex: int, message: bytes):
        send_success = False

        msg_id = frc_can.can_id.build(
            self.dev_type, self.dev_mfg, int(apiClass), int(apiIndex), self.dev_num
        )
        canMessage = Message(id=msg_id, data=message, extended=True)

        if self.can_bus.state in (BusState.ERROR_ACTIVE, BusState.ERROR_WARNING):
            try:
                send_success = self.can_bus.send(canMessage)
            except RuntimeError as ex:
                print("Unexpected error:", ex)
        else:
            print("CAN Bus is not active", self.can_bus.state)

        # print("Send Success:", send_success)
        return send_success

    def start_listener(self):
        """the MCP2515 has slots for 2 masks and 6 filters
        # mask-0 has 2 filter slots, mask-1 has 4 filter slots
        # you can use up to 6 matches (match = mask & filter)
        # the order of the match objects below matter
        # the first mask used in the array can only have 2 filters
        # the second mask used can have up to 4 filters
        # not passing in a mask will use an 'exact match' mask of all 1's
        # read the MCP2515 datasheet for more details on masks and filters.
        """
        self.listener = self.can_bus.listen(
            matches=[
                # Match FRC RIO Heartbeat using default mask (exact match)
                Match(
                    frc_can.matching.filters.heartbeat,
                    extended=True,
                ),
                # FRC Broadcast messages use the API_Index bits to indicate the message type
                # the remaining bits are set to 0
                # so this filter uses the type, manufacture and number match mask
                Match(
                    frc_can.matching.filters.broadcast,
                    mask=frc_can.matching.masks.type_mfg_num,
                    extended=True,
                ),
                # Device Match uses the type, manufacture and number match mask
                Match(
                    self.device_filter,
                    mask=frc_can.matching.masks.type_mfg_num,
                    extended=True,
                ),
            ],
            timeout=0.9,
        )
        print("***  Listening for Broadcast, Heartbeat and Device specific messages")
        print()

    def receive_messages(self):
        # receive CAN messages and split out the device, api and data values
        message_count = self.listener.in_waiting()
        # print(message_count, "messages received")

        for _i in range(message_count):
            msg = self.listener.receive()

            if isinstance(msg, Message):
                (
                    device_type,
                    mfg_code,
                    api_class,
                    api_index,
                    api_id,
                    device_number,
                ) = frc_can.can_id.parse(msg.id)

            if isinstance(msg, RemoteTransmissionRequest):
                print("RTR length:", msg.length)

            message = CANMessage(raw_msg_id=msg.id, raw_msg_data=msg.data)

            # If a routes exists for this message...
            route = self.handlers.get(message)
            if route:
                # call it
                route(message)
            else:
                # If not log an error.
                if message.api_id == frc_app_ids.heartbeat:
                    print("Handler Not Defined for FRC Heartbeat messages")
                elif message.api_id == frc_app_ids.broadcast:
                    print("Handler Not Defined for FRC Broadcast messages")
                    print(bin(msg.id), bin(int.from_bytes(msg.data, sys.byteorder)))
                else:
                    print(
                        "Handler Not Defined. API ID:",
                        hex(message.api_id),
                        "Message Type:",
                        message.msg_type,
                        bin(msg.id),
                    )

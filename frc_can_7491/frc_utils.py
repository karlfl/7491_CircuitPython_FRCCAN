import sys;

class frc_can:
    class matching:
        class masks:
            # when using match masks in CAN a bit value of ...
            #   1 = must match filter on this bit
            #   0 = ignore this bit 
            type_mfg_num     = 0b1111111111110000000000111111 # match everything but API Class and Index
            num_mask         = 0b0000000000000000000000111111 # match only device number
            api_class        = 0b0000000000001111110000000000 # match only API Class
            # exact_match      = 0b1111111111111111111111111111 # match everything exactly

        class filters:
            # Periodic Heartbeat CAN ID filter
            # Type= 1 (Robot Controller)
            # Manufacturer = 1 (NI)
            # API Class = 6 (Heartbeat)
            # API Index = 1 (Message)
            # Device Number = 0
            heartbeat    = 0b0001000000010001100001000000
            # Broadcast CAN ID filter
            # Type= 0 (Robot Controller)
            # Manufacturer = 0 (NI)
            # API Class = 0 (Heartbeat)
            # API Index = contains broadcast message
            # Device Number = 0
            broadcast    = 0b0000000000000000000000000000

    class bitmasks:
        # Bit masks for spliting out a 32bit binary field
        # see https://docs.wpilib.org/en/stable/docs/software/can-devices/can-addressing.html for more details
        device_type    = 0b1111100000000000000000000000  # bits 28-24
        mfg_code       = 0b0000011111111000000000000000  # bits 23-16
        api            = 0b0000000000000111111111100000  # bits 15-6
        api_class      = 0b0000000000000111111000000000  # bits 15-10
        api_index      = 0b0000000000000000000111100000  # bits 9-6
        device_number  = 0b0000000000000000000000011111  # bits 5-0

        # Bit masks for spliting out a 64bit binary field for heartbeat
        # see https://docs.wpilib.org/en/stable/docs/software/can-devices/can-addressing.html for more details
        match_time      = 0b1111111100000000000000000000000000000000000000000000000000000000  # bits 64-57 8 bits
        match_number    = 0b0000000011111111110000000000000000000000000000000000000000000000  # bits 56-47 10 bits
        replay_number   = 0b0000000000000000001111110000000000000000000000000000000000000000  # bits 46-41 6 bits
        tournament_type = 0b0000000000000000000000001110000000000000000000000000000000000000  # bits 40-38 3 bits

        system_watchdog = 0b0000000000000000000000000001000000000000000000000000000000000000  # bits 37 1 bit
        test_mode       = 0b0000000000000000000000000000100000000000000000000000000000000000  # bits 36 1 bit
        auto_mode       = 0b0000000000000000000000000000010000000000000000000000000000000000  # bits 35 1 bit
        enabled         = 0b0000000000000000000000000000001000000000000000000000000000000000  # bits 34 1 bit
        red_alliance    = 0b0000000000000000000000000000000100000000000000000000000000000000  # bits 33 1 bit
                        # 0b1111111100000000000000000001101111111100110100000100110010000110 Red Enabled Test
                        #                              STAER        
        datetime_year   = 0b0000000000000000000000000000000011111100000000000000000000000000  # bits 32-27 6 bits
        datetime_month  = 0b0000000000000000000000000000000000000011110000000000000000000000  # bits 26-23 4 bits
        datetime_day    = 0b0000000000000000000000000000000000000000001111100000000000000000  # bits 22-18 5 bits
        datetime_sec    = 0b0000000000000000000000000000000000000000000000011111100000000000  # bits 17-12 6 bits
        datetime_min    = 0b0000000000000000000000000000000000000000000000000000011111100000  # bits 11-6 6 bits
        datetime_hour   = 0b0000000000000000000000000000000000000000000000000000000000011111  # bits 5-0 5 bits

    def parse_heartbeat(bytes):
        # split the heartbeat id using bitwise AND with right shift
        msg = int.from_bytes(bytes, sys.byteorder)
        # print(bin(msg))
        match_time      = (msg & frc_can.bitmasks.match_time     ) >> 56
        match_number    = (msg & frc_can.bitmasks.match_number   ) >> 46
        replay_number   = (msg & frc_can.bitmasks.replay_number  ) >> 40
        tournament_type = (msg & frc_can.bitmasks.tournament_type) >> 37
        system_watchdog = (msg & frc_can.bitmasks.system_watchdog) >> 36
        test_mode       = (msg & frc_can.bitmasks.test_mode      ) >> 35
        auto_mode       = (msg & frc_can.bitmasks.auto_mode      ) >> 34
        enabled         = (msg & frc_can.bitmasks.enabled        ) >> 33
        red_alliance    = (msg & frc_can.bitmasks.red_alliance   ) >> 32
        datetime_year   = (msg & frc_can.bitmasks.datetime_year  ) >> 26
        datetime_month  = (msg & frc_can.bitmasks.datetime_month ) >> 22
        datetime_day    = (msg & frc_can.bitmasks.datetime_day   ) >> 17
        datetime_sec    = (msg & frc_can.bitmasks.datetime_sec   ) >> 11
        datetime_min    = (msg & frc_can.bitmasks.datetime_min   ) >> 5
        datetime_hour   = (msg & frc_can.bitmasks.datetime_hour  )
        # print (bin(api_class), bin(api_index), bin(api_id), api_id)
        # print(bin(device_type), bin(mfg_code), bin(api), bin(device_number))
        # print(device_type, mfg_code, api, device_number)

        return  (match_time, 
                match_number, 
                replay_number, 
                system_watchdog, 
                test_mode, 
                auto_mode, 
                enabled, 
                red_alliance,
                # tournament_type, 
                # datetime_year, datetime_month, datetime_day, 
                # datetime_sec, datetime_min, datetime_hour
        )

    # create a device filter (type, mfg and number)to use when listening for packets
    # this will ignore the API_ID portion of the extended CAN id used by FRC
    # see https://docs.wpilib.org/en/stable/docs/software/can-devices/can-addressing.html for more details
    def build_device_filter(dev_manufacturer, dev_type, dev_number):
        return (
            (dev_type << 24) | (dev_manufacturer << 16) | (0x00 << 6) | (dev_number)
        )
    
    class can_id:
        def parse(bytes):
            # split the message id using bitwise AND with right shift
            device_type     = (bytes & frc_can.bitmasks.device_type) >> 24
            mfg_code        = (bytes & frc_can.bitmasks.mfg_code) >> 16
            api_class       = (bytes & frc_can.bitmasks.api_class) >> 10
            api_index       = (bytes & frc_can.bitmasks.api_index) >> 6
            api_id          = (bytes & frc_can.bitmasks.api) >> 6
            device_number =    bytes & frc_can.bitmasks.device_number

            # print (bin(api_class), bin(api_index), bin(api_id), api_id)
            # print(bin(device_type), bin(mfg_code), bin(api), bin(device_number))
            # print(device_type, mfg_code, api, device_number)

            return device_type, mfg_code, api_class, api_index, api_id, device_number

        def build(dev_type, dev_mfg, api_class, api_index, dev_num):
            # combine the device info with the api id using bitwise AND with left shift
            device_bits = dev_type << 24
            mfg_code_bits = dev_mfg << 16
            api_class_bits = api_class << 10
            api_index_bits = api_index << 6
            api_id = (api_class_bits | api_index_bits) >> 6

            # print (bin(api_class), bin(api_index), bin(api_id), api_id)
            # print(bin(device_type), bin(mfg_code), bin(api), bin(device_number))
            # print(device_type, mfg_code, api, device_number)

            msg_id = (
                device_bits | mfg_code_bits | api_class_bits | api_index_bits | dev_num
            )
            return msg_id
        
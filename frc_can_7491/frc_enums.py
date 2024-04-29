class frc_app_ids:
    broadcast: int = 0x0
    heartbeat: int = 0x61


class frc_device_type:
    BroadcastMessages = 0
    RobotController = 1
    MotorController = 2
    RelayController = 3
    GyroSensor = 4
    Accelerometer = 5
    UltrasonicSensor = 6
    GearToothSensor = 7
    PowerDistributionModule = 8
    PneumaticsController = 9
    Miscellaneous = 10
    IOBreakout = 11
    FirmwareUpdate = 31


class frc_manufacturer:
    Broadcast = 0
    NI = 1
    LuminaryMicro = 2
    DEKA = 3
    CTRElectronics = 4
    REVRobotics = 5
    Grapple = 6
    MindSensors = 7
    TeamUse = 8
    KauaiLabs = 9
    Copperforge = 10
    PlayingWithFusion = 11
    Studica = 12
    TheThriftyBot = 13
    ReduxRobotics = 14
    AndyMark = 15
    VividHosting = 16


class frc_api_class:
    Informational = 0
    SpeedControlMode = 1
    VoltageCompensationMode = 2
    PositionControlMode = 3
    CurrentControlMode = 4
    Status = 5
    PeriodicStatus = 6
    Configuration = 7
    Ack = 8


class frc_api_index:
    StatusUpdate = 0
    DisableControl = 1
    SetSetpoint = 2
    PConstant = 3
    IConstant = 4
    DConstant = 5
    SetReference = 6
    TrustedEnable = 7
    TrustedSetNoAck = 8
    TrustedSetSetpointNoAck = 10
    SetSetpointNoAck = 1


class frc_broadcast_message:
    Disable = 0
    SystemHalt = 1
    SystemReset = 2
    DeviceAssign = 3
    DeviceQuery = 4
    Heartbeat = 5
    Sync = 6
    Update = 7
    FirmwareVersion = 8
    Enumerate = 9
    SystemResume = 10

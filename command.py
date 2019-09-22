class Command():
    Attention = 'AT'
    End = '\n'
    Error = 'ER'
    Okay = 'OK'
    # Info = 'HI'
    SetMode = 'SM'
    # GetMode = 'GM'
    SetRGB = 'SV' # (for Set Values)
    # GetRGB = 'GV' # (for Get Values)
    SetSpeed = 'SS'
    ToggleOnboardLED = 'TL'

    class Mode():
        """To be used after SetMode"""
        Steady = 'STD'
        Blink = 'BLK'
        Pulse = 'PLS'

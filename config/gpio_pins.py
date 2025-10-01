"""
GPIO Pin Configuration for Raspberry Pi Gaming Device
Modify these values to match your hardware setup
"""

BUTTONS = {
    'HOME': 17,
    'SELECT': 27,
    'START': 22,
    'POWER': 23,
    'FRIENDS': 24,
    'A': 5,
    'B': 6,
    'X': 13,
    'Y': 19,
    'L': 25,
    'R': 8,
}

DPAD = {
    'UP': 16,
    'DOWN': 20,
    'LEFT': 21,
    'RIGHT': 12,
}

JOYSTICKS = {
    'LEFT_X': 0,
    'LEFT_Y': 1,
    'RIGHT_X': 2,
    'RIGHT_Y': 3,
}

JOYSTICK_DEADZONE = 0.15
JOYSTICK_SENSITIVITY = 1.0

SCREENS = {
    'TOP_SCREEN': {
        'WIDTH': 800,
        'HEIGHT': 480,
        'TYPE': 'HDMI',
        'MODEL': 'Waveshare 5" HDMI LCD',
        'INTERFACE': 'HDMI',
        'FRAMEBUFFER': '/dev/fb0',
    },
    'BOTTOM_SCREEN': {
        'WIDTH': 320,
        'HEIGHT': 240,
        'TYPE': 'SPI_TFT',
        'MODEL': 'Adafruit 3.2" TFT (ILI9341)',
        'CONTROLLER': 'ILI9341',
        'INTERFACE': 'SPI',
        'FRAMEBUFFER': '/dev/fb1',
        'TOUCH_DEVICE': '/dev/input/event0',
        'SPI_SPEED': 64000000,
    }
}

TESTING_MODE = {
    'DUAL_HDMI': False,
    'HDMI_0_RESOLUTION': (800, 480),
    'HDMI_1_RESOLUTION': (320, 240),
}

LED_INDICATORS = {
    'POWER_LED': 26,
    'WIFI_LED': 7,
    'BLUETOOTH_LED': 11,
}

BACKLIGHT_CONTROL = {
    'TOP_SCREEN_PWM': 18,
    'BOTTOM_SCREEN_PWM': 14,
}

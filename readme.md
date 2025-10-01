# Nintendo 3DS-Inspired Gaming System for Raspberry Pi 4

## Project Overview
A complete gaming system UI built in Python/Pygame that mimics the Nintendo 3DS dual-screen interface. Designed to run on Raspberry Pi OS Lite with custom hardware (dual screens, buttons, joysticks, touchscreen).

## Current Status - First Version in development ⚠️

### ✅ Fully Working Features
- **Dual-Screen Layout**: Top screen (800x480) for content preview, bottom screen (320x240 touchscreen) for controls
- **Home Screen**: Status bar showing time, WiFi indicator, Bluetooth indicator, working app grid
- **Navigation**: Full keyboard and touch input support with proper coordinate handling for both screens
- **Quick-Access Bar**: Bottom toolbar with Friends, Notifications, Browser, and Menu buttons
- **Quick Menu**: Overlay with brightness/volume sliders (UI functional, system integration needs hardware)
- **Input System**: Complete button mapping for Home, Select, Start, Power, Friends, A/B/X/Y, L/R, D-pad, dual joysticks
- **GPIO Configuration**: Developer-friendly config file at `config/gpio_pins.py` for easy hardware customization
- **App Registry**: Modular system for registering and launching apps - working
- **On-Screen Keyboard**: Touch keyboard widget for text input in apps
- **Theme Engine**: 4 themes (Default Blue, Dark Mode, Nintendo Red, Forest Green) - working theme switching
- **Game Scanner**: Auto-detects games from /games folder with metadata support
- **Auto-Update Service**: Checks for git updates periodically
- **App Launching**: All apps launch and can be navigated with B button to go back

### ⚠️ Partially Implemented (UI Complete, Backend Needs Work)
- **Settings App**: UI with 12 sections ready, but WiFi/Bluetooth controls need system-level integration
- **Friends App**: UI complete with demo data, Supabase integration needs authentication setup
- **Chat App**: UI and keyboard working, Supabase real-time subscriptions need configuration
- **Browser App**: UI and URL bar working, but doesn't render actual webpages (would need webkit integration)
- **Music Player**: UI and controls complete, works with local audio files in data/music/ folder (pygame.mixer)
- **Notification System**: Service infrastructure ready, needs app integration

### 🔧 Requires Hardware/System Access
- **WiFi Management**: Needs NetworkManager or wpa_supplicant access on Raspberry Pi
- **Bluetooth Pairing**: Needs bluez and dbus access on Raspberry Pi
- **Brightness Control**: Needs PWM or backlight sysfs access on actual hardware
- **SPI Display**: Bottom screen will need ILI9341/ST7789 driver setup on actual hardware

## Project Structure
```
/
├── main.py                 # Main application entry point
├── config/
│   ├── gpio_pins.py       # Hardware pin configuration (customize for your setup)
│   └── settings.py        # System-wide settings
├── ui/
│   ├── screen_manager.py  # Dual-screen management
│   ├── input_handler.py   # Button/touch input handling
│   └── screens/
│       └── home.py        # Home screen with app grid
├── services/
│   ├── app_registry.py    # App registration and management
│   └── notification_service.py
├── apps/                   # Individual applications
│   ├── settings/
│   ├── music/
│   ├── friends/
│   ├── chat/
│   └── browser/
├── themes/                 # Custom themes
├── assets/                 # Icons, sounds, wallpapers
└── games/                  # Game installation directory

## Hardware Requirements

### Actual Hardware Specs
- **Raspberry Pi 4**

**Top Screen (Primary Display):**
- 4.3"–5" HDMI LCD (800×480 or 800×800, non-touch)
- Example: Waveshare 5" HDMI LCD 800×480
- Connection: HDMI port

**Bottom Screen (Secondary Display):**
- 3.2"–3.5" SPI TFT LCD with ILI9341 or ST7789 controller
- Example: Adafruit 3.2" TFT 320×240 (ILI9341)
- Connection: SPI interface (controlled via SPI, readable with PyQt UI)
- Touchscreen capable

**Controls:**
- Buttons: Home, Select, Start, Power, Friends, A, B, X, Y, L, R
- D-pad: Up, Down, Left, Right
- 2x Analog joysticks

### Testing with Dual HDMI (While Hardware is on Backorder)
You can test the UI using 2 HDMI displays connected to Raspberry Pi 4's dual HDMI ports.
See `TESTING_DUAL_HDMI.txt` for complete setup instructions.

## Button Controls
- **Home**: Return to main menu
- **Start**: Pause/options menu
- **Select**: Quick menu
- **Power**: Shutdown dialog
- **Friends**: Open friends list
- **A**: Confirm/select
- **B**: Back/cancel
- **X/Y**: Shortcuts (app-specific)
- **L/R**: Tab switching
- **D-pad**: Grid navigation
- **Joysticks**: Analog navigation and shortcuts

## Running the System
The system runs automatically via the "Gaming System" workflow:
```bash
python main.py
```

## Environment Variables
- `DATABASE_URL`: Supabase PostgreSQL connection string (for Friends/Chat features)
- `SESSION_SECRET`: Session encryption key

## Auto-Update Feature
The system includes an automatic update checker that:
- Checks for updates every hour (configurable)
- Pulls updates from the git repository
- Notifies users when updates are available
- Can be enabled/disabled in `config/settings.py`

To configure:
```python
SYSTEM = {
    'AUTO_UPDATE': True,
    'UPDATE_CHECK_INTERVAL': 3600,  # seconds
}
```

## Development Notes
- The system is designed for Raspberry Pi OS Lite (no desktop environment)
- Audio support is optional (gracefully handles missing audio devices)
- GPIO pins are configurable in `config/gpio_pins.py`
- Apps are modular and can be added to the registry
- Touch input is calibrated for centered bottom screen display
- Dual HDMI testing mode available while waiting for actual hardware

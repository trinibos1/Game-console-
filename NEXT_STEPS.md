# Next Steps for Full Feature Implementation

This document outlines what needs to be done to complete the partially implemented features.

## 1. Supabase Real-Time Integration

### What's Done:
- Database schema (SUPABASE_SCHEMA.sql)
- Basic Supabase client connection
- Demo UI for Friends and Chat apps

### What's Needed:
1. **Authentication Setup:**
   ```python
   # Add to supabase_service.py
   def sign_up(self, email, password, username):
       response = self.client.auth.sign_up({
           'email': email,
           'password': password,
           'options': {'data': {'username': username}}
       })
       return response
   
   def sign_in(self, email, password):
       response = self.client.auth.sign_in_with_password({
           'email': email,
           'password': password
       })
       return response
   ```

2. **Real-Time Subscriptions:**
   ```python
   # Subscribe to new messages
   def subscribe_to_messages(self, user_id, callback):
       channel = self.client.channel('messages')
       channel.on('postgres_changes', 
                  event='INSERT', 
                  schema='public', 
                  table='messages',
                  filter=f'receiver_id=eq.{user_id}',
                  callback=callback)
       channel.subscribe()
       return channel
   ```

## 2. Web Browser Implementation

### Current State:
- URL bar and bookmarks UI
- Touch keyboard integration

### Options for Full Browser:
1. **Use PyQt WebEngine (Recommended):**
   ```bash
   pip install PyQt5 PyQt5-WebEngine
   ```
   
2. **Use requests + BeautifulSoup for Simple HTML:**
   ```python
   import requests
   from bs4 import BeautifulSoup
   ```

3. **External Browser Launch:**
   ```python
   import subprocess
   subprocess.Popen(['chromium-browser', '--kiosk', url])
   ```

## 3. WiFi Management

### Requires:
- Root/sudo access
- NetworkManager or wpa_supplicant

### Implementation:
```python
import subprocess

def scan_wifi():
    result = subprocess.run(['nmcli', 'dev', 'wifi'], 
                          capture_output=True, text=True)
    return parse_wifi_list(result.stdout)

def connect_wifi(ssid, password):
    subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 
                   'password', password])
```

## 4. Bluetooth Management

### Requires:
- bluez installed
- bluetoothctl or Python pybluez

### Implementation:
```python
import bluetooth

def discover_devices():
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    return nearby_devices

def pair_device(address):
    # Use bluetoothctl via subprocess
    subprocess.run(['bluetoothctl', 'pair', address])
```

## 5. Hardware Brightness Control

### For Raspberry Pi:
```python
def set_brightness(value):
    # For DSI/HDMI displays
    with open('/sys/class/backlight/rpi_backlight/brightness', 'w') as f:
        f.write(str(value))
    
    # For SPI displays (Adafruit TFT)
    import board
    import digitalio
    led = digitalio.DigitalInOut(board.D18)
    led.direction = digitalio.Direction.OUTPUT
    # Use PWM for brightness control
```

## 6. Testing on Actual Hardware

### When Hardware Arrives:
1. Flash Raspberry Pi OS Lite
2. Install dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install python3-pygame python3-pip
   pip3 install -r requirements.txt
   ```

3. Configure SPI for bottom screen:
   ```bash
   sudo raspi-config
   # Enable SPI interface
   ```

4. Install Adafruit CircuitPython libraries:
   ```bash
   pip3 install adafruit-circuitpython-rgb-display
   ```

5. Set TESTING_MODE to False in config/gpio_pins.py

6. Connect GPIO buttons according to config/gpio_pins.py

## 7. Performance Optimization

### For Raspberry Pi 4:
- Enable GPU acceleration
- Optimize Pygame rendering
- Use proper framebuffer access
- Implement dirty rectangle rendering

## 8. Additional Features to Consider

### Game Installation:
- Add download manager
- Implement .zip extraction
- Auto-update game metadata

### Social Features:
- Voice chat integration
- Game invites
- Achievement system
- Leaderboards

### System Features:
- Screenshot capture
- Screen recording
- Cloud save sync
- Parental controls

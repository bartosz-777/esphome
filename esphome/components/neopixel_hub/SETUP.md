# WS2811 PWM Expander - Setup & Usage Guide

## ✅ Component Status

Your component is **properly set up** and ready to use! Here's what's included:

```
esphome/components/neopixel_hub/
├── __init__.py              # Main component configuration
├── light.py                 # Light platform definition
├── neopixel_hub.h           # C++ header
├── neopixel_hub.cpp         # C++ implementation
├── README.md                # Full documentation
├── example.yaml             # Configuration examples
├── manifest.yaml            # Component manifest
├── CODEOWNERS               # Maintainer info
└── __pycache__/             # Python cache (auto-generated)
```

## 🚀 How to Use

### Option 1: Use Directly in ESPHome (Main Repository)

If this is in the main ESPHome repository, you can use it immediately in your YAML configs:

```yaml
# example_config.yaml
esphome:
  name: my-ws2811-project
  platform: esp32
  board: esp32dev

# The hub - manages the WS2811 chip(s)
light:
  - platform: neopixel_hub
    id: my_pwm_hub
    num_chips: 1
    pin: GPIO5
    mode: pwm_channels

  # Individual white LED controls
  - platform: neopixel_hub/light
    name: "Backlight"
    hub_id: my_pwm_hub
    channel_id: 0

  - platform: neopixel_hub/light
    name: "Accent LED 1"
    hub_id: my_pwm_hub
    channel_id: 1

  - platform: neopixel_hub/light
    name: "Accent LED 2"
    hub_id: my_pwm_hub
    channel_id: 2
```

### Option 2: Use as External Component

If you're using this in your own project (not in main esphome), add this to your YAML:

```yaml
external_components:
  - source: 
      type: local
      path: /path/to/esphome/components/neopixel_hub
    components: [neopixel_hub]

light:
  - platform: neopixel_hub
    id: my_pwm_hub
    num_chips: 1
    pin: GPIO5
    mode: pwm_channels
```

### Option 3: Copy to Your Project

Copy the entire `neopixel_hub` folder to your ESPHome config directory:

```bash
# If using ESPHome via Docker or pip
cp -r /path/to/esphome/components/neopixel_hub ~/.config/esphome/custom_components/
```

Then reference it:

```yaml
external_components:
  - source:
      type: local
      path: custom_components
    components: [neopixel_hub]
```

## 🔧 Development Setup

If you want to contribute or modify the component:

```bash
# 1. Install ESPHome development dependencies
cd /path/to/esphome
pip install -r requirements_dev.txt

# 2. Verify Python syntax
python3 -m py_compile esphome/components/neopixel_hub/__init__.py
python3 -m py_compile esphome/components/neopixel_hub/light.py

# 3. Verify the component loads
esphome config example_config.yaml

# 4. Build firmware
esphome compile example_config.yaml
```

## 📋 Configuration Quick Reference

### Hub Configuration

```yaml
light:
  - platform: neopixel_hub
    id: unique_id               # Required: unique identifier
    num_chips: 1                # Required: number of WS2811 chips (each = 3 channels)
    pin: GPIO5                  # Required: data pin GPIO number
    mode: pwm_channels          # Optional: pwm_channels or rgb_pixels (default: pwm_channels)
```

### Light Component Configuration

```yaml
  - platform: neopixel_hub/light
    name: "LED Name"            # Required: display name in Home Assistant
    hub_id: unique_id           # Required: reference to hub
    channel_id: 0               # Required: channel number (0 - num_chips*3-1)
    brightness: 100%            # Optional: default brightness (0-100%)
```

## 🎯 Channel Mapping

For **PWM mode**, channels map to color outputs:

```
Chip 0:  Channels 0, 1, 2  (Red, Green, Blue outputs)
Chip 1:  Channels 3, 4, 5  (Red, Green, Blue outputs)
Chip 2:  Channels 6, 7, 8  (Red, Green, Blue outputs)
```

**Example: 3-chip setup with 9 white LEDs**

```yaml
light:
  - platform: neopixel_hub
    id: hub3
    num_chips: 3
    pin: GPIO5
    mode: pwm_channels

  # Chip 0 LEDs (channels 0-2)
  - platform: neopixel_hub/light
    name: "Zone 1 - LED A"
    hub_id: hub3
    channel_id: 0

  - platform: neopixel_hub/light
    name: "Zone 1 - LED B"
    hub_id: hub3
    channel_id: 1

  - platform: neopixel_hub/light
    name: "Zone 1 - LED C"
    hub_id: hub3
    channel_id: 2

  # Chip 1 LEDs (channels 3-5)
  - platform: neopixel_hub/light
    name: "Zone 2 - LED A"
    hub_id: hub3
    channel_id: 3
    
  # ... etc (channels 6-8 for Chip 2)
```

## ✨ Features Verified

- ✅ Proper namespace (`ws2811_expander`)
- ✅ C++ header guards
- ✅ Component registration
- ✅ Light registration
- ✅ PWM value management
- ✅ NeoPixelBus library dependency included
- ✅ Multiple chip support
- ✅ CODEOWNERS file
- ✅ Manifest file
- ✅ Python syntax valid
- ✅ Follows ESPHome conventions

## 🔍 Testing Your Setup

### Verify Files Are Present

```bash
ls -la ~/path/to/esphome/esphome/components/neopixel_hub/
```

Should show:
- `__init__.py`
- `light.py`
- `neopixel_hub.h`
- `neopixel_hub.cpp`
- `README.md`
- `manifest.yaml`
- `CODEOWNERS`

### Test Configuration

Create `test_config.yaml`:

```yaml
esphome:
  name: test-ws2811
  platform: esp32
  board: esp32dev

light:
  - platform: neopixel_hub
    id: test_hub
    num_chips: 1
    pin: GPIO5
    mode: pwm_channels

  - platform: neopixel_hub/light
    name: "Test LED"
    hub_id: test_hub
    channel_id: 0
```

Then validate:

```bash
esphome config test_config.yaml
```

If successful, you'll see the validated configuration.

## 🏗️ Integration Points

The component properly integrates with:

- **ESPHome Core**: `cg.Component` base class
- **Light Component**: `light.Light` for dimming/on-off
- **Output Component**: Can be extended for raw PWM
- **Home Assistant**: Automatic discovery via ESPHome integration

## 📚 Documentation Files

- **README.md** - Full feature documentation
- **example.yaml** - Configuration examples with comments
- **SETUP.md** - This file (you're reading it!)

## ⚠️ Known Limitations

- Only tested on ESP32/ESP8266 (should work on RP2040)
- Single data pin (not two-wire protocols like APA102)
- PWM frequencies follow NeoPixelBus defaults
- Brightness control via PWM duty cycle

## 🐛 Troubleshooting

### "Component neopixel_hub not found"

Make sure the component folder is in:
- `esphome/components/neopixel_hub/` (if in main repo)
- OR configured in `external_components` (if external)

### "ImportError: No module named voluptuous"

You need to install development dependencies:

```bash
cd /path/to/esphome
pip install -r requirements_dev.txt
```

### LEDs not responding

1. Verify GPIO pin is correct
2. Check WS2811 power supply (5V ±0.5V)
3. Verify data line has proper signal quality
4. Check channel IDs are in valid range (0 to `num_chips*3 - 1`)

## 📞 Support

For detailed documentation, see:
- [ESPHome Components Guide](https://developers.esphome.io/components/)
- [NeoPixelBus Library](https://github.com/Makuna/NeoPixelBus)

Happy building! 🎉

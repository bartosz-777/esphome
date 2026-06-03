# WS2811 PWM Expander Component

A powerful ESPHome component that repurposes WS2811 LED controller chips as **PWM expanders**. Each WS2811 chip provides 3 independent PWM channels (Red, Green, Blue) that can each independently control white LEDs or other PWM devices.

## Features

- **PWM Expander Mode**: Use WS2811 chips as 3-channel PWM controllers
- **Independent Channel Control**: Each color channel (R, G, B) is a separate controllable light
- **Multiple Chips**: Chain multiple WS2811 chips for up to 510 PWM channels (170 chips)
- **White LED Support**: Perfect for controlling white LEDs with independent brightness
- **Simple Configuration**: Easy YAML-based setup
- **Home Assistant Integration**: Each channel appears as an independent light entity

## How It Works

### Traditional Use (Addressable RGB LEDs)
WS2811 chips are normally used to control addressable RGB LED strips where each LED is a full RGB pixel.

### PWM Expander Mode (This Component)
This component repurposes the WS2811 to act as a PWM expander:
- Each WS2811 chip outputs 3 independent PWM signals (one for each color channel)
- These PWM signals can drive white LEDs, DC motors, heaters, or any PWM device
- Each channel is independently controllable
- Multiple chips can be chained together

## Hardware Setup

### Single Chip Setup
```
ESP32/ESP8266
    |
    +---> GPIO5 (Data Pin) ---> WS2811 Chip
                                  |
                                  +---> Red PWM ---> White LED 1
                                  +---> Green PWM ---> White LED 2
                                  +---> Blue PWM ---> White LED 3
```

### Multiple Chips (Chained)
```
ESP32/ESP8266
    |
    +---> GPIO5 (Data Pin) ---> WS2811 Chip 1 ---> WS2811 Chip 2 ---> WS2811 Chip 3
                                  |                  |                  |
                                  +-> 3 Channels    +-> 3 Channels    +-> 3 Channels
```

## Channel Mapping

For **PWM mode**, channels are indexed as follows:

```
Chip 0:  Channels 0, 1, 2  (R, G, B outputs)
Chip 1:  Channels 3, 4, 5  (R, G, B outputs)
Chip 2:  Channels 6, 7, 8  (R, G, B outputs)
...
```

## Configuration

### Basic Hub Setup (PWM Mode)

```yaml
light:
  - platform: neopixel_hub
    id: my_pwm_hub
    num_chips: 1              # Number of WS2811 chips (each chip = 3 channels)
    pin: GPIO5                # Data pin
    mode: pwm_channels        # Use as PWM expander
```

### Individual LED Configuration

```yaml
light:
  # White LED 1 - uses Chip 0, Red channel
  - platform: neopixel_hub/light
    name: "White LED 1"
    hub_id: my_pwm_hub
    channel_id: 0

  # White LED 2 - uses Chip 0, Green channel
  - platform: neopixel_hub/light
    name: "White LED 2"
    hub_id: my_pwm_hub
    channel_id: 1

  # White LED 3 - uses Chip 0, Blue channel
  - platform: neopixel_hub/light
    name: "White LED 3"
    hub_id: my_pwm_hub
    channel_id: 2
```

### Configuration with Multiple Chips

```yaml
light:
  - platform: neopixel_hub
    id: pwm_hub_multi
    num_chips: 3              # 3 chips = 9 total channels
    pin: GPIO5
    mode: pwm_channels

  # Chip 0 channels
  - platform: neopixel_hub/light
    name: "Strip 1 LED"
    hub_id: pwm_hub_multi
    channel_id: 0

  - platform: neopixel_hub/light
    name: "Strip 2 LED"
    hub_id: pwm_hub_multi
    channel_id: 1

  - platform: neopixel_hub/light
    name: "Strip 3 LED"
    hub_id: pwm_hub_multi
    channel_id: 2

  # Chip 1 channels
  - platform: neopixel_hub/light
    name: "Room 1 LED"
    hub_id: pwm_hub_multi
    channel_id: 3

  - platform: neopixel_hub/light
    name: "Room 2 LED"
    hub_id: pwm_hub_multi
    channel_id: 4

  - platform: neopixel_hub/light
    name: "Room 3 LED"
    hub_id: pwm_hub_multi
    channel_id: 5

  # Chip 2 channels (add more as needed)
  # ...
```

## Home Assistant Integration

Each PWM channel appears as a separate light entity in Home Assistant:

- `light.white_led_1`
- `light.white_led_2`
- `light.white_led_3`

Each light supports:
- On/Off control
- Brightness dimming (0-100%)
- Automation triggers and actions

## Automations & Scripts

Control each LED independently:

```yaml
automation:
  - trigger: homeassistant
    action:
      light.turn_on:
        entity_id: light.white_led_1
        brightness_pct: 75

  - trigger: homeassistant
    action:
      light.turn_off:
        entity_id: light.white_led_2
```

Fade effect:

```yaml
script:
  fade_white_led:
    sequence:
      - repeat:
          count: 20
          sequence:
            - light.turn_on:
                entity_id: light.white_led_1
                brightness_pct: !lambda "return int(100 * (loop.index / 20.0));"
            - delay: 100ms
```

## Platform Support

- **ESP32**: Full support with GPIO pins
- **ESP8266**: Full support with GPIO pins
- **RP2040**: Should work (not tested)

## Performance Considerations

- Each update to any channel sends all channel values to the WS2811 chips
- Suitable for up to 170 chips (510 channels) with typical performance
- Update frequency depends on ESP microcontroller speed (typically 100s of Hz)
- Low power consumption compared to driving loads directly from GPIO

## Troubleshooting

### LEDs not lighting up

1. Verify the correct GPIO pin is configured
2. Ensure WS2811 data line is connected to the specified GPIO pin
3. Check power supply voltage and current capacity
4. Verify WS2811 chip is powered and has GND connection to ESP32/ESP8266

### Flickering or unstable brightness

- Ensure adequate power supply (especially with multiple LEDs at high brightness)
- Verify data line signal quality (consider adding a series resistor on the data line)
- Reduce number of simultaneous updates if possible

### Wrong brightness or not fully bright

- Verify WS2811 power supply voltage (typically 5V ±0.5V)
- Check for voltage drop over data line (add resistor if needed)

## Advantages Over GPIO PWM

- **More Channels**: One WS2811 chip provides 3 channels vs 1 per GPIO pin
- **Chainable**: Connect multiple chips without using more GPIO pins
- **Signal Integrity**: WS2811 handles signal regeneration between chips
- **Flexibility**: Mix and match different loads on each channel

## Future Enhancements

- RGBW support with white channel
- Animation effects and color transitions
- PWM frequency customization
- Duty cycle ramping and fading built-in


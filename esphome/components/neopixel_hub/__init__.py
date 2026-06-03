"""ESPHome WS2811 PWM Expander Component - Uses WS2811 chips as PWM controllers."""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import light, output
from esphome.const import (
    CONF_CHANNEL,
    CONF_ID,
    CONF_OUTPUT_ID,
    CONF_PIN,
    Framework,
)
from esphome.core import CORE

# Constants
CONF_NUM_CHIPS = "num_chips"
CONF_CHANNEL_ID = "channel_id"
CONF_PWM_EXPANDER = "pwm_expander"
CONF_MODE = "mode"

# Modes for operation
MODE_RGB_PIXELS = "rgb_pixels"  # Traditional addressable RGB LEDs
MODE_PWM_CHANNELS = "pwm_channels"  # Use as PWM expander (each chip = 3 PWM outputs)

ws2811_expander_ns = cg.esphome_ns.namespace("ws2811_expander")
WS2811Hub = ws2811_expander_ns.class_("WS2811Hub", cg.Component)
WS2811PWMOutput = ws2811_expander_ns.class_("WS2811PWMOutput", output.FloatOutput)
WS2811Light = ws2811_expander_ns.class_("WS2811Light", light.LightOutput)

# Hub Configuration Schema
HUB_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(WS2811Hub),
        cv.Required(CONF_PIN): pins.internal_gpio_output_pin_number,
        cv.Required(CONF_NUM_CHIPS): cv.positive_not_null_int,
        cv.Optional(CONF_MODE, default=MODE_PWM_CHANNELS): cv.one_of(
            MODE_RGB_PIXELS, MODE_PWM_CHANNELS, lower=True
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


CONFIG_SCHEMA = HUB_SCHEMA


async def to_code(config):
    """Generate C++ code for hub."""
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    num_chips = config[CONF_NUM_CHIPS]
    cg.add(var.set_num_chips(num_chips))
    cg.add(var.set_data_pin(config[CONF_PIN]))

    mode = config[CONF_MODE]
    if mode == MODE_PWM_CHANNELS:
        cg.add(var.set_mode("PWM_CHANNELS"))
    else:
        cg.add(var.set_mode("RGB_PIXELS"))

    # Add NeoPixelBus library
    if CORE.is_esp32:
        cg.add_build_flag("-DESP32_ARDUINO_NO_RGB_BUILTIN")
        cg.add_library("makuna/NeoPixelBus", "2.8.0")
    else:
        cg.add_library("makuna/NeoPixelBus", "2.7.3")

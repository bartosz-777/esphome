"""ESPHome NeoPixel Hub Component - Uses WS2811 chips as PWM controllers."""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import output
from esphome.const import (
    CONF_ID,
    CONF_OUTPUT_ID,
    CONF_PIN,
)
from esphome.core import CORE

# Constants
CONF_NUM_CHIPS = "num_chips"
CONF_CHANNEL_ID = "channel_id"
CONF_MODE = "mode"

# Modes for operation
MODE_RGB_PIXELS = "rgb_pixels"
MODE_PWM_CHANNELS = "pwm_channels"

# Define namespace and classes
neopixel_hub_ns = cg.esphome_ns.namespace("neopixelhub")
NeoPixelHub = neopixel_hub_ns.class_("NeoPixelHub", cg.Component)
# NeoPixelChannel = neopixel_hub_ns.class_("NeoPixelHub::Channel", output.FloatOutput)

# Hub Configuration Schema (for neopixel_hub platform)
CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(NeoPixelHub),
        cv.Required(CONF_PIN): pins.gpio_output_pin_schema,
        cv.Required(CONF_NUM_CHIPS): cv.int_range(min=1, max=15),
        cv.Optional(CONF_MODE, default=MODE_PWM_CHANNELS): cv.one_of(
            MODE_RGB_PIXELS, MODE_PWM_CHANNELS, lower=True
        ),
    }
).extend(cv.COMPONENT_SCHEMA)


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

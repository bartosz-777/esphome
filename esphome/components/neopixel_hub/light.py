"""Individual WS2811 PWM Light Component - Control white LEDs via PWM channels."""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light
from esphome.const import CONF_OUTPUT_ID
from . import CONF_CHANNEL_ID, WS2811Hub, WS2811Light


# Light configuration schema for individual PWM channels
CONFIG_SCHEMA = light.LIGHT_SCHEMA.extend(
    {
        cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(WS2811Light),
        cv.GenerateID("hub_id"): cv.use_id(WS2811Hub),
        cv.Required(CONF_CHANNEL_ID): cv.positive_int,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    """Generate C++ code for PWM-based white light."""
    hub = await cg.get_variable(config["hub_id"])
    
    # Create light output instance
    light_var = cg.new_Pvariable(
        config[CONF_OUTPUT_ID],
        hub,
        config[CONF_CHANNEL_ID],
    )
    await light.register_light(light_var, config)

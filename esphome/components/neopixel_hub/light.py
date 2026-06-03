"""Individual WS2811 PWM Light Component - Control white LEDs via PWM channels."""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import light
from esphome.const import CONF_OUTPUT_ID
from . import LIGHT_SCHEMA, CONF_CHANNEL_ID, WS2811Hub, WS2811Light


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
    await cg.register_component(light_var, config)


CONFIG_SCHEMA = LIGHT_SCHEMA

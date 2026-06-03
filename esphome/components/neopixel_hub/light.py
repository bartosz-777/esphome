"""Individual WS2811 PWM Channel Component - Control white LEDs via PWM outputs."""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import output
from esphome.const import CONF_OUTPUT_ID
from . import CONF_CHANNEL_ID, NeoPixelHub, NeoPixelChannel


# Output configuration schema for individual PWM channels
CONFIG_SCHEMA = output.FLOAT_OUTPUT_SCHEMA.extend(
    {
        cv.GenerateID(CONF_OUTPUT_ID): cv.declare_id(NeoPixelChannel),
        cv.GenerateID("hub_id"): cv.use_id(NeoPixelHub),
        cv.Required(CONF_CHANNEL_ID): cv.positive_int,
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    """Generate C++ code for PWM-based channel output."""
    hub = await cg.get_variable(config["hub_id"])
    
    # Create channel output instance
    output_var = cg.new_Pvariable(config[CONF_OUTPUT_ID])
    await output.register_output(output_var, config)
    
    cg.add(output_var.set_parent(hub))
    cg.add(output_var.set_channel_id(config[CONF_CHANNEL_ID]))

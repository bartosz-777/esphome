#pragma once

#include "esphome/core/component.h"
#include "esphome/components/light/light_output.h"
#include "esphome/core/hal.h"
#include "esphome/components/output/float_output.h"
#include <NeoPixelBus.h>
#include <memory>
#include <vector>
#include <array>

namespace esphome {
namespace neopixel_hub {

enum class WS2811Mode {
  RGB_PIXELS,      // Treat as addressable RGB LEDs
  PWM_CHANNELS,    // Treat each chip as 3 independent PWM outputs (R, G, B)
};

class neopixel_hub : public Component {
 public:
  class Channel;
  neopixel_hub() = default;

  void setup() override;
  void dump_config() override;
  void loop() override;

  void set_num_chips(uint8_t num_chips) { this->num_chips_ = num_chips; }
  void set_data_pin(uint8_t pin) { this->data_pin_ = pin; }
  void set_mode(const std::string &mode_str) {
    this->mode_ = (mode_str == "PWM_CHANNELS") ? WS2811Mode::PWM_CHANNELS : WS2811Mode::RGB_PIXELS;
  }

  // PWM mode: set channel value (0-255)
  void set_channel_value(uint16_t channel_id, uint8_t value);
  
  // RGB pixel mode: set pixel color
  void set_pixel_color(uint16_t pixel_index, uint8_t r, uint8_t g, uint8_t b);

  uint16_t get_total_channels() const { return this->num_chips_ * 3; }
  uint16_t get_total_pixels() const { return this->num_chips_; }

 protected:
  uint8_t num_chips_{1};
  uint8_t data_pin_{0};
  WS2811Mode mode_{WS2811Mode::PWM_CHANNELS};
  
  // Buffer for PWM values: each chip has 3 channels (R, G, B)
  std::vector<uint8_t> pwm_values_;
  
  // NeoPixelBus instance - can hold up to 510 LEDs (170 chips * 3 channels)
  std::unique_ptr<NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod>> bus_;
  
  bool needs_update_{true};

class Channel : public output::FloatOutput {
 public:
  void set_parent(neopixel_hub *hub) { hub_ = hub; }
  void set_channel(uint16_t channel) { channel_id_ = channel; }

 protected:
  void write_state(float state) override {
    auto amount = static_cast<uint8_t>(state * 255);
    this->hub_->set_channel_value(channel_id_, amount);
  }

  neopixel_hub *hub_;
  uint16_t channel_id_;
};

    void set_pixel_color(uint16_t pixel_index, uint8_t r, uint8_t g, uint8_t b);

    GPIOPin *data_pin_;
    uint8_t num_chips_;
    WS2811Mode mode_;
    std::vector<uint8_t> pwm_values_;
    std::unique_ptr<NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod>> bus_;
    bool needs_update_;

};

}  // namespace neopixel_hub
}  // namespace esphome

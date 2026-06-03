#include "neopixel_hub.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include <cstring>

namespace esphome {
namespace ws2811_expander {

static const char *const TAG = "ws2811_expander";

void WS2811Hub::setup() {
  uint16_t total_channels = this->get_total_channels();
  
  ESP_LOGCONFIG(TAG, "Setting up WS2811 Hub:");
  ESP_LOGCONFIG(TAG, "  Mode: %s", this->mode_ == WS2811Mode::PWM_CHANNELS ? "PWM_CHANNELS" : "RGB_PIXELS");
  ESP_LOGCONFIG(TAG, "  Chips: %u", this->num_chips_);
  ESP_LOGCONFIG(TAG, "  Total Channels: %u", total_channels);
  ESP_LOGCONFIG(TAG, "  Data Pin: GPIO%u", this->data_pin_);
  
  // Initialize PWM buffer
  this->pwm_values_.resize(total_channels, 0);
  
  // Initialize NeoPixelBus
  // Each channel is represented as one "pixel" in the bus
  try {
    this->bus_ = std::make_unique<NeoPixelBus<NeoGrbFeature, Neo800KbpsMethod>>(
        total_channels, this->data_pin_);
    
    if (this->bus_) {
      this->bus_->Begin();
      ESP_LOGD(TAG, "NeoPixelBus initialized with %u channels", total_channels);
    }
  } catch (const std::exception &e) {
    ESP_LOGE(TAG, "Failed to initialize NeoPixelBus: %s", e.what());
  }
}

void WS2811Hub::dump_config() {
  ESP_LOGCONFIG(TAG, "WS2811 Hub:");
  ESP_LOGCONFIG(TAG, "  Mode: %s", this->mode_ == WS2811Mode::PWM_CHANNELS ? "PWM_CHANNELS" : "RGB_PIXELS");
  ESP_LOGCONFIG(TAG, "  Chips: %u", this->num_chips_);
  ESP_LOGCONFIG(TAG, "  Data Pin: GPIO%u", this->data_pin_);
}

void WS2811Hub::loop() {
  if (this->needs_update_ && this->bus_) {
    this->bus_->Show();
    this->needs_update_ = false;
  }
}

void WS2811Hub::set_channel_value(uint16_t channel_id, uint8_t value) {
  if (channel_id >= this->pwm_values_.size()) {
    ESP_LOGW(TAG, "Channel ID %u out of range (max %zu)", channel_id, this->pwm_values_.size() - 1);
    return;
  }
  
  this->pwm_values_[channel_id] = value;
  
  if (!this->bus_) {
    return;
  }
  
  // In PWM mode, we use RGB channels to represent PWM duty cycles
  // Each "pixel" in the bus represents a PWM channel
  // We set the pixel color based on the duty cycle
  if (this->mode_ == WS2811Mode::PWM_CHANNELS) {
    // Channel format: each channel becomes an R, G, or B value
    // Channel 0 = Chip 0 Red, Channel 1 = Chip 0 Green, Channel 2 = Chip 0 Blue
    // etc.
    this->bus_->SetPixelColor(channel_id, RgbColor(value, 0, 0));
  }
  
  this->needs_update_ = true;
}

void WS2811Hub::set_pixel_color(uint16_t pixel_index, uint8_t r, uint8_t g, uint8_t b) {
  if (pixel_index >= this->num_chips_) {
    ESP_LOGW(TAG, "Pixel index %u out of range (max %u)", pixel_index, this->num_chips_ - 1);
    return;
  }
  
  if (!this->bus_) {
    return;
  }
  
  this->bus_->SetPixelColor(pixel_index, RgbColor(r, g, b));
  this->needs_update_ = true;
}

void WS2811Light::setup() {
  ESP_LOGCONFIG(TAG, "WS2811 Light Channel %u", this->channel_id_);
}

void WS2811Light::dump_config() {
  ESP_LOGI(TAG, "WS2811 Light Channel #%u", this->channel_id_);
}

light::LightTraits WS2811Light::get_traits() const {
  auto traits = light::LightTraits();
  traits.set_supports_brightness(true);
  traits.set_supports_rgb(false);  // PWM channels are white-only
  traits.set_supports_color_temperature(false);
  traits.set_supports_white_value(true);
  return traits;
}

void WS2811Light::write_state(const light::LightState *state) {
  float brightness = state->get_brightness();
  bool on = state->is_on();
  
  if (!on) {
    // Turn off channel
    this->hub_->set_channel_value(this->channel_id_, 0);
  } else {
    // Get brightness (0.0 - 1.0) and scale to 0-255
    uint8_t pwm_value = static_cast<uint8_t>(brightness * 255.0f);
    this->hub_->set_channel_value(this->channel_id_, pwm_value);
  }
}

}  // namespace ws2811_expander
}  // namespace esphome


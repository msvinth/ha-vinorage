"""Light platform for vinorage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    LightEntity,
)
from homeassistant.components.light.const import ColorMode

from .entity import VinorageEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import VinorageDataUpdateCoordinator
    from .data import VinorageConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: VinorageConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the light platform."""
    async_add_entities([VinorageLight(coordinator=entry.runtime_data.coordinator)])


class VinorageLight(VinorageEntity, LightEntity):
    """Vinorage LED light class."""

    _attr_color_mode = ColorMode.BRIGHTNESS
    _attr_supported_color_modes = {ColorMode.BRIGHTNESS}
    _attr_name = "LED Light"
    _attr_icon = "mdi:lightbulb"

    def __init__(self, coordinator: VinorageDataUpdateCoordinator) -> None:
        """Initialize the light."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_light"

    @property
    def brightness(self) -> int | None:
        """Return the brightness of this light between 0..255."""
        if self.coordinator.data is None:
            return None
        # Convert from 0-100 to 0-255
        brightness_pct = self.coordinator.data.get("led_brightness", 0)
        return round(brightness_pct * 255 / 100)

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        if self.coordinator.data is None:
            return False
        return self.coordinator.data.get("led_brightness", 0) > 0

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn on the light."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        # Convert from 0-255 to 0-100
        brightness_pct = round(brightness * 100 / 255)

        client = self.coordinator.config_entry.runtime_data.client
        await client.async_set_led_brightness(brightness_pct)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the light."""
        client = self.coordinator.config_entry.runtime_data.client
        await client.async_set_led_brightness(0)
        await self.coordinator.async_request_refresh()

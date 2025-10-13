"""Cover platform for vinorage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.cover import (
    CoverDeviceClass,
    CoverEntity,
    CoverEntityFeature,
)

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
    """Set up the cover platform."""
    async_add_entities([VinorageCover(coordinator=entry.runtime_data.coordinator)])


class VinorageCover(VinorageEntity, CoverEntity):
    """Vinorage cellar cover class."""

    _attr_device_class = CoverDeviceClass.DAMPER
    _attr_supported_features = (
        CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE | CoverEntityFeature.STOP
    )
    _attr_name = "Wine Cellar"
    _attr_icon = "mdi:elevator"

    def __init__(self, coordinator: VinorageDataUpdateCoordinator) -> None:
        """Initialize the cover."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_cover"

    @property
    def is_closed(self) -> None:
        """
        Return if the cover is closed.

        Since we cannot determine the state, return None to indicate unknown.
        """
        return None

    async def async_open_cover(self, **_: Any) -> None:
        """Open the cover (raise the cellar)."""
        client = self.coordinator.config_entry.runtime_data.client
        await client.async_control_actuator(1)

    async def async_close_cover(self, **_: Any) -> None:
        """Close the cover (lower the cellar)."""
        client = self.coordinator.config_entry.runtime_data.client
        await client.async_control_actuator(2)

    async def async_stop_cover(self, **_: Any) -> None:
        """Stop the cover."""
        client = self.coordinator.config_entry.runtime_data.client
        await client.async_control_actuator(0)

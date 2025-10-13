"""Custom types for vinorage."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import VinorageApiClient
    from .coordinator import VinorageDataUpdateCoordinator


type VinorageConfigEntry = ConfigEntry[VinorageData]


@dataclass
class VinorageData:
    """Data for the Vinorage integration."""

    client: VinorageApiClient
    coordinator: VinorageDataUpdateCoordinator
    integration: Integration

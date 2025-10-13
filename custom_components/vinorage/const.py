"""Constants for vinorage."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "vinorage"
ATTRIBUTION = "Data provided by Vinorage wine cellar"

# Configuration
CONF_SCAN_INTERVAL = "scan_interval"
DEFAULT_SCAN_INTERVAL = 15  # seconds

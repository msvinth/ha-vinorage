"""Adds config flow for Vinorage."""

from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    VinorageApiClient,
    VinorageApiClientCommunicationError,
    VinorageApiClientError,
)
from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER

SCAN_INTERVAL_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_SCAN_INTERVAL,
        ): selector.NumberSelector(
            selector.NumberSelectorConfig(
                min=0,
                max=300,
                step=1,
                unit_of_measurement="seconds",
                mode=selector.NumberSelectorMode.BOX,
            ),
        ),
    },
)


class VinorageFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Vinorage."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,  # noqa: ARG004
    ) -> VinorageOptionsFlowHandler:
        """Get the options flow handler."""
        return VinorageOptionsFlowHandler()

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_connection(
                    host=user_input[CONF_HOST],
                )
            except VinorageApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "cannot_connect"
            except VinorageApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                # Use the IP address as the unique ID
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=f"Vinorage ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_HOST,
                        default=(user_input or {}).get(CONF_HOST, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Optional(
                        CONF_SCAN_INTERVAL,
                        default=(user_input or {}).get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ): selector.NumberSelector(
                        selector.NumberSelectorConfig(
                            min=0,
                            max=300,
                            step=1,
                            unit_of_measurement="seconds",
                            mode=selector.NumberSelectorMode.BOX,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def async_step_reconfigure(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle reconfiguration of the host address."""
        _errors = {}
        reconfigure_entry = self._get_reconfigure_entry()

        if user_input is not None:
            try:
                await self._test_connection(host=user_input[CONF_HOST])
            except VinorageApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "cannot_connect"
            except VinorageApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_HOST])
                self._abort_if_unique_id_configured()
                return self.async_update_reload_and_abort(
                    reconfigure_entry,
                    title=f"Vinorage ({user_input[CONF_HOST]})",
                    data_updates=user_input,
                )

        reconfigure_schema = vol.Schema(
            {
                vol.Required(
                    CONF_HOST,
                ): selector.TextSelector(
                    selector.TextSelectorConfig(
                        type=selector.TextSelectorType.TEXT,
                    ),
                ),
            },
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=self.add_suggested_values_to_schema(
                reconfigure_schema,
                {CONF_HOST: reconfigure_entry.data.get(CONF_HOST)},
            ),
            errors=_errors,
        )

    async def _test_connection(self, host: str) -> None:
        """Validate the connection to the device."""
        client = VinorageApiClient(
            host=host,
            session=async_get_clientsession(self.hass),
        )
        await client.async_get_data()


class VinorageOptionsFlowHandler(config_entries.OptionsFlowWithReload):
    """Handle options flow for Vinorage (auto-reloads on change)."""

    async def async_step_init(
        self,
        user_input: dict | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Manage the scan interval option."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=self.add_suggested_values_to_schema(
                SCAN_INTERVAL_SCHEMA,
                {
                    CONF_SCAN_INTERVAL: self.config_entry.options.get(
                        CONF_SCAN_INTERVAL,
                        self.config_entry.data.get(
                            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
                        ),
                    ),
                },
            ),
        )

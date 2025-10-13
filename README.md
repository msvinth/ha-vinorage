# Vinorage Wine Cellar Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

A custom Home Assistant integration for controlling [Vinorage](https://vinorage.dk/en/) wine cellars with elevation.

## About Vinorage

Vinorage manufactures premium wine storage solutions with built-in elevation systems that allow wine cellars to be mounted flush with the floor and raised when needed. This integration allows you to control your Vinorage wine cellar directly from Home Assistant.

## Compatibility

This integration has been tested with:
- **[Vinorage Wine Cellar with Elevation (200 bottles)](https://vinorage.dk/en/produkt/vinorage-wine-cellar-with-elevation-exclusive-and-optimal-wine-storage/)** - Exclusive model with elevation system

Other Vinorage models with similar web-based control interfaces may also work, but have not been tested.

## Features

This integration provides control over two main components of your Vinorage wine cellar:

### 🔆 LED Light Control
- **Entity Type**: Light
- **Features**:
  - Brightness control (0-100%)
  - On/Off control
  - Current brightness state monitoring

### �� Wine Cellar Elevation
- **Entity Type**: Cover
- **Features**:
  - Raise cellar (Open)
  - Lower cellar (Close)
  - Stop movement
  - Stateless operation (position not tracked)

### ⚙️ Configuration Options
- **IP Address**: Local network address of your Vinorage device
- **Scan Interval**: How often to poll the device for LED status (default: 15 seconds, set to 0 to disable)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/msvinth/ha-vinorage`
6. Select category "Integration"
7. Click "Add"
8. Click "Install" on the Vinorage card
9. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/msvinth/ha-vinorage/releases)
2. Extract the `vinorage` folder from the archive
3. Copy the `vinorage` folder to your Home Assistant's `custom_components` directory
4. Restart Home Assistant

## Configuration

### Adding the Integration

1. In Home Assistant, go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Vinorage"
4. Enter your Vinorage device's local IP address (e.g., `192.168.1.100`)
5. Optionally adjust the scan interval (default: 15 seconds)
6. Click **Submit**

### Finding Your Device's IP Address

Your Vinorage wine cellar must be connected to your local network. You can find its IP address by:
- Checking your router's connected devices list
- Using a network scanning app
- Checking your DHCP server logs

**Note**: It's recommended to assign a static IP address to your Vinorage device in your router settings to prevent the IP from changing.

## Usage

### LED Light

Once configured, you'll see a light entity named **"LED Light"**:

```yaml
# Example automation to turn on LED at 50% brightness
automation:
  - alias: "Wine cellar ambient lighting"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: light.turn_on
        target:
          entity_id: light.vinorage_led_light
        data:
          brightness_pct: 50
```

### Wine Cellar Cover

The cover entity **"Wine Cellar"** controls the elevation:

```yaml
# Example automation to raise cellar when someone approaches
automation:
  - alias: "Raise wine cellar"
    trigger:
      - platform: state
        entity_id: binary_sensor.wine_room_motion
        to: "on"
    action:
      - service: cover.open_cover
        target:
          entity_id: cover.vinorage_wine_cellar

# Don't forget to lower it after a delay
  - alias: "Lower wine cellar"
    trigger:
      - platform: state
        entity_id: binary_sensor.wine_room_motion
        to: "off"
        for:
          minutes: 5
    action:
      - service: cover.close_cover
        target:
          entity_id: cover.vinorage_wine_cellar
```

## Entities Created

| Entity ID | Type | Description |
|-----------|------|-------------|
| `light.vinorage_led_light` | Light | Controls LED brightness |
| `cover.vinorage_wine_cellar` | Cover | Controls cellar elevation |

## Technical Details

### Polling

The integration polls the device at the configured interval to update the LED brightness state. The cellar position is not tracked as the device does not provide position feedback.

## Troubleshooting

### Integration won't connect

- Verify the IP address is correct
- Ensure the device is powered on and connected to your network
- Try accessing `http://[IP_ADDRESS]` in a web browser to verify the device responds
- Check that Home Assistant can reach the device (same network/VLAN)

### LED state not updating

- Check the scan interval is not set to 0
- Verify the device is responding (check in a web browser)
- Look at Home Assistant logs for any error messages

### Cover position shows as "Unknown"

This is normal behavior. The Vinorage device does not report position, so the cover entity is stateless.

## Development

### Setting up Development Environment

This repository includes a devcontainer for easy development:

```bash
# Clone the repository
git clone https://github.com/msvinth/ha-vinorage
cd ha-vinorage

# Open in VS Code with devcontainer
code .
```

### Running Home Assistant

```bash
# Start Home Assistant in development mode
scripts/develop
```

### Linting

```bash
# Run linters
scripts/lint
```

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Support

If you encounter any issues or have questions:
- Check the [troubleshooting section](#troubleshooting) above
- Search [existing issues](https://github.com/msvinth/ha-vinorage/issues)
- Open a [new issue](https://github.com/msvinth/ha-vinorage/issues/new) with detailed information

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This is an unofficial integration and is not affiliated with, endorsed by, or supported by Vinorage. Use at your own risk.

## Credits

- Integration developed by [msvinth](https://github.com/msvinth)
- Built using the [Home Assistant Integration Blueprint](https://github.com/ludeeus/integration_blueprint)

---

**Enjoy your perfectly stored wine! 🍷**

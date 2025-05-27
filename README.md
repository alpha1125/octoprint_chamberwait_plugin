# ChamberWait Plugin for OctoPrint
Developed for a Raspberry Pi 3B, but should work with any modern pi, running OctoPrint, this plugin integrates a DS18B20 digital temperature sensor via the 1-Wire interface. It enables conditional G-code execution based on ambient chamber temperature, allowing prints to automatically pause and wait until a specified temperature threshold is reached before continuing.

## Out Of Scope
Setting up your DS18B20 sensor and configuring your Raspberry Pi to read from it. It's assumed you've got a working 1-Wire setup.

## Key Features:
Monitors a DS18B20 sensor directly from the Pi (e.g., /sys/bus/w1/devices/.../w1_slave)

Introduces a custom G-code command (@CHAMBERWAIT <temp>) to pause printing until the chamber reaches the desired temperature

Implements a dedicated thread to monitor temperature independently of the print loop

Handles cancellation and cleanup if the print is aborted mid-wait

Logs temperature progress and plugin activity for debugging and diagnostics

Ideal for enclosed 3D printing environments (e.g., ASA/ABS), where consistent chamber heat is critical for print quality.
This plugin pauses the print when it encounters the `@CHAMBERWAIT <temp>` command in the G-code. It monitors the chamber temperature using a DS18B20 sensor and resumes the print once the target temperature is reached.

## Installation

1. Clone this repository into your OctoPrint plugins directory:

   ```bash
   git clone https://github.com/alpha1125/octoprint_chamberwait_plugin
   ```
 
2.	Restart OctoPrint.


## Usage

Add the following lines to your G-code at the desired point:
```gcode
M117 Waiting for chamber heat 40°C
@CHAMBERWAIT 40
M117 Starting to print...
```

The plugin will pause the print when it encounters @CHAMBERWAIT 40, monitor the chamber temperature, and resume printing once the temperature reaches 40°C.

## Configuration
Your DS18B20 sensor will have a different device path, update the sensor_path in the plugin settings accordingly.

---

## ✅ Final Notes

- **Threading**: The plugin uses a separate thread to monitor the temperature, ensuring that the main OctoPrint process remains responsive.

- **Logging**: Detailed logs are provided for monitoring and debugging purposes.

- Ensure that your DS18B20 sensor is properly connected and that the necessary kernel modules (`w1_gpio` and `w1_therm`) are loaded on your Raspberry Pi.

## License
AGPL-3.0
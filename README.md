# OctoPrint-ChamberWait

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

- **Extensibility**: You can enhance the plugin by adding a settings interface to configure the sensor path or by supporting multiple sensors.

Ensure that your DS18B20 sensor is properly connected and that the necessary kernel modules (`w1_gpio` and `w1_therm`) are loaded on your Raspberry Pi.

Let me know if you need assistance with packaging this plugin or adding a settings interface! 
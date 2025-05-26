import octoprint.plugin
import re
import time
import threading
import logging


class ChamberWaitPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.TemplatePlugin,
    octoprint.plugin.SettingsPlugin
):

    def __init__(self):
        self._logger = logging.getLogger("octoprint.plugins.chamberwait")
        self._chamber_thread = None
        self._pause_event = threading.Event()
        self._resume_event = threading.Event()
        self._target_temp = None
        self._sensor_path = "/sys/bus/w1/devices/28-5c190087bd28/w1_slave"
        self._stop_event = threading.Event()

    def get_settings_defaults(self):
        return {
            "sensor_path": self._sensor_path
        }

    def on_after_startup(self):
        self._logger.info("ChamberWait Plugin started. Monitoring for @CHAMBERWAIT commands.")


    def read_chamber_temp(self):
        try:
            with open(self._sensor_path, 'r') as f:
                lines = f.readlines()
                if lines[0].strip()[-3:] != 'YES':
                    return None
                equals_pos = lines[1].find('t=')
                if equals_pos != -1:
                    temp_string = lines[1][equals_pos + 2:]
                    temp_c = float(temp_string) / 1000.0
                    return temp_c
                return None
        except Exception as e:
            self._logger.error(f"Error reading temperature: {e}")
            return None

    def monitor_chamber_temp(self, target_temp):
        self._logger.info(f"Monitoring chamber temperature until it reaches {target_temp}°C.")
        while not self._stop_event.is_set():
            current_temp = self.read_chamber_temp()
            if current_temp is not None:
                self._printer.commands(f"M117 Chamber Temp {current_temp:.2f}C/{target_temp:.2f}C")
                self._logger.info(f"M117 Chamber Temp {current_temp:.2f}C/{target_temp:.2f}C")
                if current_temp >= target_temp:
                    self._logger.info("Target chamber temperature reached. Resuming print.")
                    self._printer.commands("M117 Starting to print...")
                    self._stop_event.set()
                    self._printer.resume_print()
                    break
            else:
                self._logger.error("Chamber temperature read failed. Cancelling print.")
                self._stop_event.set()
                self._printer.cancel_print()
                break

            time.sleep(5)

    def gcode_queuing_handler(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
        match = re.match(r"@CHAMBERWAIT\s+(\d+)", cmd)
        if match:
            self._stop_event.clear()

            self._target_temp = int(match.group(1))
            self._logger.info(f"Detected @CHAMBERWAIT command with target temperature: {self._target_temp}°C")
            self._logger.info("Will pause print, until chamber reaches target temperature.")
            self._printer.pause_print()

            # Ensure previous thread is stopped before starting a new one
            if self._chamber_thread and self._chamber_thread.is_alive():
                self._logger.info("Waiting for previous chamber monitoring thread to finish.")
                self._stop_event.set()
                self._chamber_thread.join()
                self._logger.info("Previous chamber monitoring thread stopped.")
            self._stop_event.clear()
            self._chamber_thread = threading.Thread(target=self.monitor_chamber_temp, args=(self._target_temp,))
            self._chamber_thread.start()

            return None  # Prevent this command from being sent to the printer
        return cmd

    ##~~ Softwareupdate hook

    def get_update_information(self):
        return {
            "chamberwait": {
                "displayName": "ChamberWait Plugin",
                "displayVersion": self._plugin_version,
                "type": "github_release",
                "user": "alpha1125",
                "repo": "OctoPrint-ChamberWait",
                "current": self._plugin_version,
                "pip": "https://github.com/alpha1125/OctoPrint-ChamberWait/archive/{target_version}.zip"
            }
        }

    def on_print_cancelled(self):
        self._logger.info("Print cancelled. Stopping chamber temperature monitoring.")
        self._stop_event.set()
        if self._chamber_thread and self._chamber_thread.is_alive():
            self._logger.info("Waiting for chamber monitoring thread to stop after cancellation.")
            self._chamber_thread.join()
            self._logger.info("Chamber monitoring thread stopped.")
        self._chamber_thread = None

__plugin_implementation__ = ChamberWaitPlugin()
__plugin_name__ = "ChamberWait Plugin"
__plugin_version__ = "0.0.1"
__plugin_description__ = "Pauses print until chamber reaches target temperature."
__plugin_pythoncompat__ = ">=3,<4"
__plugin_hooks__ = {
    "octoprint.comm.protocol.gcode.queuing": __plugin_implementation__.gcode_queuing_handler
}

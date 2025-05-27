from setuptools import setup

plugin_identifier = "chamberwait"
plugin_package = "octoprint_chamberwait"
plugin_name = "OctoPrint-ChamberWait"
plugin_version = "0.1.0"
plugin_description = "Pauses print until chamber reaches target temperature. Reading  DS18B20 temperature sensor via GPIO."
plugin_author = "Lloyd Leung"
plugin_author_email = "you@example.com"
plugin_url = "https://github.com/alpha1125/octoprint_chamberwait_plugin"
plugin_license = "AGPLv3"
plugin_requires = []

setup(
    name=plugin_name,
    version=plugin_version,
    description=plugin_description,
    author=plugin_author,
    author_email=plugin_author_email,
    url=plugin_url,
    license=plugin_license,
    packages=[plugin_package],
    include_package_data=True,
    install_requires=plugin_requires,
    entry_points={
        "octoprint.plugin": [f"{plugin_identifier} = {plugin_package}"]
    },
)
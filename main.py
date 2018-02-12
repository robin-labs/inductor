import json
import os

import click

import wpa_supplicant

def is_root():
	return os.getuid() == 0

def get_valid_device_names(devices):
	return [device["name"] for device in devices]

def get_device_by_name(devices, name):
	for device in devices:
		if device["name"] == name:
			return device
	return None

@click.command()
@click.argument("config-path")
@click.argument("device-name", required=False)
@click.option("-i", "--install-conf", is_flag=True)
@click.option("-g", "--go-intent", default=0, type=click.Choice(xrange(16)))
def main(config_path, device_name, install_conf, go_intent):
	if not is_root():
		print "Please run this script as root."
		return
	config = json.loads(open(config_path).read())
	networks, devices = config["networks"], config["devices"]
	device = get_device_by_name(devices, device_name)
	if device is None:
		if len(devices) == 1:
			device = devices[0]
			print "Selecting only listed device: %s" % (device["name"])
		else:
			print "Please specify a valid device from the following: %s" % (
				", ".join(get_valid_device_names(devices))
			)
			return
	if install_conf:
		print "Installing wpa_supplicant.conf..."
		wpa_supplicant.install_wpa_supplicant(networks, device)

if __name__ == "__main__":
	main()
WPA_SUPPLICANT = "/etc/wpa_supplicant/wpa_supplicant.conf"

CONF_TEMPLATE = """
ctrl_interface=DIR=/var/run/wpa_supplicant 
update_config=1

%s

ap_scan=1
device_name=RPi_3
device_type=1-0050F204-1
driver_param=use_p2p_group_interface=1
driver_param=p2p_device=1
p2p_go_intent=%s
p2p_go_ht40=1
"""

NET_TEMPLATE = """
network={
	ssid="%s"
	psk="%s"
	key_mgmt=WPA-PSK
}
"""


def install_wpa_supplicant(*args, **kwargs):
	open(WPA_SUPPLICANT, "w").write(generate_wpa_supplicant(*args, **kwargs))

def generate_wpa_supplicant(networks, device):
	return CONF_TEMPLATE % (
		"\n".join([
			generate_network_entry(net) 
			for net in networks
		]),
		str(device["go-intent"])
	)

def generate_network_entry(network):
	ssid = network["ssid"].replace("\"", "\\\"")
	psk = network["psk"].replace("\"", "\\\"")
	return NET_TEMPLATE % (ssid, psk)

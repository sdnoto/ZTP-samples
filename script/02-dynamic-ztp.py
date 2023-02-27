from cli import configure, cli
from xml.dom import minidom
import re
import json
import urllib2

CONFIG_SERVER='10.13.2.150:1880'

USER="nohsadmin"
PASSWORD="cisco"
ENABLE="cisco"

def base_config():
    configure(['hostname switch-ztp'])
    configure(['username {} privilege 15 password {}'.format(USER,PASSWORD)])
    configure(['enable secret {}'.format(ENABLE)])
    configure(['line vty 0 4', 'login local'])

def get_serials():
    # xml formatted
    inventory = cli('show inventory | format')
    # skip leading newline
    doc = minidom.parseString(inventory[1:])
    serials =[]
    for node in doc.getElementsByTagName('InventoryEntry'):
        # router, what if there are several?
        chassis = node.getElementsByTagName('ChassisName')[0]
        if chassis.firstChild.data == "Chassis":
            serials.append(node.getElementsByTagName('SN')[0].firstChild.data)

        # switch
        match = re.match('"Switch ([0-9])"', chassis.firstChild.data)
        if match:
            serials.append(node.getElementsByTagName('SN')[0].firstChild.data)

    return serials

def get_my_config(serials):
    # define your own REST API CALL
    base = 'http://{}:1880/device?serial='.format(CONFIG_SERVER)
    url =  base + '&serial='.join(serials)
    print(url)
    configs = json.load(urllib2.urlopen(url))
    return configs

def configure_network(**kwargs):
    if 'ip' in kwargs and kwargs['ip'] is not None:
        print(kwargs['ip'])
        configure(['int g0/0','ip address {} {}'.format(kwargs['ip'], kwargs['netmask'])])
        configure(['ip route vrf Mgmt-vrf 0.0.0.0 0.0.0.0 {}'.format(kwargs['gw'])])


base_config()
serials = get_serials()
config = get_my_config(serials)
configure_network(**config)

print ("\n\n *** Executing show platform  *** \n\n")
cli_command = "show platform" 
cli.executep(cli_command)

print ("\n\n *** Executing show version *** \n\n")
cli_command = "show version"                  
cli.executep(cli_command)

print ("\n\n *** Configuring a Loopback Interface *** \n\n")
cli.configurep(["interface loop 100", "ip address 10.10.10.10 255.255.255.255", "end"])


print ("\n\n *** Executing show ip interface brief  *** \n\n")
cli_command = "sh ip int brief"                       
cli.executep(cli_command)

print ("\n\n *** ZTP Day0 Python Script Execution Complete *** \n\n")

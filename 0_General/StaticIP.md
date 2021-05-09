# RasPi - Set Up Static IP:

### TASKS:
1.) Get current router (**network IP**):
```
ip r | grep default
```

2.) Get current DNS server (**nameserver IP**):
```
sudo nano /etc/resolv.conf
```
Note the IP next to “nameserver“

3.) Modify the “dhcpcd.conf” configuration file:
```
sudo nano /etc/dhcpcd.conf
```

4.) Within this file, enter the following lines:

* Replace “**NETWORK**” with either “eth0” (Ethernet) **OR** you “wlan0” (WiFi)
* Replace “**STATICIP**” with the IP address that you want to assign
* Replace “**ROUTERIP**” with the network IP address
*  Replace “**DNSIP**" with the IP of the domain name server
	* either the IP you got in step 2 of this tutorial or another one such as Googles “8.8.8.8” or Cloudflare’s “1.1.1.1“
```
interface <NETWORK>
static ip_address=<STATICIP>/24
static routers=<ROUTERIP>
static domain_name_servers=<DNSIP>
```
5.) Save the file and reboot

---
### Test Static IP:
```
hostname -I
```
Check that the new IP is listed...

---
#### Summary:
| Label:			| Option:				| 
| -| -| 
| interface		| eth0 / wlan0 			|
| STATICIP		| IP you want to assign 	|
| network IP		| IP Retrieved? 		|
| DNS / nameserver 	| 192.168.0.1 / 8.8.8.8 / 1.1.1.1	|


#### Example static IP configurations:
```
interface wlan0								# eth0 / wlan0
static ip_address=192.168.0.10/24			# New IP to assign
static routers=192.168.0.1					# network IP ? ?
static domain_name_servers=192.168.0.1		# DNS nameserver 
```
```
interface wlan0
static ip_address=192.168.0.10/24
static routers=192.168.0.1
static domain_name_servers=8.8.8.8
```
```
interface eth0
static ip6_address=fd51:42f8:caae:d92e::ff/64
static routers=192.168.0.1
static domain_name_servers=fd51:42f8:caae:d92e::1
```


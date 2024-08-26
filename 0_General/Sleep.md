# Screensaver - Sleep Mode - Blank Screen

### XSET:

**To see all commands:**

	xset -?
	or
	man xset

**To see current settings:**

	DISPLAY=:0 xset q

---
### Disable Sleep Mode Completely:

	sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

Should look like the following:

	@lxpanel --profile LXDE-pi
	@pcmanfm --desktop --profile LXDE-pi
	@xset s noblank
	@xset s off
	@xset -dpms
	# @xscreensaver -no-splash
	@point-rpi

---
### Disable & Enable Screen Blanking:

Turn blanking off:

	xset dpms 0 0 0

Turn blanking on with 15 min timeout:

	xset dpms 0 0 900

---
#### xset Errors:

If using LCD Display:

	Error: xset: unable to open display ""

Need to set which display to use:

	export DISPLAY=:0
	# If error persists
	xset:  unable to open display ":0"

**OR** 

Can try **vbetool** instead:

	sudo vbetool dpms off

**OR**

	sudo nano /etc/lightdm/lightdm.conf
	
Add the following lines to the [SeatDefaults] section:

	# don't sleep the screen
	xserver-command=X -s 0 dpms

---
### OTHER OPTIONS:

To view system blanking:

	cat /sys/module/kernel/parameters/consoleblank

Set the system blanking time:

	setterm -blank 600
	or
	setterm -blank 0
	
**Note:** '0' should be blanking disabled.

#### Graphical Settings for Screen Saver:
**(Only works with HDMI)**

	sudo apt install xscreensaver

Start Menu-> preferences -> Xscreensaver


---
#### Backlight Dimmer:
**(2020) - untested**

[GITHUB Installation instructions](https://github.com/DougieLawson/backlight_dimmer)

**Note:** Not working on RPi4?
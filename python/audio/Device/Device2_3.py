# -*- coding: utf-8 -*-
"""
Output of 'Device2_3.py' looks like this:

  0 HDA Intel PCH: 92HD93BXX Analog (hw:0,0), ALSA (2 in, 0 out)
  1 HDA Intel PCH: HDMI 0 (hw:0,3), ALSA (0 in, 8 out)
  2 HDA Intel PCH: HDMI 1 (hw:0,7), ALSA (0 in, 8 out)
  3 HDA Intel PCH: HDMI 2 (hw:0,8), ALSA (0 in, 8 out)
  4 Samson Meteorite Mic: USB Audio (hw:1,0), ALSA (2 in, 0 out)
  5 sysdefault, ALSA (128 in, 0 out)
  6 hdmi, ALSA (0 in, 8 out)
  7 pulse, ALSA (32 in, 32 out)
* 8 default, ALSA (32 in, 32 out)
"""

def main():
    import sounddevice as sd
    print(sd.query_devices())

if __name__ == "__main__": main()
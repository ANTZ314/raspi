# -*- coding: utf-8 -*-
""" 
Output of 'Device2.py' looks like this:

ALSA lib pcm_dmix.c:1029:(snd_pcm_dmix_open) unable to open slave
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.rear
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.center_lfe
ALSA lib pcm.c:2266:(snd_pcm_open_noupdate) Unknown PCM cards.pcm.side
ALSA lib pcm_route.c:867:(find_matching_chmap) Found no matching channel map
ALSA lib pcm_dmix.c:1029:(snd_pcm_dmix_open) unable to open slave
(0, 'HDA Intel PCH: 92HD93BXX Analog (hw:0,0)', 2)
(1, 'HDA Intel PCH: HDMI 0 (hw:0,3)', 0)
(2, 'HDA Intel PCH: HDMI 1 (hw:0,7)', 0)
(3, 'HDA Intel PCH: HDMI 2 (hw:0,8)', 0)
(4, 'Samson Meteorite Mic: USB Audio (hw:1,0)', 2)
(5, 'sysdefault', 128)
(6, 'hdmi', 0)
(7, 'pulse', 32)
(8, 'default', 32)
"""

import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
  dev = p.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))
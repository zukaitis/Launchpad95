from _Framework.ControlSurface import ControlSurface

class StatusTransmitter(object):
	def __init__(self, control_surface = None):
		self._control_surface = control_surface

	def send_track_name(self, name):
		name = 't' + name
		self.transmit_string(name)
		#self._control_surface.show_message("kaimas:" + name)

	def send_clip_name(self, name):
		name = 'c' + name
		self.transmit_string(name)
		#self._control_surface._send_midi((240, 0, 32, 41, 2, 24, 20) +  tuple(ord(c) for c in name) + (247,))

	def send_device_name(self, name):
		name = 'd' + name
		#self._control_surface.show_message("kaimas:" + name)
		self.transmit_string(name)

	def transmit_string(self, str):
		self._control_surface._send_midi((240, 0, 32, 41, 2, 24, 20) + tuple(ord(c) for c in str) + (247,))
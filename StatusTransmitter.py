from threading import Timer

def debounce(wait):
	""" Decorator that will postpone a functions
		execution until after wait seconds
		have elapsed since the last time it was invoked. """

	def decorator(fn):
		def debounced(*args, **kwargs):
			def call_it():
				fn(*args, **kwargs)

			try:
				debounced.t.cancel()
			except(AttributeError):
				pass
			debounced.t = Timer(wait, call_it)
			debounced.t.start()

		return debounced
	return decorator

class StatusTransmitter(object):
	def __init__(self, control_surface = None):
		self._control_surface = control_surface

	@debounce(0.1)
	def send_track_name(self, name):
		name = 't' + name
		self.transmit_string(name)

	@debounce(0.2)
	def send_clip_name(self, name):
		name = 'c' + name
		self.transmit_string(name)

	@debounce(0.2)
	def send_device_name(self, name):
		name = 'd' + name
		self.transmit_string(name)

	@debounce(0.2)
	def send_status(self, is_playing, is_recording, is_session_recording):
		status_string = 's'
		status_string += 'P' if is_playing else '-'
		status_string += 'R' if is_recording else '-'
		status_string += 'S' if is_session_recording else '-'
		status_string += '-' # leaving one byte for future uses
		self.transmit_string(status_string)

	@debounce(0.2)
	def send_timing(self, tempo, signature_numerator, signature_denominator, nudge_down, nudge_up):
		timing_string = 'T'
		timing_string += str(int(tempo)).zfill(3)
		timing_string += str(signature_numerator).zfill(2)
		timing_string += str(signature_denominator).zfill(2)
		timing_string += 'D' if nudge_down else ('U' if nudge_up else '-')
		self.transmit_string(timing_string)

	def transmit_string(self, str):
		self._control_surface._send_midi((240, 0, 32, 41, 2, 24, 20) + tuple(ord(c) for c in str) + (247,))
		#self._control_surface.show_message("debug:" + str)


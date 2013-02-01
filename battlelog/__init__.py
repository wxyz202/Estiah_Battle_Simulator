import sys

_log_active = True

def log(s):
	if _log_active:
		sys.stdout.write(s)

def log_close():
	global _log_active
	_log_active = False

def log_open():
	global _log_active
	_log_active = True

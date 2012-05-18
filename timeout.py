#!/usr/local/bin/python
"""Usage: timeout.py [timeout] [command]
	timeout in seconds before killing [command]
	command is any command (and arguments) that you wish to timeout"""
import datetime, os, signal, subprocess, sys, time

# how long (in seconds) between sigterm and sigkill
SIGTERM_TO_SIGKILL = 1

def timeout_command(cmd, timeout):
	start = datetime.datetime.now()
	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	while process.poll() is None:
		now = datetime.datetime.now()
		if (now - start).seconds >= timeout:
			os.kill(process.pid, signal.SIGTERM)
			sys.stderr.write('TIMEOUT %s second%s, sent sigterm to %s %s\n' %(str(timeout), '' if timeout==1 else 's', process.pid, ' '.join(cmd)))
			time.sleep(SIGTERM_TO_SIGKILL)
			if process.poll() is None:
				os.kill(process.pid, signal.SIGKILL)
				sys.stderr.write('process still running, sent sigkill to %s %s\n' %(process.pid, ' '.join(cmd)))
				os.waitpid(-1, os.WNOHANG)
			return 2
		time.sleep(0.1)
	sys.stdout.write(process.stdout.read())
	sys.stderr.write(process.stderr.read())
	return 0

def main(argv=None):
	try:
		if "-h" in argv or "--help" in argv:
			print __doc__
			return 0
		return timeout_command(sys.argv[2:], int(argv[1]))
	except:
		print >>sys.stderr, __doc__
		return 2

if __name__ == '__main__':
	sys.exit(main(sys.argv))


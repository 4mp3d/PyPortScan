import argparse
import socket

parser = argparse.ArgumentParser(description='Port scan and banner grab an IP address.')
parser.add_argument('-i', '--ipaddress', type=str, required=True, help='IP Address you want to scan.')
parser.add_argument('-lp', '--lowport', type=int, default=1, help='Low TCP port for range. Default is 1.')
parser.add_argument('-hp', '--highport', type=int, default=1024, help='High TCP port for range. Default is 1024.')
args = parser.parse_args()

class Scanner:
	def __init__(self, ip):
		self.ip = ip
		self.open_ports = [];

	def __repr__(self):
		return 'Scanner: {}'.format(self.ip)

	def add_port(self, port):
		self.open_ports.append(port)

	def scan(self, lowerport, upperport):
		for port in range(lowerport, upperport + 1):
			if self.is_open(port):
				self.add_port(port)

	def is_open(self, port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = s.connect_ex((self.ip, port))
		s.close
		return result == 0

	def write(self, filepath):
		openport = map(str, self.open_ports)
		with open(filepath, 'w') as f:
			f.write('\n'.join(openport))

class Grabber:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.settimeout(0.5)
		self.socket.connect((self.ip, self.port))

	def read(self, length=1024):
		return self.socket.recv(length)

	def close(self):
		self.socket.close()

def main():
	ip = args.ipaddress
	lowport = args.lowport
	highport = args.highport
	scanner = Scanner(ip)
	scanner.scan(lowport, highport)
	for port in scanner.open_ports:
		try:
			grabber = Grabber(args.ipaddress, port)
			print(grabber.read())
			grabber.close
		except Exception as e:
			print("Port: " + str(port) + " Error: " + str(e))

if __name__ == '__main__':
	main()

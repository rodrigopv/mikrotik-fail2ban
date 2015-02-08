#!/usr/bin/env python

# This projected is licensed under the terms of the MIT license.
# See LICENSE for details.

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from netaddr import IPNetwork, IPAddress
import syslog
CIDR_WHITELIST = []

# -- START CONFIGURATION --

# Listen in the following IP Address
# Default: all interfaces (0.0.0.0)
LISTEN_IP = '0.0.0.0'

# Port to listen for UDP log packets. Note that you must configure your Mikrotik Router to send to the same address
LISTEN_PORT = 12346

# Uncomment by removing # symbol according to your needs and modify the IP or IP Ranges so it includes your router IP
# You can include multiple ranges or IPs by repeating the append line.
# Examples
# a /26 IP Range
#CIDR_WHITELIST.append("10.20.30.0/24") 
# a single IP
#CIDR_WHITELIST.append("192.168.1.1")


# -- END CONFIGURATION --


# Write to auth.log
syslog.openlog(ident="mikrotikd",logoption=syslog.LOG_PID, facility=syslog.LOG_AUTH)

class MikrotikLogger(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        ip, port = address
        for CIDR in CIDR_WHITELIST:
          if IPAddress(ip) in IPNetwork(CIDR):
            # Log only failed login attempts
            if "system,error,critical login failure for user" in datagram:
              syslog.syslog(syslog.LOG_INFO, datagram)
            break

def main():
    reactor.listenUDP(LISTEN_PORT, MikrotikLogger(), interface=LISTEN_IP)
    print "Mikrotik UDP Log Receiver running on %s:%s" % (LISTEN_IP, LISTEN_PORT)
    print "Make sure you have configured your Mikrotik Router to send critical topic log entries to that port."
    print "If everything is OK, now failed login attempts should appear at your system auth log at /var/log/auth.log (may vary depending on your distro)"
    reactor.run()

if __name__ == '__main__':
    main()

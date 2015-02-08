# mikrotik-fail2ban
Fail2Ban filter and Twisted-based (Python) UDP log receiver with CIDR whitelisting. Allows to stop bruteforce attempts against your Mikrotik hardware the same way you do it with your servers.


## How it works
The package consists in a fail2ban filter configuration that reads syslog auth.log and searches for login failures at mikrotik services. There's also a Twisted-based UDP Log receiver included that will receive UDP log packets from whitelisted Mikrotik router, and send only the login failures to auth.log.

You may want to use this along with Mikrotik ban action for fail2ban ( http://wiki.mikrotik.com/wiki/Use_Mikrotik_as_Fail2ban_firewall ) so it block the IPs at router.

### Requirements
- Mikrotik Routerboard
- Fail2ban
- Python 2.7
- Python Twisted (pip install twisted)
- Python netaddr (pip install netaddr)
- GNU Screen (apt-get install screen) (for running at a detached console)

## Setup
1. put filter.d/mikrotik.conf at /etc/fail2ban/filter.d/ (or at your fail2ban filters directory)
2. edit `log_server/mikrotik_logserver.py` and set the IP and Port where to listen for UDP log packets (it should be reachable from your router). You must also add the IP of your router, or the IP range that the program should trust to receive packets from.
3. Add the following entry to your jail.local file (as you shouldn't edit jail.conf as it can be overwritten at further updates).
```
[mikrotik]
# Default ports for mikrotik routerboard services: 8728,8729,21,22,23,8291,80,443
enabled = true
port   = 8728,8729,21,22,23,8291,80,443
filter = mikrotik
logpath = /var/log/auth.log
maxretry = 6
```
4. Configure your Mikrotik router to send `critical` topic log entries to the remote address and port you specified at mikrotik_logserver.py
5. Launch launch_logserver.sh to open the Log Receiver Server at a detached console (so it doesn't close when you close your ssh session).

** Please remember that if you want to make your IP blocks at router level you must configure Mikrotik ban action for fail2ban, as shown on [Mikrotik Wiki](http://wiki.mikrotik.com/wiki/Use_Mikrotik_as_Fail2ban_firewall). 


## Testing
Once you have complete the setup steps, you can test that everything is working by checking the following things
- Check that the router is sending logs to the IP and Port that you have set in the Log Server configuration
- Make sure that when you fail a login at your Mikrotik router, a log entry appears at /var/log/auth.log with the same text it would appear at your router's log.
- You can test fail2ban action by failing many times (If it doesn't ban you from keep trying, remember to set-up mikrotik ban action as shown in the note above).
- You should check fail2ban logs as well to check if it triggers the ban to your IP.

## License
mikrotik-fail2ban is licensed under the MIT license.

## Support this project
Feel free to fork and make pull requests to support Mikrotik user community and to secure out our networks from bruteforcing attempts. 

You can support me by [donating to me on Pledgie with Paypal](https://pledgie.com/campaigns/28306). If you buy me a coffee, I'm sure that I'll like it :P. 

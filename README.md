# PyScanner 🔍

```
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░  p y s c a n n e r          ░
░  network recon · python      ░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
```

A network scanner built in Python, inspired by nmap. PyScanner automatically detects your local network and scans all devices — open ports, services, OS fingerprinting, hostnames, MAC addresses, vendor info, and firewall detection.

Built by a cyber-anarchist who thinks security tools should be honest about what they do and who they serve.

---

## Features

- **Auto network detection** — no need to enter your IP range manually
- **Host discovery** — pings all 254 hosts on your subnet
- **Port scanning** — multi-threaded TCP scanning for speed
- **Service detection** — identifies services on open ports
- **Banner grabbing** — reads service banners where available
- **OS fingerprinting** — guesses OS via TTL analysis
- **Hostname resolution** — reverse DNS lookup
- **MAC address lookup** — reads from `/proc/net/arp`
- **Vendor lookup** — identifies manufacturers via MAC API
- **Firewall detection** — detects filtered ports and summarizes them
- **Progress bar** — real-time scan progress
- **Colored output** — green for open, red for filtered
- **Ctrl+C support** — graceful interrupt

---

## Requirements

- Python 3.x
- Linux (uses `/proc/net/arp` for MAC lookup)
- Internet connection (vendor lookup via `api.macvendors.com`)

---

## Usage

```bash
python3 PyScanner.py
```

No arguments needed. The scanner detects your network automatically and starts scanning.

---

## Example Output

```
___  _   _ ____ ____ ____ _  _ _  _ ____ ____
|__]  \_/  [__  |    |__| |\ | |\ | |___ |__/
|      |   ___] |___ |  | | \| | \| |___ |  \

Scan has begun...

192.168.1.1 - _gateway - Linux/Mac - aa:bb:cc:dd:ee:ff - XEROX CORPORATION
  53 - domain - no banner
  80 - http - no banner
  443 - https - no banner

192.168.1.105 - myphone - Linux/Mac - ff:ee:dd:cc:bb:aa - Apple, Inc.
  146 ports filtered

192.168.1.202 - unknown - Network Device - 18:69:d8:xx:xx:xx - Tuya Smart Inc.
  42 ports filtered

[██████████████████████████████████████████████████] 100%
Scan has ended...

6 hosts were down
The scan took 62 seconds
```

---

## How It Works

1. Detects your local IP automatically using `socket`
2. Pings each host in the `/24` subnet via `os.system`
3. Grabs TTL from ping output to fingerprint OS
4. Reads `/proc/net/arp` for MAC addresses
5. Looks up vendor from `api.macvendors.com`
6. Scans ports using threaded TCP sockets
7. Attempts banner grabbing on open ports
8. Detects filtered ports via `socket.timeout`
9. Prints grouped results per host with colors

---

## Limitations

- MAC vendor lookup may be rate-limited by the free API
- OS detection via TTL is approximate, not definitive
- Linux only
- Your own machine's MAC may show as `unknown`

---

## Legal Notice

Only use PyScanner on networks you own or have explicit permission to scan. Unauthorized network scanning may be illegal in your jurisdiction. Security without consent is surveillance.

---

## Author

Made by [SagiHacky](https://github.com/SagiHacky) · they/them · cyber-anarchist · `@legolymas:matrix.org`

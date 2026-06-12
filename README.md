# PyScanner 🔍

A powerful network scanner built in Python, inspired by nmap. PyScanner automatically detects your local network and scans all devices for open ports, services, OS, hostname, MAC address, and vendor information.

---

## Features

- **Auto network detection** — no need to enter your IP range manually
- **Host discovery** — pings all 254 hosts on your subnet
- **Port scanning** — scans ports with multi-threading for speed
- **Service detection** — identifies services running on open ports
- **Banner grabbing** — reads service banners where available
- **OS fingerprinting** — guesses the OS via TTL analysis
- **Hostname resolution** — resolves hostnames via reverse DNS
- **MAC address lookup** — reads MAC addresses from the ARP table
- **Vendor lookup** — identifies device manufacturers via MAC address API
- **Firewall detection** — detects filtered ports and summarizes them
- **Progress bar** — shows scan progress in real time
- **Colored output** — green for open ports, red for filtered
- **Ctrl+C support** — gracefully interrupts the scan

---

## Requirements

- Python 3.x
- Linux (uses `/proc/net/arp` for MAC lookup)
- Internet connection (for vendor lookup via `api.macvendors.com`)

---

## Usage

```bash
python3 PyScanner.py
```

The scanner will automatically detect your network and begin scanning. No arguments needed.

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

[██████████████████████████████████████████████████] 100%
Scan has ended...

6 hosts were down
The scan took 62 seconds
```

---

## How It Works

1. Detects your local IP automatically using `socket`
2. Pings each host in the `/24 subnet using `os.system`
3. For alive hosts, grabs TTL from ping output to guess OS
4. Reads `/proc/net/arp` for MAC addresses
5. Looks up vendor from `api.macvendors.com`
6. Scans ports 1-1000 using threaded TCP sockets
7. Attempts banner grabbing on open ports
8. Detects filtered ports via `socket.timeout`
9. Prints grouped results per host with colors

---

## Limitations

- MAC vendor lookup may be rate-limited by the free API
- OS detection via TTL is not 100% accurate
- Linux only (uses `/proc/net/arp`)
- Your own machine's MAC may show as `unknown`

---

## Legal Notice

Only use PyScanner on networks you own or have explicit permission to scan. Unauthorized network scanning may be illegal in your country.

---

## Author

Made by [SagiHacky](https://github.com/SagiHacky)

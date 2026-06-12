import socket
import os
import threading
import subprocess
import time
import urllib.request
import sys

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

scanned = 0
print_lock = threading.Lock()

def get_vendor(mac):
    try:
        url = "https://api.macvendors.com/" + mac
        response = urllib.request.urlopen(url)
        return response.read().decode()
    except:
        return "unknown"

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "unknown"

def get_mac(ip):
    with open("/proc/net/arp") as f:
        content = f.read()
        for line in content.split("\n"):
            if ip in line:
                return line.split()[3]
        return "unknown"

def scan_port(current_ip, i, open_ports):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((current_ip, i))
        try:
            banner = s.recv(1024).decode().strip()
        except:
            banner = "no banner"
        try:
            service = socket.getservbyport(i)
            open_ports.append(str(i) + " - " + service + " - " + banner.strip())
        except:
            service = "unknown"
    except ConnectionRefusedError:
        pass
    except socket.timeout:
        open_ports.append(str(i) + " - filtered")
    except OSError:
        pass
    finally:
        if s:
            s.close()

def scan_host(ip_range):
    semaphore.acquire()
    current_ip = ip_parts[0] + "." + ip_parts[1] + "." + ip_parts[2] + "." + str(ip_range)
    response = os.system("ping -c 1 " + current_ip + " > /dev/null 2>&1")
    hostname = get_hostname(current_ip)
    if response == 0:
        global alive_hosts
        alive_hosts += 1
        try:
            ping_output = subprocess.check_output("ping -c 1 " + current_ip, shell=True).decode()
            ttl = int(ping_output.split("ttl=")[1].split()[0])
            mac = get_mac(current_ip)
            vendor = get_vendor(mac)
            if ttl <= 64:
                os_guess = f"{CYAN}Linux/Mac{RESET}"
            elif ttl <= 128:
                os_guess = f"{YELLOW}Windows{RESET}"
            else:
                os_guess = f"{MAGENTA}Network Device{RESET}"
            open_ports = []
            port_threads = []
            for i in range(Port1, Port2):
                t = threading.Thread(target=scan_port, args=(current_ip, i, open_ports), daemon=True)
                t.start()
                port_threads.append(t)
            for t in port_threads:
                t.join()
            filtered_count = len([p for p in open_ports if "filtered" in p])
            with print_lock:
                sys.stdout.write("\n")
                print(f"{BOLD}{GREEN}[+] {current_ip}{RESET} {BLUE}-{RESET} {WHITE}{hostname}{RESET} {BLUE}-{RESET} {os_guess} {BLUE}-{RESET} {MAGENTA}{mac}{RESET} {BLUE}-{RESET} {YELLOW}{vendor}{RESET}")
                if filtered_count > 10:
                    for port in open_ports:
                        if "filtered" not in port:
                            print(f"{GREEN}    {port}{RESET}")
                    print(f"{RED} {filtered_count} ports filtered{RESET}")
                else:
                    for port in open_ports:
                        print(f"{GREEN}    {port}{RESET}")

        except:
            pass
    else:
        down_hosts.append(current_ip)
    global scanned
    scanned += 1
    percent = int(scanned / 254 * 100)
    bar = f"{CYAN}█{RESET}" * (percent // 2) + f"{BLUE}-{RESET}" * (50 - percent // 2)
    sys.stdout.write(f"\r[{bar}] {BOLD}{WHITE}{percent}%{RESET} | {GREEN}Alive: {alive_hosts}{RESET} | {RED}Down: {len(down_hosts)}{RESET} | {YELLOW}Scanned: {scanned}/254{RESET}")
    sys.stdout.flush()
    semaphore.release()

local_ip = socket.gethostbyname(socket.gethostname())
ip_parts = local_ip.split(".")
Port1 = 1
Port2 = 1000
down_hosts = []
alive_hosts = 0
threads = []
semaphore = threading.Semaphore(50)

print(f"{BOLD}{CYAN}")
print(r"___  _   _ ____ ____ ____ _  _ _  _ ____ ____")
print(r"|__]  \_/  [__  |    |__| |\ | |\ | |___ |__/")
print(r"|      |   ___] |___ |  | | \| | \| |___ |  \ ")
print(f"{RESET}")

start_time = time.time()

print(f"{BOLD}{GREEN}Scan has begun...{RESET}")

try:
    for ip_range in range(1,255):
        t = threading.Thread(target=scan_host, args=(ip_range,), daemon=True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    sys.stdout.write("\n\n")
    print(f"{BOLD}{GREEN}Scan has ended...{RESET}")
    print()
    final = round((int(time.time() - start_time)), 2)
    print(f"{CYAN}Hosts down:{RESET} {RED}{len(down_hosts)}{RESET}")
    print(f"{CYAN}Hosts alive:{RESET} {GREEN}{alive_hosts}{RESET}")
    print(f"{CYAN}Scan duration:{RESET} {YELLOW}{final} seconds{RESET}")
except KeyboardInterrupt:
    print(f"\n{RED}{BOLD}Scan interrupted by user!{RESET}")

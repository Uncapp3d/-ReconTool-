import socket
import dns.resolver
import requests
import ipwhois
import threading
import time


TARGET = input("Enter the target IP or domain: ")
LOG_FILE = 'recon_log.txt'


def dns_query(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        print(f"DNS records for {domain}:")
        for ipval in result:
            print(f"  - {ipval.to_text()}")
    except Exception as e:
        print(f"DNS Query failed: {e}")


def port_scan(ip):
    print(f"Scanning ports on {ip}...")
    open_ports = []
    for port in range(20, 1025):  
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()

    if open_ports:
        print(f"Open ports on {ip}: {open_ports}")
    else:
        print(f"No open ports found on {ip}")


def ip_info(ip):
    try:
        ip_info = ipwhois.IPWhois(ip)
        result = ip_info.lookup_rdap()
        print(f"IP information for {ip}:")
        print(f"  - Country: {result.get('country', 'N/A')}")
        print(f"  - ASN: {result.get('asn', 'N/A')}")
        print(f"  - Organization: {result.get('network', {}).get('name', 'N/A')}")
    except Exception as e:
        print(f"Failed to retrieve IP information: {e}")


def start_recon(target):
    if target.count('.') == 3:
        ip = target
    else:  
        dns_query(target)
        ip = socket.gethostbyname(target)

    print(f"Starting recon on {ip}...")
    
  
    threads = []


    port_thread = threading.Thread(target=port_scan, args=(ip,))
    threads.append(port_thread)


    ip_thread = threading.Thread(target=ip_info, args=(ip,))
    threads.append(ip_thread)


    for thread in threads:
        thread.start()

  
    for thread in threads:
        thread.join()

    print("Recon completed!")


def log_results(data):
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {data}\n")

if __name__ == '__main__':
    start_recon(TARGET)

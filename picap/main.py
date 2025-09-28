#!/usr/bin/env python3
import argparse
import subprocess
import sys
import socket
from datetime import datetime
import requests


def resolve_domain_to_ip(domain: str) -> str:
    """Resolve a domain name to an IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror as e:
        print(f"[!] Could not resolve domain {domain}: {e}")
        sys.exit(1)


def start_capture(ip: str, output_file: str, duration: int | None):
    """Start a tshark capture filtered for the given IP."""
    print(f"[*] Starting capture for IP: {ip}")
    print(f"[*] Saving capture to {output_file}")

    cmd = [
        "tshark",
        "-f", f"host {ip}",
        "-w", output_file
    ]

    if duration:
        cmd.extend(["-a", f"duration:{duration}"])

    try:
        # Start tshark as a background process
        proc = subprocess.Popen(cmd)
    except FileNotFoundError:
        print("[!] tshark not found. Please install Wireshark/tshark.")
        sys.exit(1)
    except Exception as e:
        print(f"[!] Error running tshark: {e}")
        sys.exit(1)

    return proc

def emulate_browser_connection(domain: str, ip: str, scheme: str):
    """Emulate a browser connection to the domain or IP using requests."""
    url = f"{scheme}://{domain}" if domain else f"{scheme}://{ip}"
    print(f"[*] Emulating browser connection to {url}")
    try:
        response = requests.get(url, timeout=5)
        print(f"[*] Request sent, status code: {response.status_code}")
    except Exception as e:
        print(f"[!] Error emulating browser connection: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Simple PCAP capture tool using tshark"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--domain", help="Domain name to capture traffic for")
    group.add_argument("-i", "--ip", help="IP address to capture traffic for")
    parser.add_argument("-t", "--duration", type=int, default=None, help="Capture duration in seconds (default: run until stopped with Ctrl+C)")
    parser.add_argument("-s","--scheme", choices=["http", "https"], default="https", help="Choose http or https for emulated browser connection (default: https)")

    args = parser.parse_args()

    if args.domain:
        ip = resolve_domain_to_ip(args.domain)
    else:
        ip = args.ip

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"capture_{ip}_{timestamp}.pcap"

    proc = start_capture(ip, output_file, args.duration)

    # Wait a moment for tshark to start
    import time
    time.sleep(2)

    emulate_browser_connection(args.domain, ip, args.scheme)

    # Wait for tshark to finish if duration is set, else instruct user to stop manually
    if args.duration:
        proc.wait()
    else:
        print("[*] Press Ctrl+C to stop capture.")
        try:
            proc.wait()
        except KeyboardInterrupt:
            print("[*] Capture stopped.")


if __name__ == "__main__":
    main()

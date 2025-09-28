# picap

A simple command-line tool to capture network packets for a specific domain or IP using `tshark`, and emulate browser traffic to help generate packets for analysis.

## Features
- Captures packets filtered by domain or IP address
- Emulates a browser HTTP/HTTPS request to the target
- Supports capture duration or manual stop
- Output saved as a `.pcap` file for analysis

## Requirements
- Python 3.8+
- `tshark` (part of Wireshark)
- Python package: `requests`

## Installation
1. Install Wireshark/tshark:
   ```sh
   sudo apt install wireshark tshark
   ```
2. Install the tool in Production mode:
   - Using pip:
     ```sh
     pip install .
     ```
   - Using uv:
     ```sh
     uv tool install .
     ```
3. Install the tool in editable / development mode:
   - Using pip:
     ```sh
     pip install -e .
     ```
   - Using uv:
     ```sh
     uv tool install --editable .
     ```

## Usage
```sh
python3 main.py -d example.com -t 10 --scheme https
```
- `-d`, `--domain`: Domain name to capture traffic for
- `-i`, `--ip`: IP address to capture traffic for
- `-t`, `--duration`: Capture duration in seconds (optional)
- `-s`, `--scheme`: Choose `http` or `https` for the emulated browser connection (default: https)

If no duration is specified, capture runs until you press Ctrl+C.

Example:
```sh
python3 main.py -d example.com --scheme http
```

## How it works
1. Resolves the domain to an IP (if needed)
2. Starts `tshark` to capture packets for the IP
3. Emulates a browser HTTP or HTTPS request to the domain/IP
4. Saves the capture to a timestamped `.pcap` file

## Notes
- You may need root privileges to run `tshark`.
- The emulated browser request uses the scheme you choose (`http` or `https`).

## License
MIT

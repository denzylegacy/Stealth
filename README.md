<div align="center">

  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://playwright.dev/python/">
    <img src="https://img.shields.io/badge/Playwright-2EAD33?style=for-the-badge&logo=playwright&logoColor=white" alt="Playwright">
  </a>
  <a href="https://www.torproject.org/">
    <img src="https://img.shields.io/badge/Tor-7D4698?style=for-the-badge&logo=tor-project&logoColor=white" alt="Tor">
  </a>

  <h3>Stealth</h3>

  A project for stress-testing web applications with multiple, concurrent browser instances, each with a unique IP address using Tor or Mullvad VPN.
  <br>
</div>

## Overview

This project provides a set of Python scripts to launch multiple instances of a web browser, each routed through a different proxy (Tor or Mullvad). This allows for simulating traffic from various locations and IPs, which is useful for stress-testing, web scraping, and other tasks requiring anonymity and IP rotation.

## Features

- **Multiple Browser Instances:** Run many browser instances in parallel.
- **IP Rotation:** Each instance can have a unique IP address.
- **Proxy Support:**
  - **Tor:** Integrates with the Tor network, including support for bridges to bypass censorship.
  - **Mullvad:** Uses Mullvad VPN's SOCKS5 proxies for a wide range of IP addresses.
- **Automation:** Powered by Playwright for reliable browser automation.

## Installation

### 1. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage the project's dependencies.

```bash
python3 -m venv myenv
source myenv/bin/activate
```

### 2. Install Dependencies

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

Install the necessary browser binaries for Playwright:

```bash
playwright install
```

## Setup and Usage

### Tor

#### 1. Install Tor

On Debian-based systems (like Ubuntu), you can install Tor with:

```bash
sudo apt update
sudo apt install tor
```

#### 2. Configure Tor (Optional: Using Bridges)

To avoid having your Tor traffic blocked, you can use bridges.

1.  **Get Bridges:**
    *   Visit [https://bridges.torproject.org/](https://bridges.torproject.org/) and request `obfs4` bridges.
    *   Or, send an email to `bridges@torproject.org` from a Gmail or Riseup email address.

2.  **Edit `torrc`:**
    Open your Tor configuration file:
    ```bash
    sudo nano /etc/tor/torrc
    ```

3.  **Add Bridges:**
    Add the following lines to the end of the file, replacing the example bridges with the ones you obtained:

    ```
    UseBridges 1
    ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
    Bridge obfs4 <IP>:<PORT> <FINGERPRINT> cert=<CERT> iat-mode=<MODE>
    Bridge obfs4 <IP>:<PORT> <FINGERPRINT> cert=<CERT> iat-mode=<MODE>
    ```

4.  **Restart Tor:**
    ```bash
    sudo systemctl restart tor
    ```

#### 3. Run the Tor Script

To run the stress test using Tor, execute:

```bash
python src/stress_test_crisp_tor.py
```

### Mullvad VPN

#### 1. Set up Mullvad VPN

Ensure you have the Mullvad VPN client installed and connected.

#### 2. Run the Mullvad Script

To run the stress test using Mullvad's SOCKS5 proxies, execute:

```bash
python src/stress_test_crisp_mullvad.py
```

This script will automatically fetch a list of available Mullvad servers and select one at random for each browser instance.

### Basic Usage (Without Proxy)

To run a simple stress test without any proxies, you can use the base script:

```bash
python src/stress_test_crisp.py
```

## Disclaimer

This project is intended for educational and testing purposes only. The user is responsible for any and all use of this software. Please use it responsibly and in compliance with the terms of service of any website you interact with.
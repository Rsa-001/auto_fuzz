#!/usr/bin/env bash
set -e

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run with sudo or as root"
  exit 1
fi

echo "Updating package lists…"
apt-get update -y

echo "Installing Python3 and tools…"
apt-get install -y python3 python3-venv ffuf gobuster seclists

echo -e "\n\nSetup complete. You can now run:"
echo " python3 auto_fuzz.py <TARGET_IP> <HOSTNAME>"

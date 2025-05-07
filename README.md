# Auto Fuzz + VHost Enumeration (auto_fuzz.py)

`auto_fuzz.py` is a simple Python3 wrapper that runs [ffuf](https://github.com/ffuf/ffuf) and [gobuster](https://github.com/OJ/gobuster). It discovers:

1. Directories and files on a target IP/hostname  
2. Virtual host (vhost) subdomains  
3. Directories and files on each discovered subdomain  

All findings are printed live and saved to text files for later review.

## Features

- **Live output** – prints each path or subdomain as soon as it's found    
- **Simple results storage** – saves `IP_paths.txt` and one `paths.txt` per subdomain under `fuzz_results/<timestamp>/`  
- **Configurable** – edit wordlist paths, extensions, and thread counts at the top of the script  
- **Ideal for CTF-style machines** (e.g. HackTheBox labs)  

## Prerequisites

- Python 3  
- [ffuf](https://github.com/ffuf/ffuf)  
- [gobuster](https://github.com/OJ/gobuster)
- Seclists
- A line in your `/etc/hosts` mapping the target IP to the hostname

## Installation

After cloning the repo, run the included `setup.sh` (requires root) to install all system dependencies


If you have any suggestions, please let me know, knowledge is always welcome.

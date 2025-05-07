#!/usr/bin/env python3
import argparse
import subprocess
import sys
import os
import datetime
import re

DIR_WORDLIST   = "/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt"
SUB_WORDLIST   = "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
FFUF_THREADS   = "350"
GOB_THREADS    = "200"
EXTENSIONS     = ".php,.html,.js,.css,.txt,.config"

FFUF_PATH_RE    = re.compile(r"^(\S+)\s+\[Status:")
GOBUSTER_SUB_RE = re.compile(r"Found:\s*([^\s]+?)\s+Status:")

def banner(msg):
    print(f"\n=== {msg} ===\n")

def run_stream(cmd, regex, prefix, save_list):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for raw in proc.stdout:
        line = raw.rstrip()
        m = regex.search(line)
        if m:
            val = m.group(1)
            if val not in save_list:
                save_list.append(val)
                if prefix:
                    print(f"    {prefix}  {val}")
                else:
                    print(f"    {val}")
    proc.wait()
    if proc.returncode != 0:
        print(f"Error running: {' '.join(cmd)}")
        sys.exit(1)

def initial_ffuf(base_url, out_dir):
    banner(f"Initial ffuf on {base_url}")
    cmd = [
        "ffuf", "-u", f"{base_url}/FUZZ",
        "-w", DIR_WORDLIST,
        "-mc", "200-299,301",
        "-fc", "403,404,405,500",
        "-r", "-ic",
        "-e", EXTENSIONS,
        "-t", FFUF_THREADS
    ]
    print("Directories/files found on IP:")
    paths = []
    run_stream(cmd, FFUF_PATH_RE, "", paths)
    with open(os.path.join(out_dir, "IP_paths.txt"), "w") as f:
        f.write("\n".join(paths) + "\n")
    return paths

def discover_subdomains(hostname):
    banner(f"Discovering subdomains for {hostname}")
    cmd = [
        "gobuster", "vhost",
        "-u", f"http://{hostname}",
        "-w", SUB_WORDLIST,
        "-t", GOB_THREADS,
        "--append-domain"
    ]
    print("Subdomains found:")
    subs = []
    run_stream(cmd, GOBUSTER_SUB_RE, "", subs)
    return subs

def ffuf_subdomain(ip, sub, out_dir):
    banner(f"ffuf on subdomain {sub}")
    subdir = os.path.join(out_dir, sub.replace(".", "_"))
    os.makedirs(subdir, exist_ok=True)
    cmd = [
        "ffuf", "-u", f"http://{ip}/FUZZ",
        "-H", f"Host: {sub}",
        "-w", DIR_WORDLIST,
        "-ic", "-fc", "403,404",
        "-e", EXTENSIONS,
        "-t", FFUF_THREADS
    ]
    print(f"Directories/files found on {sub}:")
    paths = []
    run_stream(cmd, FFUF_PATH_RE, "", paths)
    with open(os.path.join(subdir, "paths.txt"), "w") as f:
        f.write("\n".join(paths) + "\n")
    return paths

def main():
    parser = argparse.ArgumentParser(description="Auto fuzz + vhost enumeration")
    parser.add_argument("target_ip", help="IP or hostname to fuzz")
    parser.add_argument("hostname", help="Real hostname for vhost discovery")
    parser.add_argument("--output-dir", default="fuzz_results", help="Directory to store results")
    args = parser.parse_args()

    base_dir = os.path.join(args.output_dir, datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    os.makedirs(base_dir, exist_ok=True)

    initial_ffuf(f"http://{args.target_ip}", base_dir)

    subs = discover_subdomains(args.hostname)
    if not subs:
        print("No subdomains found, exiting.")
        sys.exit(0)

    for s in subs:
        ffuf_subdomain(args.target_ip, s, base_dir)

    banner("All tasks complete")
    print(f"Results saved in {base_dir}")

if __name__ == "__main__":
    main()

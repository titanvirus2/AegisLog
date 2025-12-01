import argparse
import requests
import json
from tabulate import tabulate

API = "http://127.0.0.1:8080"

def cmd_add():
    print ("Enter Vulnerability Details. Leave blank to use default/empty.")
    title = input("Title: ").strip()
    severity = input("Severity [Low/Medium/High/Critical]: ").strip().title() or "Low"
    asset = input("Asset (IP/Hostname): ").strip()
    description = input("Description: ").strip()
    steps = input("Steps to Reproduce: ").strip()
    mitigation = input("Mitigation: ").strip()
    status = input("Status [Open/Fixed/Accepted/False Positive]: ").strip().title() or "Open"

    payload = {
        "title": title,
        "severity": severity,
        "asset": asset,
        "description": description,
        "steps": steps,
        "mitigation": mitigation,
        "status": status
    }
    r = requests.post(f"{API}/vulnerabilities", json=payload)
    if r.status_code in (200,201):
        print("Created:")
        r.json()
    else:
        print("Error:", r.status_code, r.text)

def cmd_list():
    r = requests.get(f"{API}/vulnerabilities")
    if r.status_code != 200:
        print("Error:", r.status_code)
        return
    data = r.json()
    if not data:
        print("No vulnerabilities found.")
        return
    table = []
    for v in data:
        table.append([v.get("id"), v.get("title"), v.get("severity"), v.get("status"), v.get("asset")])
    print(tabulate(table, headers=["ID", "Title", "Severity", "Status", "Asset"]))

def cmd_get(vuln_id):
    r = requests.get(f"{API}/vulnerabilities/{vuln_id}")
    if r.status_code == 200:
        r.json()
    else:
        print("Error:", r.status_code, r.text)

def cmd_update(vuln_id):
    # fetch existing
    r = requests.get(f"{API}/vulnerabilities/{vuln_id}")
    if r.status_code != 200:
        print("Error fetching vulnerability:", r.status_code, r.text)
        return
    current = r.json()
    print("Leave blank to keep current value.")
    def i(prompt, current_value):
        val = input(f"{prompt} [{current_value}]: ").strip()
        return val if val else current_value
    payload = {
        "title": i("Title", current.get("title")),
        "severity": i("Severity", current.get("severity")),
        "asset": i("Asset", current.get("asset")),
        "description": i("Description", current.get("description")),
        "steps": i("Steps to Reproduce", current.get("steps")),
        "mitigation": i("Mitigation", current.get("mitigation")),
        "status": i("Status", current.get("status")),
    }
    r2 = requests.put(f"{API}/vulnerabilities/{vuln_id}", json=payload)
    if r2.status_code == 200:
        print("Updated:")
        r2.json()
    else:
        print("Error:", r2.status_code, r2.text)

def cmd_delete(vuln_id):
    r = requests.delete(f"{API}/vulnerabilities/{vuln_id}")
    if r.status_code == 200:
        print("Deleted:", r.json())
    else:
        print("Error:", r.status_code, r.text)

def cmd_export():
    r = requests.post(f"{API}/export")
    if r.status_code == 200:
        pretty_print_json(r.json())
    else:
        print("Error:", r.status_code, r.text)

def main():
    parser = argparse.ArgumentParser(prog="vulncli", description="LV-MTS CLI client")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("add")
    sub.add_parser("list")
    getp = sub.add_parser("get")
    getp.add_argument("id", type=int)
    upd = sub.add_parser("update")
    upd.add_argument("id", type=int)
    dlt = sub.add_parser("delete")
    dlt.add_argument("id", type=int)
    sub.add_parser("export")

    args = parser.parse_args()
    if args.cmd == "add":
        cmd_add()
    elif args.cmd == "list":
        cmd_list()
    elif args.cmd == "get":
        cmd_get(args.id)
    elif args.cmd == "update":
        cmd_update(args.id)
    elif args.cmd == "delete":
        cmd_delete(args.id)
    elif args.cmd == "export":
        cmd_export()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()



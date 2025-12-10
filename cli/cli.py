import requests
import json
from tabulate import tabulate
import sys

# --- API Configuration ---
API_BASE = "http://127.0.0.1:8080"
API_VULN_BASE = f"{API_BASE}/vulnerabilities"
API_ASSET_BASE = f"{API_BASE}/assets"

def get_input_with_default(prompt, default_value=""):
    display_prompt = f"{prompt} [{default_value}]: " if default_value else f"{prompt}: "
    user_input = input(display_prompt).strip()
    return user_input if user_input else default_value

def display_api_error(response, action="Request"):
    try:
        error_details = response.json()
    except requests.exceptions.JSONDecodeError:
        error_details = response.text
    print(f" {action} Error: Status Code {response.status_code}")
    print(f"Details: {error_details}")

def get_id_input(prompt_name):
    while True:
        try:
            record_id = input(f"Enter ID of {prompt_name}: ").strip()
            if not record_id:
                return None
            return int(record_id)
        except ValueError:
            print(" Invalid input. Please enter a valid integer ID.")


# --- Vulnerability CRUD Commands ---

def add_vulnerability():
    print("\n--- Add New Vulnerability ---")

    payload = {
        "title": get_input_with_default("Title"),
        "severity": get_input_with_default("Severity [Low/Medium/High/Critical]", "Low").title(),
        "asset": get_input_with_default("Asset (IP/Hostname)"),
        "description": get_input_with_default("Description"),
        "status": get_input_with_default("Status [Open/Fixed/Accepted/False Positive]", "Open").title()
    }

    try:
        response = requests.post(API_VULN_BASE, json=payload)

        if response.status_code in (200, 201):
            print(" Successfully Created New Vulnerability Record.")
            print("Response:", response.json())
        else:
            display_api_error(response, "Create Vulnerability Record")
    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def list_vulnerabilities():
    print("\n--- List All Vulnerabilities ---")

    try:
        response = requests.get(API_VULN_BASE)

        if response.status_code != 200:
            display_api_error(response, "List Vulnerability Records")
            return

        data = response.json()

        if not data:
            print(" No vulnerabilities found in the system.")
            return

        table = []
        for v in data:
            title = v.get("title", "")
            display_title = title[:30] + "..." if len(title) > 30 else title
            table.append([
                v.get("id"),
                display_title,
                v.get("severity", ""),
                v.get("status", ""),
                v.get("asset", "")
            ])

        headers = ["ID", "Title", "Severity", "Status", "Asset"]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def get_vulnerability():
    print("\n--- Get Vulnerability Details ---")
    vuln_id = get_id_input("vulnerability to retrieve")
    if vuln_id is None: return

    try:
        response = requests.get(f"{API_VULN_BASE}/{vuln_id}")

        if response.status_code == 200:
            print(" Record Details:")
            print(json.dumps(response.json(), indent=4))
        else:
            display_api_error(response, f"Get Vulnerability Record ID {vuln_id}")

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def update_vulnerability():
    print("\n--- Update Vulnerability Record ---")
    vuln_id = get_id_input("vulnerability to update")
    if vuln_id is None: return

    try:
        print(f"Fetching current data for ID {vuln_id}...")
        r_get = requests.get(f"{API_VULN_BASE}/{vuln_id}")
        if r_get.status_code != 200:
            display_api_error(r_get, f"Fetch Vulnerability Record ID {vuln_id} for Update")
            return
        current_data = r_get.json()

        print("\n Current values displayed in brackets []. Leave blank to keep current value.")

        new_payload = {
            "title": get_input_with_default("Title", current_data.get("title", "")),
            "severity": get_input_with_default("Severity [Low/Medium/High/Critical]", current_data.get("severity", "")).title(),
            "asset": get_input_with_default("Asset", current_data.get("asset", "")),
            "description": get_input_with_default("Description", current_data.get("description", "")),
            "status": get_input_with_default("Status [Open/Fixed/Accepted/False Positive]", current_data.get("status", "")).title(),
        }

        r_put = requests.put(f"{API_VULN_BASE}/{vuln_id}", json=new_payload)

        if r_put.status_code == 200:
            print(f"\n Successfully Updated Vulnerability Record ID {vuln_id}.")
            print("Response:", r_put.json())
        else:
            display_api_error(r_put, f"Update Vulnerability Record ID {vuln_id}")

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def delete_vulnerability():
    print("\n--- Delete Vulnerability Record ---")
    vuln_id = get_id_input("vulnerability to delete")
    if vuln_id is None: return

    confirm = input(f" Are you sure you want to DELETE vulnerability record ID {vuln_id}? (type 'YES' to confirm): ").strip()
    if confirm != "YES":
        print("Action cancelled.")
        return

    try:
        response = requests.delete(f"{API_VULN_BASE}/{vuln_id}")

        if response.status_code == 200:
            print(f" Successfully Deleted Vulnerability Record ID {vuln_id}.")
            print("Response:", response.json())
        else:
            display_api_error(response, f"Delete Vulnerability Record ID {vuln_id}")

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")


# --- Asset CRUD Commands ---

def add_asset():
    print("\n--- Add New Asset ---")

    payload = {
        "operating_system": get_input_with_default("Operating System"),
        "ip_address": get_input_with_default("IP Address", "")
    }

    try:
        response = requests.post(API_ASSET_BASE, json=payload)

        if response.status_code in (200, 201):
            print(" Successfully Created New Asset Record.")
            print("Response:", response.json())
        else:
            display_api_error(response, "Create Asset Record")
    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def list_assets():
    print("\n--- List All Assets ---")

    try:
        response = requests.get(API_ASSET_BASE)

        if response.status_code != 200:
            display_api_error(response, "List Asset Records")
            return

        data = response.json()

        if not data:
            print(" No assets found in the system.")
            return

        table = []
        for a in data:
            table.append([
                a.get("id"),
                a.get("operating_system", ""),
                a.get("ip_address", "")
            ])

        headers = ["ID", "Operating System", "IP Address"]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def get_asset():
    print("\n--- Get Asset Details ---")
    asset_id = get_id_input("asset to retrieve")
    if asset_id is None: return

    try:
        response = requests.get(f"{API_ASSET_BASE}/{asset_id}")

        if response.status_code == 200:
            print(" Asset Details:")
            print(json.dumps(response.json(), indent=4))
        else:
            display_api_error(response, f"Get Asset Record ID {asset_id}")

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def update_asset():
    print("\n--- Update Asset Record ---")
    asset_id = get_id_input("asset to update")
    if asset_id is None: return

    try:
        print(f"Fetching current data for ID {asset_id}...")
        r_get = requests.get(f"{API_ASSET_BASE}/{asset_id}")
        if r_get.status_code != 200:
            display_api_error(r_get, f"Fetch Asset Record ID {asset_id} for Update")
            return
        current_data = r_get.json()

        print("\n Current values displayed in brackets []. Leave blank to keep current value.")

        new_payload = {
            "operating_system": get_input_with_default("Operating System", current_data.get("operating_system", "")),
            "ip_address": get_input_with_default("IP Address", current_data.get("ip_address", ""))
        }
        
        # Filter out fields that were not changed (empty input)
        new_payload = {k: v for k, v in new_payload.items() if v} 

        r_put = requests.put(f"{API_ASSET_BASE}/{asset_id}", json=new_payload)

        if r_put.status_code == 200:
            print(f"\n Successfully Updated Asset Record ID {asset_id}.")
            print("Response:", r_put.json())
        else:
            display_api_error(r_put, f"Update Asset Record ID {asset_id}")

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

def delete_asset():
    print("\n--- Delete Asset Record ---")
    asset_id = get_id_input("asset to delete")
    if asset_id is None: return

    confirm = input(f" Are you sure you want to DELETE asset record ID {asset_id}? (type 'YES' to confirm): ").strip()
    if confirm != "YES":
        print("Action cancelled.")
        return

    try:
        response = requests.delete(f"{API_ASSET_BASE}/{asset_id}")

        if response.status_code == 200:
            print(f" Successfully Deleted Asset Record ID {asset_id}.")
            print("Response:", response.json())
        else:
            display_api_error(response, f"Delete Asset Record ID {asset_id}")

    except requests.exceptions.RequestException as e:
        print(f" Connection Error: {e}")

# --- Main Functions ---

def display_menu():
    print("\n=============================================")
    print("         AegisLog Vulnerability Tracker      ")
    print("=============================================")
    print("--- VULNERABILITY OPERATIONS ---")
    print("1. Add New Vulnerability Record")
    print("2. List All Vulnerabilities")
    print("3. Get Details of a Vuln. Record (by ID)")
    print("4. Update a Vuln. Record (by ID)")
    print("5. Delete a Vuln. Record (by ID)")
    print("--- ASSET OPERATIONS ---")
    print("6. Add New Asset Record")
    print("7. List All Assets")
    print("8. Get Details of an Asset (by ID)")
    print("9. Update an Asset (by ID)")
    print("10. Delete an Asset (by ID)")
    print("--- SYSTEM ---")
    print("11. Exit Program")
    print("=============================================")

def main():
    print("--- Welcome to AegisLog Console ---")
    print(f"Connecting to API at: {API_BASE}")

    commands = {
        # Vulnerability Commands
        "1": add_vulnerability,
        "2": list_vulnerabilities,
        "3": get_vulnerability,
        "4": update_vulnerability,
        "5": delete_vulnerability,
        # Asset Commands
        "6": add_asset,
        "7": list_assets,
        "8": get_asset,
        "9": update_asset,
        "10": delete_asset,
    }

    while True:
        display_menu()
        choice = input(" Enter your choice (1-11): ").strip()

        if choice in commands:
            commands[choice]()
        elif choice == "11":
            print(" Exiting AegisLog Console. Goodbye!")
            sys.exit(0)
        else:
            print(" Invalid option. Please choose a number between 1 and 11.")

if __name__ == "__main__":
  main()

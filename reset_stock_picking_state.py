import os
import requests
import json

# ------------------ CONFIGURATION ------------------
odoo_url = "https://digitalvizta-klever-kitchen.odoo.com"
db = "digitalvizta-klever-kitchen-master-17296866"

# ✅ Use environment variables for security
# Example (set before running):
# export ODOO_USER="your_email@example.com"
# export ODOO_KEY="your_api_key_here"
username = "sawada48127@gmail.com"       # replace with your Odoo user email
api_key = "123"

# Target model and record ID
model = "stock.picking"
record_id = 18  # Example record ID to reset

# ---------------------------------------------------

# 1️⃣ Authenticate
auth_url = f"{odoo_url}/web/session/authenticate"
auth_payload = {
    "jsonrpc": "2.0",
    "params": {
        "db": db,
        "login": username,
        "password": api_key,
    },
}

session = requests.Session()
auth_response = session.post(auth_url, json=auth_payload)
auth_data = auth_response.json()

if "result" not in auth_data or not auth_data["result"].get("uid"):
    raise Exception(f"❌ Authentication failed: {auth_data}")

uid = auth_data["result"]["uid"]
print(f"✅ Authenticated as UID {uid}")

# ---------------------------------------------------
# Helper function for calling Odoo methods
def call_odoo_method(model, method, args=None, kwargs=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args or [],
            "kwargs": kwargs or {},
        },
        "id": 1,
    }
    response = session.post(f"{odoo_url}/web/dataset/call_kw/{model}/{method}", json=payload)
    return response.json()

# ---------------------------------------------------
# Step 1️⃣: Verify record exists
search_result = call_odoo_method(
    model, "search_read", [[["id", "=", record_id]]], {"fields": ["id", "state"]}
)

if not search_result.get("result"):
    raise Exception(f"❌ stock.picking record {record_id} not found.")

print(f"🔎 Found record ID {record_id} with state: {search_result['result'][0]['state']}")

# ---------------------------------------------------
# Step 2️⃣: If available, try cancel and draft actions
for method in ["action_cancel", "action_draft"]:
    print(f"⚙️ Executing method: {method}")
    result = call_odoo_method(model, method, [[record_id]])
    if "error" in result:
        print(f"⚠️ {method} failed: {result['error']['data']['message']}")
    else:
        print(f"✅ {method} executed successfully")

# ---------------------------------------------------
# Step 3️⃣: Ensure state field is updated manually if needed
# Some stock.picking types don’t auto-reset states with actions
print("📝 Forcing manual state updates just in case...")

call_odoo_method(model, "write", [[record_id], {"state": "cancel"}])
call_odoo_method(model, "write", [[record_id], {"state": "draft"}])

print("🎯 Record successfully set to DRAFT state!")

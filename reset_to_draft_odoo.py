import requests
import json

# ------------------ CONFIGURATION ------------------
odoo_url = "https://digitalvizta-klever-kitchen.odoo.com"
db = "digitalvizta-klever-kitchen-master-17296866"
username = "sawada48127@gmail.com"       # replace with your Odoo user email
api_key = "123"

model = "stock.move.line"
record_id = 1  # Example record ID

# ---------------------------------------------------

# Authenticate to Odoo
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
# Function to call Odoo model methods
def call_odoo_method(model, method, args, kwargs=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "model": model,
            "method": method,
            "args": args,
            "kwargs": kwargs or {},
        },
        "id": 1,
    }
    url = f"{odoo_url}/web/dataset/call_kw/{model}/{method}"
    response = session.post(url, json=payload)
    return response.json()


# ---------------------------------------------------
# Step 1️⃣: Verify record exists
search_result = call_odoo_method(
    model, "search_read", [[["id", "=", record_id]]], {"fields": ["id", "state"]}
)

if not search_result.get("result"):
    raise Exception(f"❌ Record with ID {record_id} not found.")

print(f"🔎 Found record ID {record_id} with state: {search_result['result'][0]['state']}")

# ---------------------------------------------------
# Step 2️⃣: Update state to 'cancel'
print("🛑 Setting record to 'cancel' state...")
cancel_result = call_odoo_method(model, "write", [[record_id], {"state": "cancel"}])
print(f"✅ Cancel update result: {cancel_result}")

# Step 3️⃣: Update state to 'draft'
print("📝 Setting record to 'draft' state...")
draft_result = call_odoo_method(model, "write", [[record_id], {"state": "draft"}])
print(f"✅ Draft update result: {draft_result}")

print("🎯 Process completed successfully!")

import os
import requests
import json

odoo_url = "https://digitalvizta-klever-kitchen.odoo.com"
db = "digitalvizta-klever-kitchen-master-17296866"

username = "sawada48127@gmail.com"       # replace with your Odoo user email
api_key = "123"

picking_model = "stock.picking"
move_model = "stock.move"
picking_id = 10  # picking you want to delete

# ---------------------------------------------------
# Authenticate
auth_url = f"{odoo_url}/web/session/authenticate"
auth_payload = {
    "jsonrpc": "2.0",
    "params": {"db": db, "login": username, "password": api_key},
}

session = requests.Session()
auth_response = session.post(auth_url, json=auth_payload)
auth_data = auth_response.json()
uid = auth_data.get("result", {}).get("uid")
if not uid:
    raise Exception(f"❌ Authentication failed: {auth_data}")
print(f"✅ Authenticated as UID {uid}")


def call_odoo(model, method, args=None, kwargs=None):
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {"model": model, "method": method, "args": args or [], "kwargs": kwargs or {}},
        "id": 1,
    }
    return session.post(f"{odoo_url}/web/dataset/call_kw/{model}/{method}", json=payload).json()


# ---------------------------------------------------
# Step 1️⃣: Find related stock moves
moves_result = call_odoo(move_model, "search_read", [[["picking_id", "=", picking_id]]], {"fields": ["id", "state", "name"]})
moves = moves_result.get("result", [])

if not moves:
    print("⚠️ No stock moves found for this picking.")
else:
    print(f"🔎 Found {len(moves)} related stock moves:")
    for mv in moves:
        print(f"   - {mv['name']} (state: {mv['state']})")

    move_ids = [mv["id"] for mv in moves]

    # Step 2️⃣: Cancel and reset moves to draft
    print("🛑 Cancelling stock moves...")
    call_odoo(move_model, "write", [move_ids, {"state": "cancel"}])
    print("📝 Resetting stock moves to draft...")
    call_odoo(move_model, "write", [move_ids, {"state": "draft"}])
    print("✅ Moves reset successfully.")

# ---------------------------------------------------
# Step 3️⃣: Try deleting picking again
print("🗑️ Attempting to delete picking...")
delete_result = call_odoo(picking_model, "unlink", [[picking_id]])

if "error" in delete_result:
    print(f"❌ Delete failed: {delete_result['error']['data']['message']}")
else:
    print(f"✅ Successfully deleted picking ID {picking_id}")

print("🎯 Process completed.")

import xmlrpc.client

# ------------------ CONFIG ------------------
odoo_url = "https://digitalvizta-klever-kitchen.odoo.com"
db = "digitalvizta-klever-kitchen-master-17296866"
username = "sawada48127@gmail.com"
password = "123"
product_template_id = 357  # Replace with your product_template ID

# ------------------ CONNECT ------------------
common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object')

# ------------------ 1️⃣ Cancel stock moves ------------------
stock_move_ids = models.execute_kw(db, uid, password,
    'stock.move', 'search', [[['product_id', '=', product_template_id]]])

if stock_move_ids:
    # Set all moves to cancel (only done moves must be returned first)
    for move_id in stock_move_ids:
        # Attempt to cancel
        try:
            models.execute_kw(db, uid, password, 'stock.move', 'action_cancel', [[move_id]])
        except Exception as e:
            print(f"Cannot cancel stock.move {move_id}: {e}")
    print(f"Stock moves canceled: {stock_move_ids}")

# ------------------ 2️⃣ Cancel sale orders ------------------
sale_order_line_ids = models.execute_kw(db, uid, password,
    'sale.order.line', 'search', [[['product_id', '=', product_template_id]]])

if sale_order_line_ids:
    sale_order_ids = models.execute_kw(db, uid, password,
        'sale.order.line', 'read', [sale_order_line_ids], {'fields': ['order_id']})
    sale_order_ids = list(set([s['order_id'][0] for s in sale_order_ids]))
    for order_id in sale_order_ids:
        try:
            models.execute_kw(db, uid, password, 'sale.order', 'action_cancel', [[order_id]])
        except Exception as e:
            print(f"Cannot cancel sale.order {order_id}: {e}")
    print(f"Sale orders canceled: {sale_order_ids}")

# ------------------ 3️⃣ Cancel accounting entries ------------------
account_move_line_ids = models.execute_kw(db, uid, password,
    'account.move.line', 'search', [[['product_id', '=', product_template_id]]])

if account_move_line_ids:
    account_move_ids = models.execute_kw(db, uid, password,
        'account.move.line', 'read', [account_move_line_ids], {'fields': ['move_id']})
    account_move_ids = list(set([m['move_id'][0] for m in account_move_ids]))
    for move_id in account_move_ids:
        try:
            models.execute_kw(db, uid, password, 'account.move', 'button_cancel', [[move_id]])
            models.execute_kw(db, uid, password, 'account.move', 'unlink', [[move_id]])
        except Exception as e:
            print(f"Cannot remove account.move {move_id}: {e}")
    print(f"Accounting entries removed: {account_move_ids}")

# ------------------ 4️⃣ Delete the product template ------------------
try:
    models.execute_kw(db, uid, password, 'product.template', 'unlink', [[product_template_id]])
    print(f"Product template {product_template_id} deleted successfully.")
except Exception as e:
    print(f"Cannot delete product template {product_template_id}: {e}")

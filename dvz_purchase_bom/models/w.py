def _get_report_values(self, docids, data=None):
    sale_orders = self.env['sale.order'].browse(data['sale_order_ids'])

    weekly_sales = defaultdict(lambda: defaultdict(float))
    unique_weeks = set()
    unique_products = set()
    product_consumption = defaultdict(float)
    product_stock_status = {}

    def collect_raw_materials(production):
        """Recursively collect raw materials from a production and its child BOMs."""
        production_date = production.date_start or production.create_date
        year = production_date.year
        week_number = production_date.isocalendar()[1]
        unique_weeks.add(week_number)

        for move in production.move_raw_ids.filtered(lambda m: m.state != 'cancel'):
            product = move.product_id
            product_name = product.name

            if product_name and isinstance(product_name, str):
                unique_products.add(product_name)
                weekly_sales[(year, week_number)][product_name] += move.product_uom_qty
                product_consumption[product.id] += move.product_uom_qty

        # Recursively collect from child MOs
        child_productions = self.env['mrp.production'].search([('origin', '=', production.name)])
        for child in child_productions:
            collect_raw_materials(child)

    # Step 1: Collect consumption data
    for order in sale_orders.filtered(lambda o: o.state == 'sale'):
        for production in order.mrp_production_ids:
            collect_raw_materials(production)

    # Step 2: Check stock and calculate shortages
    products = self.env['product.product'].browse(product_consumption.keys())
    for product in products:
        available_qty = product.qty_available
        consumed_qty = product_consumption[product.id]
        shortage = max(0, consumed_qty - available_qty)

        product_stock_status[product.name] = {
            'consumed': consumed_qty,
            'available': available_qty,
            'required': shortage,
        }

    sorted_weeks = sorted(unique_weeks)
    sorted_products = sorted(unique_products)

    return {
        'data': data,
        'docs': sale_orders,
        'weekly_sales': weekly_sales,
        'weeks': sorted_weeks,
        'products': sorted_products,
        'product_stock_status': product_stock_status,
        'year': 2025  # Or make dynamic if needed
    }

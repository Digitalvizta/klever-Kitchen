# Product BOM Type

This Odoo module adds a new boolean field **"Is BOM"** to the product form (`product.template`).  
It ensures that only **one** of the following product type flags can be selected at a time:

- **Can be Sold** (`sale_ok`)
- **Can be Purchased** (`purchase_ok`)
- **Is BOM** (`is_bom`)

## ✅ Features

- Adds an **Is BOM** checkbox to the Product form.
- Ensures mutual exclusivity between:
  - Can be Sold
  - Can be Purchased
  - Is BOM
- Automatic deselection of other fields when one is selected (via `@api.onchange`).
- Clean error handling with validation message if multiple options are selected.

## 📦 Installation

1. Clone or copy this module into your Odoo `addons` directory.
2. Update the app list:

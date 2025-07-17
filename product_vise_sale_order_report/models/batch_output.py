from datetime import date, timedelta
from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import UserError

# ------------------------------
# Year Week Model
# ------------------------------
class YearWeek(models.Model):
    _name = 'year.week'
    _description = 'Year Week'

    name = fields.Char('Year-Week', required=True, unique=True)



# ------------------------------
# Helper Method (post-init hook)
# ------------------------------
def populate_current_year_weeks(cr, registry):
    """Post-init hook to populate current year ISO weeks."""
    from odoo.api import Environment
    env = Environment(cr, SUPERUSER_ID, {})

    current_year = date.today().year
    start_date = date(current_year, 1, 1)
    end_date = date(current_year, 12, 31)

    weeks = set()
    day = start_date
    while day <= end_date:
        iso_year, iso_week, _ = day.isocalendar()
        if iso_year == current_year:
            week_str = f"{iso_year}-W{iso_week:02d}"
            weeks.add(week_str)
        day += timedelta(days=7)

    for week in sorted(weeks):
        if not env['year.week'].search([('name', '=', week)]):
            env['year.week'].create({'name': week})

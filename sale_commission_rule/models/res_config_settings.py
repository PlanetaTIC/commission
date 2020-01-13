# Copyright 2019 PlanetaTIC <info@planetatic.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_commission_rule_priority = fields.Selection([
        ('sequence', 'Order'),
        ('fixed_percent_lower', 'Lower fixed percentage'),
        ('fixed_percent_higher', 'Higher fixed percentage')],
        string='Sale commission rules priority',
        default='sequence',
        config_parameter='sale_commission_rule.priority')

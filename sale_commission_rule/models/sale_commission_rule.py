# Copyright 2019 PlanetaTIC <info@planetatic.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleCommissionRule(models.Model):
    _name = 'sale.commission.rule'
    _description = 'Commission rule'
    _order = 'sequence, id'

    sequence = fields.Integer(
        default=10)
    agent = fields.Many2one(
        'res.partner', 'Agent',
        ondelete='cascade', index=True,
        domain=[('agent', '=', True)])
    customer = fields.Many2one(
        'res.partner', 'Customer',
        ondelete='cascade', index=True,
        domain=[('customer', '=', True)])
    category = fields.Many2one(
        'product.category', 'Category',
        ondelete='cascade', index=True)
    product = fields.Many2one(
        'product.template', 'Product',
        ondelete='cascade', index=True,
        domain=[('sale_ok', '=', True)])
    commission = fields.Many2one(
        'sale.commission', 'Commission',
        ondelete='cascade', index=True,
        required=True)

    def get_commission(self, agent, customer, product):
        if not (agent and customer and product):
            return False
        rules = self.search([
            '|',
            ('agent', '=', agent.id),
            ('agent', '=', False),
            '|',
            ('customer', '=', customer.id),
            ('customer', '=', False),
            '|',
            ('category', 'parent_of', product.categ_id.id),
            ('category', '=', False),
            '|',
            ('product', '=', product.product_tmpl_id.id),
            ('product', '=', False),
        ])
        if not rules:
            return False
        priority = self.env['ir.config_parameter'].sudo().get_param(
            'sale_commission_rule.priority', 'sequence')
        if priority == 'sequence':
            return rules[0].commission
        rules = rules.sorted(
            key=lambda r: r.commission.fix_qty,
            reverse=(priority == 'fixed_percent_higher'))
        return rules[0].commission

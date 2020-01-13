# Copyright 2019 PlanetaTIC <info@planetatic.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.onchange('product_id')
    def _onchange_product_id_sale_commission_rule(self):
        self.agents = [(5, 0, 0)] + self._prepare_agents_vals_partner_product(
            self.invoice_id.partner_id, self.product_id)

    def _prepare_agents_vals(self):
        self.ensure_one()
        res = super()._prepare_agents_vals()
        return res + self._prepare_agents_vals_partner_product(
            self.invoice_id.partner_id, self.product_id)

    @api.model
    def create(self, vals):
        """Add agents for records created from automations instead of UI."""
        # We use this form as this is the way it's returned when no real vals
        agents_vals = vals.get('agents', [(6, 0, [])])
        if (agents_vals and agents_vals[0][0] == 6 and not agents_vals[0][2]):
            invoice = self.env['account.invoice'].browse(
                vals.get('invoice_id'))
            product = self.env['product.product'].browse(
                vals.get('product_id'))
            vals['agents'] = self._prepare_agents_vals_partner_product(
                invoice.partner_id, product)
        return super().create(vals)

    def button_edit_agents(self):
        self.ensure_one()
        res = super().button_edit_agents()
        view = self.env.ref(
            'sale_commission_rule.view_account_invoice_line_agent_only'
        )
        res.update({
            'views': [(view.id, 'form')],
            'view_id': view.id,
        })
        return res


class AccountInvoiceLineAgent(models.Model):
    _inherit = "account.invoice.line.agent"

    def _get_partner_product(self):
        self.ensure_one()
        return self.object_id.invoice_id.partner_id, self.object_id.product_id

# Copyright 2019 PlanetaTIC <info@planetatic.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleCommissionMixin(models.AbstractModel):
    _inherit = 'sale.commission.mixin'

    @api.model
    def _prepare_agents_vals_partner(self, partner):
        return []

    @api.model
    def _prepare_agents_vals_partner_product(self, partner, product):
        agents = []
        for agent in partner.agents:
            commission = self.env['sale.commission.rule'].get_commission(
                agent, partner, product)
            if commission:
                agents.append((0, 0, {
                    'agent': agent.id,
                    'commission': commission.id,
                }))
        return agents


class SaleCommissionLineMixin(models.AbstractModel):
    _inherit = 'sale.commission.line.mixin'

    def _get_partner_product(self):
        return False

    def _get_commission_partner_product(self, partner, product):
        self.ensure_one()
        return self.env['sale.commission.rule'].get_commission(
            self.agent, partner, product)

    @api.onchange('agent')
    def onchange_agent(self):
        self.commission = self._get_commission_partner_product(
            *self._get_partner_product())

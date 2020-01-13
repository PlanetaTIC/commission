# Copyright 2019 PlanetaTIC <info@planetatic.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sale Commission Rule',
    'summary': 'Allows commissions by customer, product and/or category',
    'version': '12.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Sales Management',
    'website': 'https://github.com/OCA/commission',
    'author': 'PlanetaTIC, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'sale_commission',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_invoice_view.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_view.xml',
        'views/sale_commission_rule_views.xml',
        'views/sale_order_view.xml',
    ],
}

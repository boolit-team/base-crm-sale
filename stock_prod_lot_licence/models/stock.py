# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC NOD Baltic
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning

class stock_production_lot_licence_type(models.Model):
    _name = 'stock.production.lot.licence_type'
    _description = 'Licence Type'

    name = fields.Char('Name')
    code = fields.Char('Code', help="Must match external system code if used in integration")

    @api.constrains('code')
    def _check_unique(self):
        types = self.search([('code', '=', self.code), ('id', '!=', self.id)])
        if types:
            raise Warning(_("Code must be unique"))

class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    licence = fields.Boolean('Licence')
    valid_date = fields.Date('Valid Date')
    order_date = fields.Date('Order Date')
    last_possible_activ_date = fields.Date('Last Possible Activ. Date')
    free = fields.Boolean('Unused')
    open_lic = fields.Boolean('Open')
    partner_id = fields.Many2one('res.partner', 'Partner')
    external_partner_id = fields.Many2one('res.partner', 'Licence User')
    quantity = fields.Integer('Quantity')
    all_quantity = fields.Integer('All Quantity')
    discount = fields.Float('Discount')
    email = fields.Char('Email')
    note_user = fields.Text('Note to Manufacturer')
    note_admin = fields.Text('Administrator Notes')
    force_system_price = fields.Float('Force System Price')
    active = fields.Boolean('Active', default=True)
    renewed_prodlot_id = fields.Many2one('stock.production.lot', 'Renewed Licence', domain=[('licence', '=', True)])
    renewed_quantity = fields.Integer('Renewed Quantity')
    # Fields for new Dexter api
    username = fields.Char('Username')
    password = fields.Char('Password')
    epli = fields.Char('EPLI')
    licence_key = fields.Char('Licence Key')
    common_tag = fields.Char('Common Tag')
    bundle_product_id = fields.Many2one('product.product', 'Bundle Product')
    bundle_quantity = fields.Integer('Bundle Quantity')
    licence_parent_id = fields.Many2one('stock.production.lot', 'Parent Licence')
    lic_create_date = fields.Date('Licence Creation Date')
    lic_create_user = fields.Integer('Licence Create User ID')
    lic_cancel_date = fields.Date('Licence Cancellation Date')
    lic_cancel_user = fields.Integer('Licence Cancel User ID')
    lic_modify_date = fields.Date('Licence Modification Date')
    lic_modify_user = fields.Integer('Licence Modify User')
    licence_type_id = fields.Many2one('stock.production.lot.licence_type', 'Licence Type')

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

from openerp import models, fields

class stock_production_lot(models.Model):
    _inherit = 'stock.production.lot'

    valid_date = fields.Date('Valid Date')
    order_date = fields.Date('Order Date')
    last_possible_activ_date = fields.Date('Last Possible Activ. Date')
    free = fields.Boolean('Unused')
    open_lic = fields.Boolean('Open')
    partner_id = fields.Many2one('res.partner', 'Partner')
    external_partner_id = fields.Many2one('res.partner', 'Licence User')
    quantity = fields.Integer('Quantity')
    all_quantity = fields.Float('All Quantity') #Integer maybe?
    discount = fields.Float('Discount')
    email = fields.Char('Email')
    note_user = fields.Text('Note to Manufacturer')
    note_admin = fields.Text('Administrator Notes')
    force_system_price = fields.Float('Force System Price')
    active = fields.Boolean('Active')

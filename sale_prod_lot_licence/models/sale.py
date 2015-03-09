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

from openerp import models, fields, api

class sale_order(models.Model):
    _inherit = 'sale.order'
    
    partner_licence_id = fields.Many2one('res.partner', 'Licence User')

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    licence_id = fields.Many2one('stock.production.lot', 'Licence', domain=[('licence', '=', True)])
    lic_key = fields.Char('Renewed/Enlarged Licence')
    note_user = fields.Text('Note to Manufacturer')

    @api.onchange('licence_id')
    def onchange_licence_id(self):
        if self.licence_id:
            self.general_qty = self.licence_id.all_quantity
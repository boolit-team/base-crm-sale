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

    partner_order_id = fields.Many2one('res.partner', 'Ordering Contact', domain=[('is_company', '=', False)])

    @api.multi
    def onchange_partner_id(self, partner_id):
        vals = super(sale_order, self).onchange_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            for child in partner.child_ids:
                if child.type == 'contact':
                    vals['value']['partner_order_id'] = child.id
                    return vals
            if partner.child_ids:
                vals['value']['partner_order_id'] = partner.child_ids[0].id
        return vals
    
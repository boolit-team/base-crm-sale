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

class product_uom(models.Model):
    _inherit = 'product.uom'

    @api.model
    def _check_sum_uom(self, qty, product, uom):
        if product and qty > 0.0 and product.mes_type == 'variable' and uom.uom_type == 'reference':
            return True
        return False

    @api.model
    def get_sum_uom(self, qty, product, uom):
        if self._check_sum_uom(qty, product, uom):
            uom = self.search([('uom_type', '=', 'bigger'), ('category_id', '=', uom.category_id.id), ('factor', '=', 1 / qty)], limit=1)
            return uom

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    general_qty = fields.Float('Sum Quantity')

    @api.onchange('general_qty')
    def onchange_general_qty(self):
            sum_uom = self.env['product.uom'].get_sum_uom(self.general_qty, self.product_id, self.product_uom)
            if sum_uom:
                self.product_uom = sum_uom.id

    @api.multi
    def product_id_change(self, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):                
        vals = super(sale_order_line, self).product_id_change(pricelist=pricelist, product=product, qty=qty,
            uom=uom, qty_uos=qty_uos, uos=uos, name=name, partner_id=partner_id,
            lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging, fiscal_position=fiscal_position, flag=flag)
        if vals.get('value'):
            print 'value passed'
            value = vals['value']
            if value.get('product_uom'):
                print 'product_uom passed'
                uom_obj = self.env['product.uom']
                default_uom = uom_obj.browse(value['product_uom'])
                sum_uom = uom_obj.get_sum_uom(self.general_qty, self.product_id, default_uom) 
                if sum_uom:
                    print 'sum_uom passed'
                    vals['value']['product_uom'] = sum_uom.id
        return vals


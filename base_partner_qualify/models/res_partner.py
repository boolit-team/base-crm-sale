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

class res_partner(models.Model):
    _inherit = 'res.partner'

    qualified = fields.Boolean('Qualified')
    show_in_name = fields.Boolean('Show in Name')

    @api.onchange('qualified')
    def onhange_qualified(self):
        if self.qualified:
            self.show_in_name = True
        else:
            self.show_in_name = False

    @api.multi
    def name_get(self):
        res = super(res_partner, self).name_get()
        res_dict = dict(res)
        for record in self:
            if record.qualified and record.show_in_name:
                res_dict[record.id] = "%s + QLF" % (res_dict[record.id])

        return res_dict.items()


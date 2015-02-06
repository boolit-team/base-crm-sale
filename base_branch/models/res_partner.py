# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: NOD Baltic JSC
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
from openerp.osv import fields as old_fields
from openerp.addons.base.res.res_partner import res_partner as res_partner_orig

class res_partner(models.Model):
    _inherit = 'res.partner'
 
    _display_name_store_triggers = {
        'res.partner': (lambda self,cr,uid,ids,context=None: self.search(cr, uid, [('id','child_of',ids)], context=dict(active_test=False)),
                        ['parent_id', 'is_company', 'name', 'parent_root_id', 'is_branch'], 10)
    }

    _commercial_partner_store_triggers = {
        'res.partner': (lambda self,cr,uid,ids,context=None: self.search(cr, uid, [('id','child_of',ids)], context=dict(active_test=False)),
                        ['parent_id', 'is_company', 'parent_root_id', 'is_branch'], 10)
    }    

    _columns = {
        'display_name': old_fields.function(res_partner_orig._display_name, type='char', string='Name', store=_display_name_store_triggers, select=True),
        'commercial_partner_id': old_fields.function(res_partner_orig._commercial_partner_id, type='many2one', relation='res.partner', 
            string='Commercial Entity', store=_commercial_partner_store_triggers),
    }

    is_branch = fields.Boolean('Is Branch?')
    parent_root_id = fields.Many2one('res.partner', 'Main Partner', domain=[('is_company', '=', True), ('is_branch', '=', False)])

    @api.multi
    def onchange_type(self, is_company):
        value = {}
        value['title'] = False
        if is_company:
            value['use_parent_address'] = False
            domain = {'title': [('domain', '=', 'partner')]}
        else:
            domain = {'title': [('domain', '=', 'contact')]}
            value['is_branch'] = False
        return {'value': value, 'domain': domain}    

    @api.multi
    def name_get(self):
        res = super(res_partner, self).name_get()
        res_dict = dict(res)
        for record in self:
            if record.parent_root_id and record.is_branch:
                res_dict[record.id] = "%s / %s" % (record.parent_root_id.name, res_dict[record.id])
        return res_dict.items()
    
    @api.multi
    def _commercial_partner_compute(self, name, args):
        """ Returns the partner that is considered the commercial
        entity of this partner. The commercial entity holds the master data
        for all commercial fields (see :py:meth:`~_commercial_fields`) """
        results = super(res_partner, self)._commercial_partner_compute(name, args)
        for partner in self:
            if partner.is_company and partner.is_branch and partner.parent_root_id:
                results[partner.id] = partner.parent_root_id.id
        return results

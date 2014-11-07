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

from openerp import models, fields
from openerp import api
class res_partner(models.Model):
    _inherit = 'res.partner'

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

    '''
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = []
        for record in self.browse(cr, uid, ids, context=context):
            name = record.name
            if record.parent_id and not record.is_company:
                name =  "%s, %s" % (record.parent_id.name, name)
            if record.parent_root_id:
                name = "%s / %s" % (record.parent_root_id.name, name)
            if context.get('show_address_only'):
                name = self._display_address(cr, uid, record, without_company=True, context=context)
            if context.get('show_address'):
                name = name + "\n" + self._display_address(cr, uid, record, without_company=True, context=context)
            name = name.replace('\n\n','\n')
            name = name.replace('\n\n','\n')
            if context.get('show_email') and record.email:
                name = "%s <%s>" % (name, record.email)
            res.append((record.id, name))
        return res
    '''

    @api.multi
    def name_get(self):
        res = super(res_partner, self).name_get()
        res_dict = dict(res)
        for record in self:
            if record.parent_root_id:
                res_dict[record.id] = "%s / %s" % (record.parent_root_id.name, res_dict[record.id])
        return res_dict.items()
    
    @api.multi
    def _commercial_partner_compute(self, name, args):
        """ Returns the partner that is considered the commercial
        entity of this partner. The commercial entity holds the master data
        for all commercial fields (see :py:meth:`~_commercial_fields`) """
        results = super(res_partner, self)._commercial_partner_compute(name, args)
        for partner in self:
            if partner.is_company and partner.is_branch:
                results[partner.id] = partner.parent_root_id.id
        return results

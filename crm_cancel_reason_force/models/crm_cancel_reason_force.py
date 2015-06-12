# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC Boolit
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

from openerp import fields, models, api, _

class crm_lead(models.Model):
    _inherit = 'crm.lead'      

    @api.multi
    def case_mark_lost(self):
        submitted_reasons = self.env.context.get('submitted_reasons', False)
        if not submitted_reasons:
            view = self.env.ref('crm_cancel_reason_force.view_force_cancel_reason_form')
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'force.cancel.reason',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view.id,
                'context': {'default_opportunity_id': self.ids[0]},
                'target': 'new',
                'nodestroy': True,                    
            }
        else:
            return super(crm_lead, self).case_mark_lost()


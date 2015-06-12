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
from openerp.exceptions import Warning

class force_cancel_reason(models.TransientModel):
    _name = 'force.cancel.reason'
    _description = 'Force Cancel Reason'

    opportunity_id = fields.Many2one('crm.lead', 'Opportunity')
    reason_ids = fields.One2many('base.reason', 'opportunity_id', 'Reasons', related="opportunity_id.reason_ids")

    @api.multi
    def submit_reasons(self):
        if not self.reason_ids:
            raise Warning(_("You must enter at least one reason!"))
        opp_ids = self.env.context and self.env.context.get('active_ids', [])
        opportunities = self.env['crm.lead'].browse(opp_ids)
        # We need this only if there are more than one opportunity
        if len(opportunities) > 1:
            for opp in opportunities:
                opp.reason_ids = self.reason_ids.copy()
        opportunities.with_context(submitted_reasons=True).case_mark_lost()
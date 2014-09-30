# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Andrius Laukavičius. Copyright JSC NOD Baltic
#    
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


class calendar_event(models.Model):
    _inherit = 'calendar.event'

    STATES = [('draft', 'Unconfirmed'), ('open', 'Confirmed'), ('cancel', 'Cancelled'), ('done', 'Done')]

    meet_state = fields.Selection(STATES, string='Status', readonly=True, track_visibility='onchange', default='draft')
    stage_log_id = fields.Many2one('crm.lead.stage_log', 'Lead/Opp. Stages Log')

    @api.multi
    def write(self, vals):
        if vals.get('meet_state') == 'done' and self.opportunity_id:
            stage_log = self.opportunity_id.get_stage_log()
            if stage_log:
                #get last stage log
                vals['stage_log_id'] = stage_log[-1].id
        return super(calendar_event, self).write(vals)    
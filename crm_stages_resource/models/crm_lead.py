# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: Andrius Laukavičius
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
from datetime import datetime, timedelta
from openerp.exceptions import Warning
from openerp.tools.translate import _
import pytz

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    def _compute_stage_deadline(self):
        for rec in self:
            rec.stage_deadline = None      
            stage_config = rec.get_stage_config()
            stage_logs = rec.get_stage_log()
            if stage_config and stage_logs:
                stage_log = stage_logs[-1]              
                create_date = datetime.strptime(stage_log.create_date, "%Y-%m-%d %H:%M:%S")
                if not rec.env.user.tz:
                    raise Warning(_("%s timezone is not set!" % (rec.env.user.name)))
                rec.stage_deadline = create_date + timedelta(days=stage_config.days_for_stage)
                if rec.section_id.uom_id:
                    if stage_config.working_hours or rec.section_id.default_working_hours:             
                        working_hours = stage_config.working_hours or rec.section_id.default_working_hours
                        hours_for_stage = int(stage_config.days_for_stage * rec.section_id.uom_id.factor)
                        end_dt = working_hours.schedule_hours(hours=hours_for_stage, day_dt=create_date)
                        end_dt = end_dt[-1][-1][-1]
                        tz = pytz.timezone(rec.env.user.tz)
                        end_dt = tz.localize(end_dt)
                        end_dt = end_dt.astimezone(pytz.utc)                        
                        rec.stage_deadline = end_dt                                
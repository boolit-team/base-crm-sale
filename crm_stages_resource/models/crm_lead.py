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

	@api.one
	def _compute_stage_deadline(self):
		self.stage_deadline = None		
		stage_config = self.get_stage_config()
		stage_logs = self.get_stage_log()
		if stage_config and stage_logs:
			stage_log = stage_logs[-1]				
			create_date = datetime.strptime(stage_log.create_date, "%Y-%m-%d %H:%M:%S")
			if not self.user_id.tz:
				raise Warning(_("%s timezone is not set!" % (self.user_id.name)))
			tz = pytz.timezone(self.user_id.tz)
			create_date = tz.localize(create_date)
			create_date = create_date.astimezone(pytz.utc)
			self.stage_deadline = create_date + timedelta(days=stage_config.days_for_stage)
			if self.section_id.uom_id:				
				employee = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)], limit=1)
				if employee and employee.contract_id:
					contract = employee.contract_id
					if contract and contract.working_hours:
						hours_for_stage = int(stage_config.days_for_stage * self.section_id.uom_id.factor)
						end_dt = contract.working_hours.schedule_hours(hours=hours_for_stage, day_dt=create_date)
						end_dt = end_dt[-1][-1][-1]
						#end_dt = tz.localize(end_dt) - localized automatically
						#end_dt = end_dt.astimezone(pytz.utc)						
						self.stage_deadline = end_dt								
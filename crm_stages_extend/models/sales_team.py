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

from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.tools.translate import _
class crm_case_section_stage_config(models.Model):
	_name = 'crm.case.section.stage_config'
	_description = 'Sales Team Stages Configuration'

	section_id = fields.Many2one('crm.case.section', 'Sales Team')
	stage_id = fields.Many2one('crm.case.stage', 'Stage', domain=[('type', '!=', 'lead')], required=True)
	next_stage_id = fields.Many2one('crm.case.stage', 'Next Stage', domain=[('type', '!=', 'lead')])
	prev_stage_id = fields.Many2one('crm.case.stage', 'Previous Stage', domain=[('type', '!=', 'lead')])
	user_id = fields.Many2one('res.users', 'Responsible')
	sequence = fields.Integer('Sequence')
	days_for_stage = fields.Integer('Days for Stage', required=True)

	_order = 'sequence'

class sales_team(models.Model):
	_inherit = 'crm.case.section'

	stage_config_ids = fields.One2many('crm.case.section.stage_config', 'section_id', 'Stages Config')
	default_stage = fields.Many2one('crm.case.stage', 'Default Stage', 
		domain=[('type', '!=', 'lead'), ('probability', '!=', 100.0), ('probability', '!=', 0.0)])
	@api.one
	@api.constrains('stage_config_ids', 'stage_ids')
	def _check_config(self):
		stages = []
		for config in self.stage_config_ids:
			if config.stage_id.id not in stages:
				stages.append(config.stage_id.id)
			else:
				raise Warning(_('Stage in Config Must be Unique!'))
			if config.stage_id not in self.stage_ids:
				raise Warning(_('"%s" Stage is not defined in Sales Team Stages!' % (config.stage_id.name)))




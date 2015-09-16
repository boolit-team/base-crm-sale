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

    section_id = fields.Many2one('crm.case.section', 'Sales Team', ondelete='cascade')
    stage_id = fields.Many2one('crm.case.stage', 'Stage', domain=[('type', '!=', 'lead'), ('probability', '!=', 0.0)], required=True)
    next_stage_id = fields.Many2one('crm.case.stage', 'Next Stage', domain=[('type', '!=', 'lead'), ('probability', '!=', 0.0)])
    back_stage_id = fields.Many2one('crm.case.stage', 'Back Stage', domain=[('type', '!=', 'lead'), ('probability', '!=', 0.0)])
    user_id = fields.Many2one('res.users', 'Responsible')
    sequence = fields.Integer('Sequence')
    days_for_stage = fields.Integer('Days for Stage', required=True)

    _order = 'sequence'

class sales_team(models.Model):
    _inherit = 'crm.case.section'

    stage_config_ids = fields.One2many('crm.case.section.stage_config', 'section_id', 'Stages Config')
    default_stage_id = fields.Many2one('crm.case.stage', 'Default Stage', 
       domain=[('type', '!=', 'lead'), ('probability', '!=', 100.0), ('probability', '!=', 0.0)])
    track_act = fields.Boolean('Track Activities', help="Track Sales Team Activities", default=True)

    @api.one
    def init_config(self):
        config_obj = self.env['crm.case.section.stage_config']
        if self.stage_ids:
            self.default_stage_id = self.stage_ids[0].id
        else:
            raise Warning(_("There are no stages in sales team!"))
        if not self.stage_config_ids:
            config_line = None
            for stage in self.stage_ids:
                if stage.type != 'lead' and stage.probability != 0.0:
                    if config_line and (config_line.stage_id.probability != 0.0 \
                        or config_line.stage_id.probability != 100.0):
                        config_line.next_stage_id = stage.id
                    config_line = config_obj.create({
                        'stage_id': stage.id, 
                        'sequence': stage.sequence,
                        'days_for_stage': 0, 
                        'section_id': self.id})
        else:
            raise Warning(_("Init Configuration settings can only be used on empty config!"))

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





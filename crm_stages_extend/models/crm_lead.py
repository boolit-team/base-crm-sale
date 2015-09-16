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
from datetime import datetime, timedelta
from openerp.exceptions import Warning
from openerp.tools.translate import _

class crm_lead_stage_log(models.Model):
    _name = 'crm.lead.stage_log'
    _description = 'Lead/Opp. Stages Log'

    lead_id = fields.Many2one('crm.lead', 'Lead/Opportunity')
    user_id = fields.Many2one('res.users', 'Responsible')
    stage_id = fields.Many2one('crm.case.stage', 'Stage')
    prev_stage_id = fields.Many2one('crm.case.stage', 'Previous Stage')
    section_id = fields.Many2one('crm.case.section', 'Sales Team')
    lead_type = fields.Selection([('lead', 'Lead'), ('opportunity', 'Opportunity')], 'Type')
    stage_activity_id = fields.Many2one('crm.stage.activity', 'Stage Activity')
    phonecall_ids = fields.One2many('crm.phonecall', 'stage_log_id', 'Phonecalls')
    event_ids = fields.One2many('calendar.event', 'stage_log_id', 'Meetings')

class crm_phonecall(models.Model):
    _inherit = 'crm.phonecall'

    stage_log_id = fields.Many2one('crm.lead.stage_log', 'Lead/Opp. Stages Log')

    @api.multi
    def write(self, vals):
        if vals.get('meet_state') == 'done' and self.opportunity_id:
            stage_log = self.opportunity_id.get_stage_log()
            if stage_log:
                #get last stage log
                vals['stage_log_id'] = stage_log[-1].id
        return super(crm_phonecall, self).write(vals)

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    stage_deadline = fields.Datetime('Stage Deadline', compute="_compute_stage_deadline")
    planned_profit = fields.Float('Expected Profit', track_visibility='always')
    title_action = fields.Char('Next Action', track_visibility='onchange')
    date_action = fields.Date('Next Action Date', select=True, track_visibility='onchange')
    
    _defaults = {
        'probability': 1.0,
    }
        

    @api.multi
    @api.returns('crm.case.section.stage_config')
    def get_stage_config(self):
        stage_config = self.env['crm.case.section.stage_config'].search(
            [('section_id', '!=', False), ('section_id', '=', self.section_id.id), ('stage_id', '=', self.stage_id.id)])
        while stage_config:
            return stage_config 

    @api.multi
    @api.returns('crm.lead.stage_log')
    def get_stage_log(self):
        stage_log = self.env['crm.lead.stage_log'].search(
            [('lead_id', '=', self.id), ('stage_id', '=', self.stage_id.id)])
        while stage_log:
            return stage_log    

    @api.model
    def _base_log_dict(self, lead=None):
        obj = self
        if lead:
            obj = lead
        log_vals = {'lead_id': obj.id, 'user_id': obj.user_id.id, 
            'stage_id': obj.stage_id.id, 'lead_type': obj.type, 'section_id': obj.section_id.id}
        return log_vals                         

    @api.one
    def next_stage(self):
        stage_config = self.get_stage_config()
        if stage_config:
            if stage_config.next_stage_id: 
                if stage_config.next_stage_id:
                    self.stage_id = stage_config.next_stage_id.id           
                    stage_config_next = self.get_stage_config()
                    if  stage_config_next and stage_config_next.user_id:
                        self.user_id = stage_config_next.user_id.id 
                    log_vals = self._base_log_dict()
                    log_vals['prev_stage_id'] = stage_config.stage_id.id
                    activity_obj = self.env['crm.stage.activity']
                    activity = activity_obj.get_activity(self, log_vals.get('prev_stage_id'))
                    if activity:
                        log_vals['stage_activity_id'] = activity.id                        
                    self.env['crm.lead.stage_log'].create(log_vals)
                    if self.stage_id.probability == 100.0: #create one more log if opp have been won
                        activity = activity_obj.get_activity(self, self.stage_id.id)
                        log_vals['stage_activity_id'] = activity.id
                        self.env['crm.lead.stage_log'].create(log_vals)
                else:
                    raise Warning(_('"%s" Stage is not Set for %s Team!' % (stage_config.next_stage_id.name, self.section_id.name)))
            else:
                raise Warning(_("Next stage in config is missing!"))
        else:
            raise Warning(_("Stage config is missing!"))

    @api.one
    def back_stage(self):
        stage_config = self.get_stage_config()
        if stage_config and stage_config.back_stage_id:
            self.stage_id = stage_config.back_stage_id.id
        else:
            raise Warning(_("Back stage is not defined for this stage\n or stage config is missing!"))

    @api.one
    def reset_stage(self):
        if self.section_id.default_stage_id:
            self.stage_id = self.section_id.default_stage_id.id                 
        else:
            raise Warning(_('There is no default Stage defined!'))                  

    @api.model
    def create(self, vals):
        """
        Logs init stage on creation.
        """
        lead = super(crm_lead, self).create(vals)
        log_vals = self._base_log_dict(lead) 
        activity = self.env['crm.stage.activity'].get_activity(lead)
        if activity:
            log_vals['stage_activity_id'] = activity.id
        self.env['crm.lead.stage_log'].create(log_vals)
        return lead

    @api.multi
    def write(self, vals):
        for lead in self: 
            if lead.type == 'lead' and vals.get('stage_id'):
                log_vals = self._base_log_dict(lead)
                log_vals = dict(log_vals, stage_id=vals.get('stage_id'), prev_stage_id=lead.stage_id.id)
                activity = self.env['crm.stage.activity'].get_activity(lead, vals.get('stage_id'))
                if activity:
                    log_vals['stage_activity_id'] = activity.id                
                self.env['crm.lead.stage_log'].create(log_vals)
        return super(crm_lead, self).write(vals)

    @api.model
    def _convert_opportunity_data(self, lead, customer, section_id=False):
        """
        Logs stage information on conversion
        """
        log_vals = self._base_log_dict(lead)
        log_vals['lead_type'] = 'opportunity'
        if lead.stage_id.probability != 0.0:
            activity = self.env['crm.stage.activity'].get_activity(lead, lead_type='opportunity')
            if activity:
                log_vals['stage_activity_id'] = activity.id         
            self.env['crm.lead.stage_log'].create(log_vals)
        return super(crm_lead, self)._convert_opportunity_data(lead, customer, section_id=False)

    @api.one
    def case_mark_won(self):
        log_vals = self._base_log_dict(self)
        if self.section_id:
            stage = self.env['crm.case.stage'].search([('probability', '=', 100.0), ('section_ids', 'in', [self.section_id.id])], limit=1)
            if stage:
                activity_obj = self.env['crm.stage.activity']
                activity = activity_obj.get_activity(self, stage_id=stage.id)
                if activity:
                    log_vals['stage_activity_id'] = activity.id         
                self.env['crm.lead.stage_log'].create(log_vals)
                #logging stage it gone from to won stage
                activity2 = activity_obj.get_activity(self)
                if activity2:
                    log_vals['stage_activity_id'] = activity2.id
                    self.env['crm.lead.stage_log'].create(log_vals)
        return super(crm_lead, self).case_mark_won()

    @api.one
    def case_mark_lost(self):
        log_vals = self._base_log_dict(self)
        if self.section_id:
            stage = self.env['crm.case.stage'].search([('probability', '=', 0.0), ('section_ids', 'in', [self.section_id.id]), ('type', '!=', 'lead')], limit=1)
            if stage:
                activity_obj = self.env['crm.stage.activity']
                activity = activity_obj.get_activity(self, stage_id=stage.id)
                if activity:
                    log_vals['stage_activity_id'] = activity.id         
                self.env['crm.lead.stage_log'].create(log_vals)
        return super(crm_lead, self).case_mark_lost()

    def _compute_stage_deadline(self):
        for rec in self:
            rec.stage_deadline = None      
            stage_config = rec.get_stage_config()
            if stage_config:
                stage_logs = rec.get_stage_log()
                if stage_logs:
                    stage_log = stage_logs[-1] #get the last log of stage               
                    create_date = datetime.strptime(stage_log.create_date, "%Y-%m-%d %H:%M:%S")             
                    rec.stage_deadline = create_date + timedelta(days=stage_config.days_for_stage)
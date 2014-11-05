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
from datetime import date, datetime

LEAD_TYPE = [('lead','Lead'), ('opportunity', 'Opportunity')]

class crm_stage_activity(models.Model):
    _name = 'crm.stage.activity'
    _description = 'CRM Stages Activity Report'     
    
    date = fields.Date('Date')
    day = fields.Char('Day', size=128, readonly=True)
    stage_id = fields.Many2one('crm.case.stage', 'Stage')
    stage_log_ids = fields.One2many('crm.lead.stage_log', 'stage_activity_id', 'Stage Logs')
    section_id = fields.Many2one('crm.case.section', 'Sales Team')
    activities_numb = fields.Integer(string='Activity Count', compute="_count_activity_data")
    users_numb = fields.Integer(string='Salesmen Count', compute="_count_activity_data")
    revenue_sum = fields.Float(string="Revenue Sum", compute="_count_activity_data")
    profit_sum = fields.Float(string="Profit Sum", compute="_count_activity_data")
    phonecalls_numb = fields.Integer("Phonecalls Count", compute="_count_activity_data")
    meetings_numb = fields.Integer("Meetings Count", compute="_count_activity_data")
    lead_type = fields.Selection(LEAD_TYPE, 'Type')

    @api.one
    @api.depends('stage_log_ids')
    def _count_activity_data(self):
        self.activities_numb = len(self.stage_log_ids)
        users = []
        phonecalls = 0
        meetings = 0
        revenue = 0.0
        profit = 0.0
        for stage_log in self.stage_log_ids:
            if stage_log.user_id.id not in users:
                users.append(stage_log.user_id.id)
            phonecalls += len(stage_log.phonecall_ids)
            meetings += len(stage_log.event_ids)
            revenue += stage_log.lead_id.planned_revenue
            profit += stage_log.lead_id.planned_profit
        self.users_numb = len(users)
        self.phonecalls_numb = phonecalls
        self.meetings_numb = meetings
        self.revenue_sum = revenue
        self.profit_sum = profit             
    
    @api.model
    def get_activity(self, lead, stage_id=None, lead_type=None, dt=None):
        """
        Returns matching activity for lead
        """
        if not dt:
            dt = date.today().strftime('%Y-%m-%d')
        return self.search([('date', '=', dt), ('stage_id', '=', stage_id if stage_id else lead.stage_id.id), 
            ('section_id', '=', lead.section_id.id), 
            ('lead_type', '=', lead_type if lead_type else lead.type)], limit=1)

    
    
    @api.cr_uid
    def _init_activity(self, cr, uid, ids=None, context=None):
        """
        Only For Scheduller
        """
        team_obj = self.pool.get('crm.case.section')
        section_ids = team_obj.search(cr, uid, [('active', '=', True), ('track_act', '=', True)])
        vals = {
            'date': date.today().strftime('%Y-%m-%d'),
            'day': date.today().strftime('%Y-%m-%d'),               
        }
        for team in team_obj.browse(cr, uid, section_ids, context=context):
            vals['section_id'] = team.id
            for stage_id in team.stage_ids:
                activity_domain = [('date' , '=', date.today().strftime('%Y-%m-%d')), 
                    ('stage_id', '=', stage_id.id), ('section_id', '=', team.id)]
                vals['stage_id'] = stage_id.id
                if stage_id.type != 'both':
                    activity_domain.append(('lead_type', '=', stage_id.type))
                    if not self.search(cr, uid, activity_domain):
                        vals['lead_type'] = stage_id.type                                
                        self.create(cr, uid, vals, context=context)
                else: #specific exception to handle stages that go in both lead and opp.
                    for tp in LEAD_TYPE:
                        both_domain = activity_domain
                        both_domain.append(('lead_type', '=', tp[0]))
                        if not self.search(cr, uid, both_domain):
                            vals['lead_type'] = tp[0]
                            self.create(cr, uid, vals, context=context)
        return True        
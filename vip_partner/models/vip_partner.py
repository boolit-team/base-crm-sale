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

class res_partner(models.Model):
    _inherit = 'res.partner'

    vip = fields.Boolean('VIP')

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    vip = fields.Boolean('VIP')
    
    @api.multi
    def on_change_partner_id(self, partner_id):
        vals = super(crm_lead, self).on_change_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            vals['value']['vip'] = partner.vip
        return vals

class crm_helpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    vip = fields.Boolean('VIP')
    
    @api.multi
    def on_change_partner_id(self, partner_id):
        vals = super(crm_helpdesk, self).on_change_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            vals['value']['vip'] = partner.vip
        return vals

class project(models.Model):
    _inherit = 'project.project'

    vip = fields.Boolean('VIP')

    @api.multi
    def onchange_partner_id(self, partner_id):
        vals = super(project, self).onchange_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            vals['value']['vip'] = partner.vip
        return vals     

class project_task(models.Model):
    _inherit = 'project.task'

    vip = fields.Boolean('VIP') 

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.vip = self.partner_id.vip     
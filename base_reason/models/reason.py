# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC NOD Baltic
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

class reason_tier_one(models.Model):
    _name = 'base.reason.tier.one'
    _description = 'Tier One Reason'
    
    name = fields.Char('First Tier Reason')
    model_ids = fields.Many2many('ir.model', 'ir_model_tier_one_rel', 'tier_one_id', 'model_id', 'Filter to', 
        help="Can be used for specific implementation to only show reasons where you want")


class reason_tier_two(models.Model):
    _name = 'base.reason.tier.two'
    _description = 'Tier Two Reason'

    name = fields.Char('Second Tier Reason')
    parent_id = fields.Many2one('base.reason.tier.one', 'Parent')

class reason_tier_three(models.Model):
    _name = 'base.reason.tier.three'
    _description = 'Tier Three Reason'

    name = fields.Char('Third Tier Reason')
    parent_id = fields.Many2one('base.reason.tier.two', 'Parent')    


class reason(models.Model):
    _name = 'base.reason'
    _description = 'Reasons'

    tier_one_id = fields.Many2one('base.reason.tier.one', 'Tier One Reason')
    tier_two_id = fields.Many2one('base.reason.tier.two', 'Tier Two Reason')
    tier_three_id = fields.Many2one('base.reason.tier.three', 'Tier Three Reason')
    details = fields.Char('Details')

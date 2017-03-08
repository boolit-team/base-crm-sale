# -*- encoding: utf-8 -*-

from odoo import models, fields, api


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

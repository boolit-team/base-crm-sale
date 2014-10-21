from openerp import models, fields

class crm_lead(models.Model):
    _inherit = 'crm.lead'
    
    company_registry = fields.Char('Company Registry', help="Registry code")



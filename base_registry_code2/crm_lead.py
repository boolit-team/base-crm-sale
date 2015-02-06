from openerp import models, fields, api

class crm_lead(models.Model):
    _inherit = 'crm.lead'
    
    company_registry = fields.Char('Company Registry', help="Registry code")

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """
        Extends original method to also add:
            'company_registry'
        """        
        partner_id = super(crm_lead, self)._lead_create_contact(lead, name, is_company, parent_id=parent_id)
        partner = self.env['res.partner'].browse(partner_id)
        partner.company_registry = lead.company_registry
        return partner_id

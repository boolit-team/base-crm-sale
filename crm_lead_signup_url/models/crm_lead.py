# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC Boolit
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
from openerp import models, api

class CRMLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def get_signup_url(self):
        # This method might be called from other model, so it should safely return 
        # nothing if source crm.lead object is not set
        if len(self.ids) == 1:
            context_signup = dict(self._context, signup_valid=True)
            partner = self.user_id.partner_id
            if partner:
                return partner.with_context(context_signup)._get_signup_url_for_action(action='mail.action_mail_redirect',
                    model=self._name, res_id=self.id,
                )[partner.id]
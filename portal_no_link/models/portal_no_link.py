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

class mail_mail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def _get_partner_access_link(self, mail, partner=None):
        """
        Overrides to return nothing if partner has portal user or has not user.
        """
        if partner and all([x.has_group('base.group_portal') for x in partner.user_ids]):
            return None
        else:
            return super(mail_mail, self)._get_partner_access_link(mail, partner)

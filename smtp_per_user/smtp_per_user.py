# -*- coding: utf-8 -*-
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
from openerp import models, fields, api
from email.utils import parseaddr, formataddr

class ir_mail_server(models.Model):
    _inherit = "ir.mail_server"

    user_id = fields.Many2one('res.users', string="Owner")
    email_name = fields.Char('Email Name', help="Overrides default email name")
    force_use = fields.Boolean('Force Use', help="If checked and this server is chosen to send mail message, It will ignore owners mail server")

    @api.model
    def replace_email_name(self, old_email):
        """
        Replaces email name if new one is provided
        """
        if self.email_name:
            old_name, email = parseaddr(old_email)
            return formataddr((self.email_name, email))
        else:
            return old_email    

class mail_mail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send(self, auto_commit=False, raise_exception=False):
        ir_mail_server_obj = self.env['ir.mail_server']
        res_user_obj = self.env['res.users']
        for email in self:
            if not email.mail_server_id.force_use:
                user = res_user_obj.search([('partner_id', '=', email.author_id.id)], limit=1)
                if user:
                    mail_server = ir_mail_server_obj.search([('user_id', '=', user.id)], limit=1)
                    if mail_server:
                        email.mail_server_id = mail_server.id
            email.email_from = email.mail_server_id.replace_email_name(email.email_from)
        return super(mail_mail, self).send(auto_commit=False, raise_exception=False)

# -*- coding: utf-8 -*-

from email.utils import parseaddr, formataddr

from odoo import models, fields, api


class IrMailServer(models.Model):
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


class MailMail(models.Model):
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
        return super(MailMail, self).send(auto_commit=auto_commit,
                                          raise_exception=raise_exception)

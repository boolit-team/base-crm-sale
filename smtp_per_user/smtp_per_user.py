# -*- coding: utf-8 -*-

from openerp import models, fields

class ir_mail_server(models.Model):
    _inherit = "ir.mail_server"

    user_id = fields.Many2one('res.users', string="Owner")

class ir_mail_server(models.Model):
    _inherit = "ir.mail_server"

    @api.one
    def send_mail(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False):
        mail_server = self.search([('user_id', '=', self.env.uid)], limit=1)
        if mail_server:
            mail_server_id = mail_server.id
        return super(ir_mail_server, self).send_email(message, mail_server_id, smtp_server, smtp_port,
                   smtp_user, smtp_password, smtp_encryption, smtp_debug)

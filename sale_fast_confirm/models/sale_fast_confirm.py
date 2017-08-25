# -*- coding: utf-8 -*-

from odoo import models, api


class SaleOrder(models.Model):
    """Extend with fast confirmation."""

    _inherit = 'sale.order'

    @api.multi
    def order_process_now(self, send_invoice=True):
        """
        Confirms order and creates and validates invoice, confirms pickings.
        """
        for sale in self:
            # Process order 
            sale.action_confirm()
            inv_id = sale.action_invoice_create()
            if inv_id:
                inv = self.env['account.invoice'].browse(inv_id)
                inv.action_invoice_open()
                if send_invoice:
                    inv.action_force_invoice_send()
            for picking in sale.picking_ids:
                picking.force_assign()
                picking.action_done()


class AccountInvoice(models.Model):
    """Extend with force invoice send method."""

    _inherit = 'account.invoice'

    @api.multi
    def action_force_invoice_send(self):
        for inv in self:
            email_act = inv.action_invoice_sent()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=inv.company_id.email)
                inv.with_context(email_ctx).message_post_with_template(
                    email_ctx.get('default_template_id'))
        return True

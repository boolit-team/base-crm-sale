# -*- coding: utf-8 -*-

from odoo import models, api


class SaleOrder(models.Model):
    """Extend with fast confirmation."""

    _inherit = 'sale.order'

    @api.multi
    def order_process_now(self, send_invoice=True, skip_confirm=False):
        """Confirm order, pickings (if any) and invoice, send invoice mail."""
        for sale in self:
            # Process order
            if not skip_confirm:
                sale.action_confirm()
            if sale.state not in ('draft', 'sent', 'cancel'):
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
        """Send invoice via email with 0 input from user."""
        for inv in self:
            email_act = inv.action_invoice_sent()
            if email_act and email_act.get('context'):
                email_ctx = email_act['context']
                email_ctx.update(default_email_from=inv.company_id.email)
                inv.with_context(email_ctx).message_post_with_template(
                    email_ctx.get('default_template_id'))
        return True

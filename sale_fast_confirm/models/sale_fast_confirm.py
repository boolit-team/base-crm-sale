# -*- coding: utf-8 -*-

from odoo import models, api


class SaleOrder(models.Model):
    """Extend with fast confirmation."""

    _inherit = 'sale.order'

    @api.multi
    def order_process_now(self):
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
            for picking in sale.picking_ids:
                picking.force_assign()
                picking.action_done()


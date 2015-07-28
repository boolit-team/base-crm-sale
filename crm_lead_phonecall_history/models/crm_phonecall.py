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

from openerp import models, fields, api, _

class CRMPhoneCall(models.Model):
    _inherit = 'crm.phonecall'

    @api.model
    def create(self, values):
        rec = super(CRMPhoneCall, self).create(values)
        if rec.opportunity_id and rec.date and rec.state != 'done':
            # We need user tz datetime string, because it is directly output to user
            # and there is no way to change it later.
            dtime = fields.Datetime
            date = dtime.from_string(rec.date)
            date_tz = dtime.context_timestamp(rec, date)
            msg = _('Scheduled call <b>%s</b> at <b>%s</b>' % (rec.name, date_tz))
            rec.opportunity_id.message_post(body=msg)
        return rec


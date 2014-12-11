# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Andrius Laukavičius. Copyright JSC NOD Baltic
#    
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
from openerp.tools.translate import _
from openerp import SUPERUSER_ID  

EXT_DICT = {
    'notify_user.mt_lead_user': 'crm.lead',
    'notify_user.mt_helpdesk_user': 'crm.helpdesk',
}

class mail_message(models.Model):
    _inherit = 'mail.message'  

    def _notify(self, cr, uid, newid, context=None, force_send=False, user_signature=True):
            """ Add the related record followers to the destination partner_ids if is not a private message.
                Call mail_notification.notify to manage the email sending
            """
            notification_obj = self.pool.get('mail.notification')
            message = self.browse(cr, uid, newid, context=context)
            partners_to_notify = set([])

            # all followers of the mail.message document have to be added as partners and notified if a subtype is defined (otherwise: log message)
            if message.subtype_id and message.model and message.res_id:
                fol_obj = self.pool.get("mail.followers")
                # browse as SUPERUSER because rules could restrict the search results
                fol_ids = fol_obj.search(
                    cr, SUPERUSER_ID, [
                        ('res_model', '=', message.model),
                        ('res_id', '=', message.res_id),
                    ], context=context)
                partners_to_notify |= set(
                    fo.partner_id.id for fo in fol_obj.browse(cr, SUPERUSER_ID, fol_ids, context=context)
                    if message.subtype_id.id in [st.id for st in fo.subtype_ids]
                )
            # remove me from notified partners, unless the message is written on my own wall
            if message.subtype_id and message.author_id and message.model == "res.partner" and message.res_id == message.author_id.id:
                partners_to_notify |= set([message.author_id.id])
            elif message.author_id:
                partners_to_notify -= set([message.author_id.id])

            # all partner_ids of the mail.message have to be notified regardless of the above (even the author if explicitly added!)
            if message.partner_ids:
                partners_to_notify |= set([p.id for p in message.partner_ids])
            #Check 'Salesman Changed to Me' conditions
            msg_sub_ext_id = self.pool.get('mail.message.subtype').get_external_id(cr, uid, [message.subtype_id.id])
            if msg_sub_ext_id[message.subtype_id.id] == 'notify_user.mt_lead_user': 
                lead = self.pool.get('crm.lead').browse(cr, uid, message.res_id) 
                partners_to_notify &= set([lead.user_id.partner_id.id])
            if msg_sub_ext_id[message.subtype_id.id] == 'notify_user.mt_helpdesk_user': 
                helpdesk = self.pool.get('crm.helpdesk').browse(cr, uid, message.res_id) 
                partners_to_notify &= set([helpdesk.user_id.partner_id.id])
            if msg_sub_ext_id[message.subtype_id.id] == 'notify_user.mt_project_user': 
                project = self.pool.get('project.project').browse(cr, uid, message.res_id) 
                partners_to_notify &= set([project.user_id.partner_id.id]) 
            if msg_sub_ext_id[message.subtype_id.id] == 'project.mt_task_assigned': 
                task = self.pool.get('project.task').browse(cr, uid, message.res_id) 
                partners_to_notify &= set([task.user_id.partner_id.id])                           

            # notify
            notification_obj._notify(
                cr, uid, newid, partners_to_notify=list(partners_to_notify), context=context,
                force_send=force_send, user_signature=user_signature
            )
            message.refresh()

            # An error appear when a user receive a notification without notifying
            # the parent message -> add a read notification for the parent
            if message.parent_id:
                # all notified_partner_ids of the mail.message have to be notified for the parented messages
                partners_to_parent_notify = set(message.notified_partner_ids).difference(message.parent_id.notified_partner_ids)
                for partner in partners_to_parent_notify:
                    notification_obj.create(cr, uid, {
                            'message_id': message.parent_id.id,
                            'partner_id': partner.id,
                            'is_read': True,
                        }, context=context)

 
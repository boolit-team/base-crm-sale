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
from openerp.addons.crm.crm_lead import crm_lead as orig_crm_lead # Renaming to not clash with current class names
from openerp.addons.project.project import task as orig_task  

class crm_lead(models.Model):
    _inherit = 'crm.lead'
    
    _track = orig_crm_lead._track
    _track['user_id'] = {
        'notify_responsible.mt_lead_user': lambda self, cr, uid, obj, ctx=None: obj.user_id.id != uid,
    }

class crm_helpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    _track = {'user_id': {
            'notify_responsible.mt_helpdesk_user': lambda self, cr, uid, obj, ctx=None: obj.user_id.id != uid
        }
    }

    @api.multi
    def write(self, vals):
        for helpdesk in self:
            if vals.get('user_id'):
                user = self.env['res.users'].browse(vals['user_id']) 
                if user.partner_id not in helpdesk.message_follower_ids:
                    vals['message_follower_ids'] = [(4, user.partner_id.id)]
        return super(crm_helpdesk, self).write(vals)

class project(models.Model):
    _inherit = 'project.project'

    _track = {'user_id': {
            'notify_responsible.mt_project_user': lambda self, cr, uid, obj, ctx=None: obj.user_id.id != uid
        }
    }

class task(models.Model):
    _inherit = 'project.task'

    _track = orig_task._track
    _track['user_id'] = {
        'project.mt_task_assigned': lambda self, cr, uid, obj, ctx=None: obj.user_id.id != uid
    }   

class mail_notification(models.Model):
    _inherit = 'mail.notification'

    @api.model
    def _notify(self, message_id, partners_to_notify=None,
                force_send=False, user_signature=True):
        """ Send by email the notification depending on the user preferences

            :param list partners_to_notify: optional list of partner ids restricting
                the notifications to process
            :param bool force_send: if True, the generated mail.mail is
                immediately sent after being created, as if the scheduler
                was executed for this message only.
            :param bool user_signature: if True, the generated mail.mail body is
                the body of the related mail.message with the author's signature
        """
        if partners_to_notify:
            #message = self.env['mail.message'].search([('id', '=', message_id)], limit=1)
            message = self.env['mail.message'].browse(message_id)
            msg_sub_ids_pair = message.subtype_id.get_external_id()
            external_ids = ('notify_responsible.mt_lead_user', 'notify_responsible.mt_helpdesk_user', 'notify_responsible.mt_project_user', 
                'project.mt_task_assigned',)
            if msg_sub_ids_pair and msg_sub_ids_pair.get(message.subtype_id.id) in external_ids:
                obj = self.env[message.model].browse(message.res_id)
                if obj.user_id:
                    partners_to_notify = set(partners_to_notify)
                    partners_to_notify &= set([obj.user_id.partner_id.id])
                    partners_to_notify = list(partners_to_notify)
        return super(mail_notification, self)._notify(message_id=message_id, partners_to_notify=partners_to_notify, force_send=force_send, 
            user_signature=user_signature)         
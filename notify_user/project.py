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
from openerp import models
from openerp.addons.project.project import task as orig_task

class project(models.Model):
    _inherit = 'project.project'

    _track = {'user_id': {
            'notify_user.mt_project_user': lambda self, cr, uid, obj, ctx=None: obj.user_id.id != uid
        }
    }

class task(models.Model):
    _inherit = 'project.task'

    _track = orig_task._track
    _track['user_id'] = {
        'project.mt_task_assigned': lambda self, cr, uid, obj, ctx=None: obj.user_id.id != uid
    }

# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC NOD Baltic
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


{
    'name': 'CRM Stages Extension',
    'version': '1.0.1',
    'category': 'CRM',
    'summary': 'CRM Stages Management',
    'description': """
	Extends CRM stages allowing to track when stages changed, automatically generating report.
    Prevents users from jumping through unfinished stages. Calculates deadlines for stages. Changes
    user that is responsible in every stage if set in stages config.
	""",
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'depends': [
        'sales_team',
        'crm',        
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_team_view.xml',
        'views/crm_lead_view.xml',
        'views/crm_stage_activity_view.xml',
        'views/calendar_event_view.xml',
        'views/crm_phonecall_view.xml',
        'data/schedulers.xml',        

    ],
    'demo': [
    ],
    'test': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

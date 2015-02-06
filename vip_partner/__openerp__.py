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
    'name': 'VIP Partner',
    'version': '1.0',
    'category': 'Partner',
    'summary': 'VIP Partner',
    'description': """
	Adds VIP check for partner and automatically assigns such value
    if such partner is chosen in opportunity, project, task or helpdesk.
	""",
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'depends': [
        'crm_helpdesk',
        'project',      
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/project_view.xml',
        'views/crm_helpdesk_view.xml',
        'views/crm_lead_view.xml',
        #'data/,        

    ],
    'demo': [
    ],
    'test': [

    ],
    'installable': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

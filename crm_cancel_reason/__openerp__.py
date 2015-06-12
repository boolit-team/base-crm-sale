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
    'name': 'Opportunity Lost Reasons',
    'version': '1.12',
    'category': 'Reasons',
    'summary': 'Manage Opportunities Lost Reasons',
    'description': """
	Lets you define and choose lost reasons for Opportunities.
    Uses base_reason module as a base for reason management. 
    Lost reasons become visible when opportunity is lost.
	""",
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'depends': [
        'base_reason', 'crm',      
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        #'data/,        

    ],
    'demo': [
    ],
    'test': [

    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: NOD Baltic JSC
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
    'name': 'Filter Events By Today',
    'version': '1.1',
    'category': 'Filters',
    'description': """
Filter Events By Today
=============================================================

Adds filters such as 'By Today', 'Today', 'To Do', that filters records up to today or the ones that are not done. Filters will be added in opportunities, schedulled phonecalls
project tasks and projects.
    """,
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'images': [],
    'depends': ['crm', 'project'],
    'data': [ 
        'view/crm_phonecall_view.xml',
        'view/project_view.xml',
        'view/crm_lead_view.xml',       
    ],
    'css': [],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

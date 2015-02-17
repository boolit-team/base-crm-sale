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
    'name': 'Sale Fast Cancel',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Cancel Sale Order with one button',
    'description': """
	When cancelling sale order, if there are related invoices or delivery orders. It automatically cancels it too.
	""",
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'depends': [   
        'sale_stock',
        'account_cancel',
    ],
    'data': [
        #'security/ir.model.access.csv',
        #'views/sale_view.xml',
        #'data/',        

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

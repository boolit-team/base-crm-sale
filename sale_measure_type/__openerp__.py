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
    'name': 'Sale Measure Type',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Manage variable measures',
    'description': """
	Takes into account Measure Type field (that was only for information purposes) in product.
    If product measure type is set to 'variable', sale can be made using variable unit of measure.
    For example selling product that is a licence. It has quantity of 1, but it serves 10 users.
    Such product will have sum quantity.
	""",
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'depends': [  
        'sale'    
    ],
    'data': [
        #'security/ir.model.access.csv',
        'views/sale_view.xml',
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

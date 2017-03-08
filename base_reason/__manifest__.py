# -*- encoding: utf-8 -*-
# Author: Andrius Laukavičius. Copyright: JSC Boolit.
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Reasons Management',
    'version': '0.2.0',
    'category': 'Reasons',
    'summary': 'Reasons Management Tree',
    'description': """
Base module to manage reasons for various models for various things.
For example it can be used to manage opportunities cancel reasons.
	""",
    'author': 'Boolit',
    'website': 'www.boolit.eu',
    'depends': [
        'base'    
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/base_reason_security.xml',
        'views/reason_view.xml',
    ],
    'application': True,
}

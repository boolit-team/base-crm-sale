# -*- coding: utf-8 -*-

{
    'name': "smtp_per_user",
    'version': '0.2',
    'category': 'Mail',
    'description': """Using different smtp settings for user's outgoing emails""",
    'author': 'OERP',
    'license': 'AGPL-3',
    'website': "www.oerp.eu",
    "depends" : ['mail'],
    'data': [
        'smtp_per_user_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True
}

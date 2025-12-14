# -*- coding: utf-8 -*-
{
    'name': "Gestión de Clases",

    'summary': "Gestión de Profesores y Tipos de Cursos",

    'description': """
Permite la gestión de profesores, sus datos de contacto y la asignación a tipos de cursos (Básico, Medio, Superior).
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "views/profesor_views.xml",
        "views/menu.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


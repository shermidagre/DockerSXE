# -*- coding: utf-8 -*-
{
    'name': "modulo_medico_paciente",

    'summary': "Gestión de pacientes, médicos y diagnósticos",

    'description': """
        Módulo que permite gestionar:
        - Pacientes (nombre, apellidos, síntomas)
        - Médicos (nombre, apellidos, nº colegiado, consulta)
        - Relación muchos a muchos mediante diagnósticos
    """,

    'author': "Samuel Hermida Gregores",
    'website': "https://www.sequenolovasaleerporqueeresuntryhard.com",

    'category': 'Healthcare',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/paciente_views.xml',
        'views/medico_views.xml',
        'views/diagnostico_views.xml',
        'views/menu_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}


# -*- coding: utf-8 -*-
{

    'name': "Cafe_al_fallo",
    'summary': "Módulo para ver que alumno esta mas dormido 0",

    'description': """ 
    Un grupo de alumnos del Daniel Castelao, se están acostando tarde porque
    estudian mucho y pican mucho código en casa. En ocasiones, a la mañana
    siguiente en el centro, tienen sueño en clase, pero no tienen claro por qué opción
    decantarse de entre las maravillosas ofertas de los establecimientos que rodean el
    centro. Como tienen dudas de qué escoger, un compañero decide realizar un
    módulo sencillo que establece la bebida que deben tomar en función del nivel de
    sueño que tengan.
    Para evitar que tus compañeros se duerman en clase, debes desarrollar un módulo
    en Odoo que asigne la bebida adecuada según el sueño de cada usuario.""",

    'author': "Samuel Hermida Gregores",
    'website': "https://www.cafealfallo.org",


    'category': 'CafeLovers',
    'version': '0.1',
    
    
    'depends': ['base'],

    'data': [
        'security/ir.model.acces.csv',
        'views/views.xml',
        'views/templates.xml'
    ],

    'demo':[
        'demo/demol.xml'
    ],

    'installable': True,
    'auto_install': False,

}

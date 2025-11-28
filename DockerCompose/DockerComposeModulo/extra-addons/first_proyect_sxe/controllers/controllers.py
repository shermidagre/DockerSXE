# -*- coding: utf-8 -*-
from odoo import http


class FirstProyectSxe(http.Controller):
     @http.route('/first_proyect_sxe/first_proyect_sxe', auth='public')
     def index(self, **kw):
         return "Hello, world"

     @http.route('/first_proyect_sxe/first_proyect_sxe/objects', auth='public')
     def list(self, **kw):
         return http.request.render('first_proyect_sxe.listing', {
             'root': '/first_proyect_sxe/first_proyect_sxe',
             'objects': http.request.env['first_proyect_sxe.first_proyect_sxe'].search([]),
         })

     @http.route('/first_proyect_sxe/first_proyect_sxe/objects/<model("first_proyect_sxe.first_proyect_sxe"):obj>', auth='public')
     def object(self, obj, **kw):
         return http.request.render('first_proyect_sxe.object', {
             'object': obj
         })


# -*- coding: utf-8 -*-

from odoo import models, fields, api


class first_proyect_sxe(models.Model):
     _name = 'first_proyect_sxe.first_proyect_sxe'
     _description = 'first_proyect_sxe.first_proyect_sxe'

     name = fields.Char()
     value = fields.Integer()
     value2 = fields.Float(compute="_value_pc", store=True)
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
         for record in self:
             record.value2 = float(record.value) / 100


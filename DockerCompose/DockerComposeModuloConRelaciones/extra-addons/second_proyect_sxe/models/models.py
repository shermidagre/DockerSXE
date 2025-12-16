# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class second_proyect_sxe(models.Model):
    _inherit = 'res.partner'

    f_nac = fields.Date("Fecha de nacimiento")

    edad = fields.Integer(string="Edad", readonly=True, compute="_calcular_edad_china", store=True)
    signo_chino = fields.Char(string="Signo Chino", readonly=True, compute="_calcular_chinada", store=True)

    codigo_socio = fields.Char(string="Código de Socio")

    nivel_fidelidad = fields.Selection(
        [
            ('estandar', 'Estándar'),
            ('premium', 'Premium'),
            ('gold', 'Gold')
        ],
        string="Nivel de Fidelidad",
        compute="_compute_nivel_fidelidad",
        store=True,
        default='estandar'
    )

    @api.depends('f_nac')
    def _calcular_edad_china(self):
        for record in self:
            if record.f_nac:
                today = date.today()
                # Fórmula precisa para edad teniendo en cuenta si ya cumplió años o no
                age = today.year - record.f_nac.year - ((today.month, today.day) < (record.f_nac.month, record.f_nac.day))
                record.edad = age
            else:
                record.edad = 0

    @api.depends('f_nac')
    def _calcular_chinada(self):
        # Lista ordenada según el resto de dividir año / 12
        zodiacos = ['Mono', 'Gallo', 'Perro', 'Cerdo', 'Rata', 'Buey', 'Tigre', 'Conejo', 'Dragón', 'Serpiente', 'Caballo', 'Cabra']
        for record in self:
            if record.f_nac:
                indice = record.f_nac.year % 12
                record.signo_chino = zodiacos[indice]
            else:
                record.signo_chino = "Desconocido"

    @api.depends('codigo_socio')
    def _compute_nivel_fidelidad(self):
        for record in self:
            if not record.codigo_socio:
                record.nivel_fidelidad = 'estandar'
            elif record.codigo_socio.upper().startswith('G'):
                record.nivel_fidelidad = 'gold'
            else:
                record.nivel_fidelidad = 'premium'
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Profesor(models.Model):
    _name = "gestion_clases.profesor"
    _description = "Profesor"
    _order = "nombre asc" # Cambio de 'name' a 'nombre'

    nombre = fields.Char(string="Nombre", required=True)
    telefono = fields.Char(string="Teléfono", required=True)
    direccion = fields.Text(string="Dirección")

    cursos = fields.Selection(
        [
            ("basico_medio_superior", "Básico, Medio y Superior"),
            ("solo_superior", "Solo Superior"),
            ("medio_superior", "Medio y Superior"),
        ],
        string="Tipos de Cursos",
        required=True,
        default="basico_medio_superior",
    )

    horas_mensuales = fields.Integer(string="Horas Mensuales de Clase")

    # Campo calculado para Horas Anuales
    horas_anuales = fields.Integer(
        string="Horas Anuales de Clase",
        compute="_calcular_horas_anuales",
        store=True,
    )

    # Método para calcular las horas anuales
    @api.depends('horas_mensuales')
    def _calcular_horas_anuales(self):
        for record in self:
            # Multiplicamos por 10 asumiendo 10 meses de clase
            record.horas_anuales = record.horas_mensuales * 10
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class first_proyect_sxe(models.Model):
    # Mantenemos el nombre original del modelo para compatibilidad
    _name = 'first_proyect_sxe.first_proyect_sxe'
    _description = 'Nivel de Sueño y Bebida Recomendada'

    _rec_name = "alumno"

    # Campo original 'name' renombrado a 'alumno'
    alumno = fields.Char(string='Nombre del Alumno', required=True)

    # Campo 'value' reemplazado por 'nivel_sueno' (almacenado en DB)
    nivel_sueño = fields.Integer(
        string='Nivel de Sueño (1-10)',
        required=True,
        default=1,
        help="Indica qué tan dormido está el alumno, de 1 (poco) a 10 (máximo)."
    )

    # Campo 'value2' reemplazado por 'bebida_recomendada' (Calculado, NO almacenado)
    bebida_recomendada = fields.Char(
        string='Bebida Recomendada',
        compute='_compute_recommended_drink',
        store=False
    )

    # Nuevo campo para la marca de tiempo del registro
    fecha_registro = fields.Datetime(
        string='Fecha y Hora del Registro',
        required=True,
        default=fields.Datetime.now,
        help="Momento en que se registró el nivel de sueño."
    )

    # Mantenemos el campo 'description' por si se usaba, aunque no es requerido por la especificación.
    description = fields.Text(string='Notas')

    # Método computado para determinar la bebida (Calulo del sueño)
    @api.depends('nivel_sueño')
    def _compute_recommended_drink(self):
        for record in self:
            sueño = record.nivel_sueño

            if sueño >= 1 and sueño <= 3:
                record.bebida_recomendada = "Café con leche 🥛☕"
            elif sueño >= 4 and sueño <= 6:
                record.bebida_recomendada = "Café solo largo ☕"
            elif sueño >= 7 and sueño <= 9:
                record.bebida_recomendada = "Café solo larguísimo 😵‍💫"
            elif sueño == 10:
                record.bebida_recomendada = "💉 Inyección de adrenalina (¡Máximo Sueño!)"
            else:
                record.bebida_recomendada = "Nivel de sueño fuera del rango (1-10)"


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
    nivel_sueno = fields.Integer(
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

    # Mantenemos el campo 'description' por si se usaba, aunque no es requerido por la especificación.
    description = fields.Text(string='Notas')

    # Método computado para determinar la bebida
    @api.depends('nivel_sueno')
    def _compute_recommended_drink(self):
        for record in self:
            sueno = record.nivel_sueno

            if sueno >= 1 and sueno <= 3:
                record.bebida_recomendada = "Café con leche 🥛☕"
            elif sueno >= 4 and sueno <= 6:
                record.bebida_recomendada = "Café solo largo ☕"
            elif sueno >= 7 and sueno <= 9:
                record.bebida_recomendada = "Café solo larguísimo 😵‍💫"
            elif sueno == 10:
                record.bebida_recomendada = "💉 Inyección de adrenalina (¡Máximo Sueño!)"
            else:
                record.bebida_recomendada = "Nivel de sueño fuera del rango (1-10)"

    # Eliminamos el método _value_pc ya que no es necesario.
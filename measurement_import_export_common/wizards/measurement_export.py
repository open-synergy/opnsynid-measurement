# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
# pylint: disable=W0622
import base64
from datetime import datetime

from openerp import api, fields, models
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class MeasurementExport(models.TransientModel):
    _name = "measurement.export"
    _description = "Measurement Export Common Feature"

    name = fields.Char(string="File Name", readonly=True)

    data = fields.Binary(string="File", readonly=True)

    state = fields.Selection(
        string="State",
        selection=[("draft", "draft"), ("success", "success"), ("failed", "failed")],
        default="draft",
    )

    @api.multi
    def _prepare_column(self):
        self.ensure_one()
        return [
            "name",
            "object",
            "item_code",
            "item_name",
            "value",
        ]

    @api.multi
    def _prepare_data_to_export(self, measurement, item):
        self.ensure_one()
        result = []
        result.append(measurement.name)
        if measurement.object_id.name:
            result.append(measurement.object_id.name)
        else:
            result.append("-")
        if item.item_type_id.code:
            result.append(item.item_type_id.code)
        else:
            result.append("-")
        if item.item_type_id.name:
            result.append(item.item_type_id.name)
        else:
            result.append("-")
        result.append("0")
        return result

    @api.multi
    def _export(self):
        active_model = self.env.context.get("active_model", False)
        active_ids = self.env.context.get("active_ids", False)
        obj_measurement = self.env[active_model]
        measurement_ids = obj_measurement.browse(active_ids)

        columns = self._prepare_column()
        csv = ",".join(columns)
        csv += "\n"
        for measurement in measurement_ids:
            for item in measurement.item_ids:
                data = self._prepare_data_to_export(measurement, item)
                csv_row = '","'.join(data)
                csv += '"{}"\n'.format(csv_row)
        return csv

    @api.multi
    def button_export(self):
        self.ensure_one()
        data = self._export()
        if data:
            date_now = fields.Datetime.now()
            convert_dt = datetime.strptime(date_now, DEFAULT_SERVER_DATETIME_FORMAT)
            format = convert_dt.strftime("%d-%m-%Y_%H:%M:%S")
            vals = {
                "state": "success",
                "data": base64.b64encode(data.encode("utf8")),
                "name": "__export__." + str(format) + ".csv",
            }
        else:
            vals = {
                "state": "failed",
            }
        self.write(vals)

        return {
            "type": "ir.actions.act_window",
            "res_model": str(self._model),
            "view_mode": "form",
            "view_type": "form",
            "res_id": self.id,
            "views": [(False, "form")],
            "target": "new",
        }

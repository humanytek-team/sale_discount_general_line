# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class Sale_order_discount(models.Model):
    _inherit = 'sale.order'

    @api.multi
    @api.onchange('line_discount_rate')
    def onchange_line_discount_rate(self):
        self.line_discount_rate = abs(self.line_discount_rate)
        for line in self.order_line:
            line.price_unit = line.product_id.list_price - (line.product_id.list_price * self.line_discount_rate / 100)

    line_discount_rate = fields.Float('Discount',
                                    digits=dp.get_precision('Product Price 2'))

    @api.model
    def _prepare_invoice(self):
        res = super(Sale_order_discount, self)._prepare_invoice()
        res['line_discount_rate'] = self.line_discount_rate
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    @api.depends('price_unit')
    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()
        self.price_unit = self._get_display_price(self.product_id) - (self._get_display_price(self.product_id) * self.order_id.line_discount_rate / 100)
        return result

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        result = super(SaleOrderLine, self).product_uom_change()
        self.price_unit = self._get_display_price(self.product_id) - (self._get_display_price(self.product_id) * self.order_id.line_discount_rate / 100)
        return result

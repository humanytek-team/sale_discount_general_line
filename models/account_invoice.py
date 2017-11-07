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

from odoo import fields, models, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    line_discount_rate = fields.Float('Discount',
                                    digits=dp.get_precision('Product Price 2'))

    @api.multi
    @api.onchange('line_discount_rate')
    def onchange_line_discount_rate(self):
        self.line_discount_rate = abs(self.line_discount_rate)
        for line in self.invoice_line_ids:
            line.price_unit = line.product_id.list_price - (line.product_id.list_price * self.line_discount_rate / 100)

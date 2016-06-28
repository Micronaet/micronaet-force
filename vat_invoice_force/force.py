# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
import os
import sys
import logging
import openerp
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)


_logger = logging.getLogger(__name__)


class AccountInvoice(orm.Model):
    """ Model name: AccountInvoice
    """
    
    _inherit = 'account.invoice'
    
    # -------------
    # Button event:
    # -------------
    def force_invoice_tax(self, cr, uid, ids, context=None):
        ''' Force vat on all lines
        '''
        assert len(ids) == 1, 'Button only for one record a time!'

        # Pool used:
        partner_pool = self.pool.get('res.partner')
        line_pool = self.pool.get('account.invoice.line')
        
        invoice_proxy = self.browse(cr, uid, ids, context=context)[0]
        
        # Get 2 discount used onchange procedure from partner:
        vat = invoice_proxy.force_tax_id.id
        if not vat:
            raise osv.except_osv(
                _('Error'), 
                _('Set VAT tax before force!'))
            
        line_ids = [line.id for line in invoice_proxy.invoice_line]
        line_pool.write(cr, uid, line_ids, {
            'invoice_line_tax_id': [(6, 0, (vat, ))],
            }, context=context)
            
        # reset discount header value:    
        return self.write(cr, uid, ids, {
            'force_tax_id': False,
            }, context=context)    
    
    _columns = {
        'force_tax_id': fields.many2one(
            'account.tax', 'Force Tax'),
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

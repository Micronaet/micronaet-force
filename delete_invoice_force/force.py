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
    def force_invoice_deletion(self, cr, uid, ids, context=None):
        ''' Force discount on all lines
        '''
        assert len(ids) == 1, 'Button only for one record a time!'        
        invoice_id = ids[0]
        current_proxy = self.browse(cr, uid, invoice_id, context=context)
        
        log_file = open(
            os.path.join(
                os.path.expanduser('~'),
                'delete_invoice.log',
                ), 'a')
        
        log_file.write('%s) Remove invoice: %s - %s (%s) [user: %s]\n' % (
            datetime.now(), 
            current_proxy.number, 
            current_proxy.internal_number,
            current_proxy.date_invoice,
            uid,
            ))
            
        # ---------------------------------------------------------------------
        # Delete invoice line:
        # ---------------------------------------------------------------------
        query = '''DELETE FROM account_invoice_line WHERE invoice_id=%s;
            ''' % invoice_id
        cr.execute(query)
        _logger.warning('Remove invoice line: %s' % query)
        log_file.write('%s Query: %s' % (datetime.now(), query))
            
        # ---------------------------------------------------------------------
        # Delete invoice tax:
        # ---------------------------------------------------------------------
        query = '''DELETE FROM account_invoice_tax WHERE invoice_id=%s;
            ''' % invoice_id
        cr.execute(query)
        _logger.warning('Remove invoice tax: %s' % query)
        log_file.write('%s Query: %s' % (datetime.now(), query))

        # ---------------------------------------------------------------------
        # Delete invoice statistic:
        # ---------------------------------------------------------------------
        #query = '''
        #    DELETE FROM statistic_invoice_deadline WHERE invoice_id=%s;
        #    ''' % invoice_id
        #cr.execute(query)
        #_logger.warning('Remove invoice stats: %s' % query)
        #log_file.write('%s Query: %s' % (datetime.now(), query))
        
        # ---------------------------------------------------------------------
        # Update invoice status in stock_move:
        # ---------------------------------------------------------------------
        query = '''UPDATE stock_move SET invoice_state = '2binvoiced' 
            WHERE picking_id IN (
                SELECT id FROM stock_picking 
                WHERE invoice_id=%s);
            ''' % invoice_id
        cr.execute(query)
        _logger.warning('Unlink stock move: %s' % query)
        log_file.write('%s Query: %s' % (datetime.now(), query))

        # ---------------------------------------------------------------------
        # Update DDT (if present)
        # ---------------------------------------------------------------------
        # Disconnect from invoice:    
        query = '''UPDATE stock_ddt SET
                invoice_id=null
                WHERE invoice_id=%s;
            ''' % invoice_id
        cr.execute(query)
        _logger.warning('Unlink DDT: %s' % query)
        log_file.write('%s Query: %s' % (datetime.now(), query))
        
        # ---------------------------------------------------------------------
        # Update picking
        # ---------------------------------------------------------------------
        # Search before change:
        picking_ids = self.pool.get('stock.picking').search(cr, uid, [
            ('invoice_id', '=', invoice_id),
            ], context=context)
        
        # Disconnect from invoice:    
        query = '''UPDATE stock_picking SET
                state='assigned', invoice_state='2binvoiced', invoice_id=null
                WHERE invoice_id=%s;
                
                
            ''' % invoice_id            
        cr.execute(query)
        _logger.warning('Unlink stock picking: %s' % query)
        log_file.write('%s Query: %s' % (datetime.now(), query))
        
        # purchase_invoice_rel  sale_order_invoice_rel
        return {
            'type': 'ir.actions.act_window',
            'name': _('Picking scollegati'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            #'res_id': 1,
            'res_model': 'stock.picking',
            'view_id': False,
            'views': [(False, 'tree'), (False, 'form')],
            'domain': [('id', 'in', picking_ids)],
            'context': context,
            'target': 'current', # 'new'
            'nodestroy': False,
            }
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

"""Client call classes.

These classes implement any response cleaning and validation needed.  If a
call class isn't defined for a given method then one is created using
ubersmith.calls.BaseCall.

"""

from ubersmith.calls import BaseCall, GroupCall
from ubersmith.utils import prepend_base

__all__ = [
    'GetCall',
    'ListCall',
]

_ = prepend_base(__name__.split('.')[-1])


class _ClientCallMixin(object):
    bool_fields = ['active']
    int_fields = [
        'clientid',
        'class_id',
        'priority',
    ]
    decimal_fields = [
        'balance',
        'commission',
        'commission_rate',
        'discount',
        'inv_balance',
        'tier_commission',
        'tier_commission_rate',
    ]
    timestamp_fields = [
        'created',
        'latest_inv',
        'password_changed',
    ]
    php_serialized_fields = ['access']


class GetCall(_ClientCallMixin, BaseCall):
    method = _('get')
    required_fields = [('client_id', 'user_login', 'email')]


class ListCall(_ClientCallMixin, GroupCall):
    method = _('list')


class InvoiceCountCall(BaseCall):
    method = _('invoice_count')
    required_fields = ['client_id']

    def clean(self):
        super(InvoiceCountCall, self).clean()
        self.cleaned = int(self.cleaned)


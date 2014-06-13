import datetime
from decimal import Decimal
import time

import phpserialize


_CLEANERS = {}


def cleaner(func):
    _CLEANERS[func.__name__] = func
    return func


@cleaner
def php(val):
    return phpserialize.loads(val.encode("utf-8"))


@cleaner
def timestamp(val):
    return datetime.datetime.fromtimestamp(float(val))


@cleaner
def date(val):
    return datetime.date(*time.strptime(val, '%b/%d/%Y')[:3])


@cleaner
def decimal(val):
    return Decimal(val.replace(',', ''))


@cleaner
def int(val):
    return __builtins__['int'](val.replace(',', ''))


class clean(object):
    def __init__(self, cleaner, keys=None, values=None, raises=False):
        self.cleaner = cleaner if callable(cleaner) else _CLEANERS[cleaner]
        self.keys = keys
        self.values = values
        self.raises = raises

    def __call__(self, val):
        val = self.cleaner(val)
        if self.cleaner is list:
            val = self._clean_list(val)
        elif self.cleaner is dict:
            val = self._clean_dict(val)
        return val

    def _clean_list(self, val):
        # TODO: factor keys/values cleaning out to methods
        # clean values
        if self.values is not None:
            if callable(self.values):
                # apply cleaner to all elements
                cleaner = self.values
                for i, element in enumerate(val):
                    val[i] = cleaner(element)
            else:
                # apply cleaners to specific values
                for i, cleaner in self.values.items():
                    try:
                        val[i] = cleaner(val[i])
                    except IndexError as e:
                        if self.raises:
                            raise e
        return val

    def _clean_dict(self, val):
        # TODO: factor keys/values cleaning out to methods
        # clean keys
        if self.keys is not None:
            tmp = {}
            if callable(self.keys):
                # apply cleaner to all keys
                cleaner = self.keys
                for k, v in val.items():
                    tmp[cleaner(k)] = v
            else:
                # apply cleaners to specific keys
                for k, v in val.items():
                    cleaner = self.keys.get(k, lambda x: x)
                    tmp[cleaner(k)] = val[k]
            val = tmp

        # TODO: factor keys/values cleaning out to methods
        # clean values
        if self.values is not None:
            if callable(self.values):
                # apply cleaner to all elements
                cleaner = self.values
                for k, v in val.items():
                    val[k] = cleaner(val[k])
            else:
                # apply cleaners to specific values
                for k, cleaner in self.values.items():
                    val[k] = cleaner(val[k])
        return val

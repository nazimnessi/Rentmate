from django.db.models.expressions import F
from django_filters import FilterSet


class OrderedFilterSet(FilterSet):
    @property
    def qs(self):
        q = super().qs
        _order = q.query.order_by
        fs = []
        for o in _order:
            f = F(o)
            if o.startswith("-"):
                f = F(o[1:]).desc(nulls_last=True)
            fs.append(f)
        q = q.order_by(*fs)
        return q

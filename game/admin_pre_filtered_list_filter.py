from typing import List, Tuple, Any

from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.options import IncorrectLookupParameters
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class PreFilteredListFilter(SimpleListFilter):
    """Taken from https://stackoverflow.com/a/62292513/7119080"""

    # Either set this or override .get_default_value()
    default_value = None

    no_filter_value = "all"
    no_filter_name = _("All")

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = None

    # Parameter for the filter that will be used in the URL query.
    parameter_name = None

    def get_default_value(self):
        if self.default_value is not None:
            return self.default_value
        raise NotImplementedError(
            "Either the .default_value attribute needs to be set or "
            "the .get_default_value() method must be overridden to "
            "return a URL query argument for parameter_name."
        )

    def get_lookups(self) -> List[Tuple[Any, str]]:
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        raise NotImplementedError(
            "The .get_lookups() method must be overridden to "
            "return a list of tuples (value, verbose value)."
        )

    # Overriding parent class:
    def lookups(self, request, model_admin) -> List[Tuple[Any, str]]:
        return [
            (self.no_filter_value, self.no_filter_name)
        ] + self.get_lookups()

    # Overriding parent class:
    def queryset(self, request, queryset: QuerySet) -> QuerySet:
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() is None:
            return self.get_default_queryset(queryset)
        if self.value() == self.no_filter_value:
            return queryset.all()
        return self.get_filtered_queryset(queryset)

    def get_default_queryset(self, queryset: QuerySet) -> QuerySet:
        return queryset.filter(
            **{self.parameter_name: self.get_default_value()}
        )

    def get_filtered_queryset(self, queryset: QuerySet) -> QuerySet:
        try:
            return queryset.filter(**self.used_parameters)
        except (ValueError, ValidationError) as e:
            # Fields may raise a ValueError or ValidationError when converting
            # the parameters to the correct type.
            raise IncorrectLookupParameters(e)

    # Overriding parent class:
    def choices(self, changelist: ChangeList):
        """
        Overridden to prevent the default "All".
        """
        value = self.value() or force_str(self.get_default_value())
        for lookup, title in self.lookup_choices:
            yield {
                "selected": value == force_str(lookup),
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}
                ),
                "display": title,
            }

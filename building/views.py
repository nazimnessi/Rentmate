from building.utils import data_export
from rest_framework import viewsets
from .models import Building
from django.db.models import Count, Q, Value
from django.db.models.functions import Concat


class PropertyAPI(viewsets.ModelViewSet):

    def get_queryset(self):
        search_query = self.request.query_params.get("name", "")
        sort_by = self.request.query_params.get("orderBy", "-id")
        projects_query = Building.objects.filter(name__icontains=search_query)
        projects_query = projects_query.annotate()
        if 'address' in sort_by:
            return projects_query.order_by(
                f'{sort_by}__address1',
                f'{sort_by}__address2',
                f'{sort_by}__city',
                f'{sort_by}__state',
                f'{sort_by}__postal_code',
            )
        elif 'total_renter' in sort_by:
            return projects_query.annotate(total_renter=Count('rooms__renter')).order_by(sort_by)
        elif 'total_rooms' in sort_by:
            return projects_query.annotate(total_rooms=Count('rooms__id')).order_by(sort_by)
        return projects_query.order_by(sort_by)

    def annotate_full_address(self, queryset):
        return queryset.annotate(full_address=Concat('address__address1', Value(', '), 'address__address2', Value(', '), 'address__city', Value(', '), 'address__state', Value(' '), 'address__postal_code'))

    def annotate_total_renters(self, queryset):
        return queryset.annotate(total_renters=Count('rooms', filter=Q(rooms__renter__isnull=False)))

    def annotate_total_rooms(self, queryset):
        return queryset.annotate(total_rooms=Count('rooms'))

    # @authentication_classes([TokenAuthentication])
    # @permission_classes([IsAuthenticated])
    # @login_required
    def download(self, request):
        properties = self.get_queryset()
        properties_with_full_address = self.annotate_full_address(properties)
        properties_with_renters = self.annotate_total_renters(properties_with_full_address)
        properties_with_renters_and_rooms = self.annotate_total_rooms(properties_with_renters)
        column_name = [
            "Property Name",
            "Property Number",
            "Property Type",
            "Address",
            "Total Renters",
            "Total Rooms",
            # "Amount/Property"
        ]
        column_values = {
            "Property Name": "name",
            "Property Number": "house_number",
            "Property Type": "building_type",
            "Address": "full_address",
            "Total Renters": "total_renters",
            "Total Rooms": "total_rooms",
            # "Amount/Property": "amount/property"
        }

        return data_export(properties_with_renters_and_rooms, column_name, column_values, "Properties_List.csv")

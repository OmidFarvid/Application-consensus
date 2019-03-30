from django.contrib import admin

from reversion.admin import VersionAdmin
from apps.school.models import School, Application, Review, Season, Staff


class SchoolInstanceAdmin(VersionAdmin):
    list_display = ('full_name', 'phone_number', 'address', 'country', 'country', 'state', 'city', 'zip_code')
    list_filter = ('full_name', 'phone_number', 'address', 'country', 'country', 'state', 'city', 'zip_code')


admin.site.register(School, SchoolInstanceAdmin)
admin.site.register(Application, VersionAdmin)
admin.site.register(Review, VersionAdmin)
admin.site.register(Season, VersionAdmin)
admin.site.register(Staff, VersionAdmin)

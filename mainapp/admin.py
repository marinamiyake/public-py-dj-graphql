from django.contrib import admin

from mainapp import models


class MomentModelAdmin(admin.ModelAdmin):
    disp_fields = [
        "id",
        "title",
        "city_name",
        "weather_description",
        "temp",
        "temp_min",
        "temp_max",
        "humidity",
        "comment",
        "created_at",
    ]
    save_on_top = True
    save_as = True
    list_display = disp_fields
    date_hierarchy = "created_at"
    search_fields = ('id', 'title')
    sortable_by = disp_fields
    readonly_fields = [
        'created_at',
    ]


admin.site.register(models.Moment, MomentModelAdmin)

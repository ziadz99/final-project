from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from main.models import Contact, Costumer


class ContactResource(resources.ModelResource):
    class Meta:
        model = Contact


@admin.register(Contact)
class PlaceAdmin(ImportExportModelAdmin):
    resource_class = ContactResource


class CostumerResource(resources.ModelResource):
    class Meta:
        model = Costumer


@admin.register(Costumer)
class CostumerAdmin(ImportExportModelAdmin):
    resource_class = CostumerResource

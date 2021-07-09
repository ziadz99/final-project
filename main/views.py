from django.shortcuts import render
import requests

# Create your views here.
from django.views.generic import ListView

from main.models import Contact, Costumer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def ip_to_location(request):
    url = f'http://ip-api.com/json/{get_client_ip(request)}'
    print(url)
    try:
        data = requests.get(url)
        return data.json()
    except:
        return


def ContactsIndexView(request, *args, **kwargs):
    objects = Contact.objects.all()
    location = ip_to_location(request)
    return render(request, "contacts.index.html",
                  {"object_list": objects,
                   "ModalFields": [f.name for f in Contact._meta.get_fields()]
                   })


def CostumersIndexView(request, *args, **kwargs):
    objects = Costumer.objects.all()
    return render(request, "costumers.index.html",
                  {"object_list": objects,
                   "ModalFields": [f.name for f in Costumer._meta.get_fields()]
                   })


def MappingView(request, *args, **kwargs):
    objects = Contact.objects.all()
    costumers_objects = Costumer.objects.all()
    location = ip_to_location(request)
    lnk_coords = None
    try:
        lnk_lat = request.GET.get('lnk_lat')
        lnk_lon = request.GET.get('lnk_lon')
        lnk_coords = [lnk_lat, lnk_lon]
    except:
        pass
    return render(request, "mapping.html",
                  {"object_list": objects,
                   "costumers_list": costumers_objects,
                   "user_lat": location.get('lat', "false"),
                   "user_lon": location.get('lon', "false"),
                   "ModalFields": [f.name for f in Contact._meta.get_fields()],
                   "costumers_modal_fields": [f.name for f in Costumer._meta.get_fields()],
                   "lnk_lat": lnk_coords[0],
                   "lnk_lon": lnk_coords[1],
                   })

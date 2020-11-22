import random

from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render
from django.views import View

from tours.data import tours, departures, title, subtitle, description


class MainView(View):

    def get(self, request):
        id_tour = random.sample(range(1, (len(tours) + 1)), k=6)
        select_tours = {}
        for i in id_tour:
            select_tours[i] = tours[i]
        context = {
            'title': title,
            'subtitle': subtitle,
            'description': description,
            'select_tours': select_tours
        }
        return render(request, 'index.html', context=context)


class DepartureView(View):

    def get(self, request, departure):
        select_departure = {}
        list_id = []
        list_amount_nights = []
        list_prices = []
        for tour_id, tour in tours.items():
            if tour["departure"] == departure:
                select_departure[tour_id] = tour
                list_id.append(tour_id)
                list_prices.append(tours[tour_id]["price"])
                list_amount_nights.append(tours[tour_id]['nights'])
        if departure not in departures.keys():
            raise Http404
        min_price = min(list_prices)
        max_price = max(list_prices)
        min_nights = min(list_amount_nights)
        max_nights = max(list_amount_nights)
        context = {
            'select_departure': select_departure,
            'departure': departures[departure],
            'amount_tours': len(list_id),
            'min_price': min_price,
            'max_price': max_price,
            'min_nights': min_nights,
            'max_nights': max_nights,
            'title': title
        }
        return render(request, 'departure.html', context=context)


class TourView(View):
    def get(self, request, id):
        departure = departures.get(tours[id]['departure'])
        context = {
            'tour': tours[id],
            'departure': departure,
            'title': title
        }
        if id not in tours.keys():
            raise Http404
        return render(request, "tour.html", context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Что-то сломалось :(')
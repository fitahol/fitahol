# coding=utf-8
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from gym.models import Gymnasium, Province, City, District
from gym.serializers import GymnasiumSerializer, ProvinceSerializer, \
    CitySerializer, DistrictSerializer, GymnasiumCreateSerializer


class ProvinceListView(ListAPIView):
    queryset = Province.objects.filter(pcode="CN")
    serializer_class = ProvinceSerializer
    pagination_class = None


class CityListView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None

    def get_queryset(self):
        pcode = self.kwargs["pcode"]
        queryset = City.objects.filter(pcode=pcode)
        return queryset


class DistrictListView(ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = None

    def get_queryset(self):
        pcode = self.kwargs["pcode"]
        queryset = District.objects.filter(pcode=pcode)
        return queryset


class GymnasiumViewSet(viewsets.ModelViewSet):
    queryset = Gymnasium.objects.all()
    serializer_class = GymnasiumSerializer
    pagination_class = None
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return GymnasiumSerializer
        return GymnasiumCreateSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        if name:
            return Gymnasium.objects.filter(name__contains=name)
        district = self.request.query_params.get("district_code")
        if district:
            return Gymnasium.objects.filter(district_code=district)
        city = self.request.query_params.get("city_code")
        if city:
            return Gymnasium.objects.filter(city_code=city)
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)


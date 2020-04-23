from django.shortcuts import render
# request an api & get json back
# Create your views here.
from django.shortcuts import render  # efacult

from django.http import HttpResponse
from django.shortcuts import get_object_or_404  # object doesnt exist... return 404
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView  # normal vieww can return apiview
from rest_framework.response import Response  # 401 not found.. 501 send error
from rest_framework import status
from downloadcsv.models import YearlyResult

from .permission import IsOwnerOrReadOnly
from .serializers import YearlyResultSerializer
from django.contrib.auth.models import User


class NodeConsumptionsAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get(self, request, node_id, year, month):
        yearly_results = YearlyResult.objects.filter(  # Django filter which is = WHERE clause.
            date__year=year,
            date__month=month,  # SQL equivalent of WHERE EXTRACT(year from reading_date) = year
            node_id=node_id
        )
        print(f"Count of results is: {yearly_results.count()}.")
        # select * from yearly_reults where node_id=65 and extract(year from reading_date) = '2007';
        # 44,00,000
        serializer = YearlyResultSerializer(yearly_results, many=True)
        return Response(serializer.data)

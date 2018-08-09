
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from rest_framework.response import Response


class AuthView(ViewSetMixin,APIView):

    def login(self,request,*args,**kwargs):
        print('用户发来POST请求了',request)
        return Response({'code':11111})




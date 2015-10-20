import json
from django import http
from django.views.generic.base import View
from django.shortcuts import render

# Create your views here.

class JsonPostView(View):

    http_method_names = ['post']

    def post(self, request):

        print request.body
        data = json.loads(request.body)

        print "hello"

        return http.HttpResponse(
            json.dumps(data),
            content_type='application/json'
        )



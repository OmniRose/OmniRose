import json
from datetime import datetime
import pytz

from django import http
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .models import SunSwing


class JsonPostView(View):

    http_method_names = ['post']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(JsonPostView, self).dispatch(*args, **kwargs)

    def post(self, request):

        data = json.loads(request.body)

        swing = SunSwing.objects.create(
            user=request.user,
            vessel="FIXME",
            note="FIXME",
            video_start_time=datetime.fromtimestamp(data["compass_video_start_time"], pytz.utc),
            latitude=data["latitude"],
            longitude=data["longitude"],
            pelorus_correction=data["pelorus_correction"],
        )

        for reading in data['readings']:
            swing.reading_set.create(
                video_time=reading["time"],
                compass_reading=reading["compass"],
                shadow_reading=reading["shadow"],
            )

        return http.HttpResponse(
            json.dumps({"pk": swing.id}),
            content_type='application/json'
        )



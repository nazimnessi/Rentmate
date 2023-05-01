from __future__ import absolute_import, unicode_literals

from rentmate.celery import app

from .models import Request


@app.task
def reject_requests(request_data=None):
    Request.objects.filter(room=request_data.get("room_id")).update(action="R")

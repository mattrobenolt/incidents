"""
{
    "user": {
        "id": "1",
        "name": "Shell",
        "room": "Shell"
    },
    "text": "fdsa",
    "id": "messageId",
    "done": false,
    "room": "Shell"
}
"""
from incidents.plugins import HttpIngestPlugin
from django.http import HttpResponse

import json


class HubotPlugin(HttpIngestPlugin):
    "Plugin to ingest Hubot messages"

    template_name = 'plugins/hubot.jinja'

    def post(self, request, project):
        data = request.body
        payload = json.loads(data)
        text = payload['text']
        name = payload['user']['name']
        actor = self.get_actor(project, name)
        self.create_event(
            actor=actor,
            project=project,
            level=self.default_level,
            message=text,
            data=data,
        )
        return HttpResponse(status=201)

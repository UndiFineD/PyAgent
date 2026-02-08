# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_volweb.py\volweb.py\consumers_d4d43c036671.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-VolWeb\VolWeb\consumers.py

import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class VolatilityTaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.dump_id = self.scope["url_route"]["kwargs"]["dump_id"]

        self.room_group_name = f"volatility_tasks_{self.dump_id}"

        # Join room group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        # Send message to room group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "message": message,
            },
        )

    # Receive message from room group

    async def send_notification(self, event):

        message = event["message"]

        # Send message to WebSocket

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )


class CasesTaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.room_group_name = "cases"

        # Join room group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        status = text_data_json["status"]

        # Send message to room group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "status": status,
                "message": message,
            },
        )

    # Receive message from room group

    async def send_notification(self, event):

        message = event["message"]

        status = event["status"]

        # Send message to WebSocket

        await self.send(
            text_data=json.dumps(
                {
                    "status": status,
                    "message": message,
                }
            )
        )


class EvidencesTaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.room_group_name = "evidences"

        # Join room group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        status = text_data_json["status"]

        # Send message to room group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "status": status,
                "message": message,
            },
        )

    # Receive message from room group

    async def send_notification(self, event):

        message = event["message"]

        status = event["status"]

        # Send message to WebSocket

        await self.send(
            text_data=json.dumps(
                {
                    "status": status,
                    "message": message,
                }
            )
        )


class SymbolsTaskConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):

        self.room_group_name = "symbols"

        # Join room group

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group

        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)

        message = text_data_json["message"]

        status = text_data_json["status"]

        # Send message to room group

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_notification",
                "status": status,
                "message": message,
            },
        )

    # Receive message from room group

    async def send_notification(self, event):

        message = event["message"]

        status = event["status"]

        # Send message to WebSocket

        await self.send(
            text_data=json.dumps(
                {
                    "status": status,
                    "message": message,
                }
            )
        )

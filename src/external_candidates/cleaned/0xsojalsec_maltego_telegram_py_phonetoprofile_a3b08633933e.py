# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_maltego_telegram.py\transforms.py\phonetoprofile_a3b08633933e.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-maltego-telegram\transforms\PhoneToProfile.py

import logging

from extensions import registry

from maltego_trx.maltego import MaltegoMsg, MaltegoTransform

from maltego_trx.transform import DiscoverableTransform

from pyrogram.types import InputPhoneContact

from settings import app, bot_token, loop

from utils import fetch_web_info, process_profile_entity


async def fetch_profile_by_phone(phone: str):
    async with app:
        contacts = await app.import_contacts([InputPhoneContact(phone, "Foo")])

        if contacts.users:
            await app.delete_contacts(contacts.users[0].id)

            return await app.get_users(contacts.users[0].id)

    return


@registry.register_transform(
    display_name="To Telegram Profile",
    input_entity="maltego.PhoneNumber",
    description="Finds a user's Telegram profile by phone number",
    output_entities=["interlinked.telegram.UserProfile"],
)
class PhoneToProfile(DiscoverableTransform):
    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        phone = request.getProperty("phonenumber")

        profile = loop.run_until_complete(fetch_profile_by_phone(phone))

        if profile:
            entity = process_profile_entity(profile)

            entity.addProperty("properties.phone", value=phone)

            entity.setLinkThickness(2)

            response.entities.append(entity)

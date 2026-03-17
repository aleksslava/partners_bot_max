import logging
from maxapi import Router, F, Bot
from maxapi.enums.attachment import AttachmentType
from maxapi.filters.command import Command
from maxapi.types import BotStarted, MessageCreated, CallbackButton, MessageCallback, RequestContactButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder

from amo_api.amo_api import AmoCRMWrapper, Contact
from lexicon.lexicon_ru import account_info, Lexicon_RU, start_menu, helpfull_materials_menu
from keyboards.main_keyboards import get_start_keyboard, get_contacts_list, problem_button, authorized_client, \
    hide_contacts_list, get_start_button, forum_button, helpfull_materials_keyboard, back_button, manager_button, \
    support_button
from utils.utils import extract_phone_from_vcf

logger = logging.getLogger(__name__)

main_router = Router()


@main_router.bot_started()
async def bot_start(event: BotStarted):
    await event.bot.send_message(
        chat_id=event.chat_id,
        text='<b>Основное меню чат-бота HiTE PRO!</b>',
        attachments=[
            await get_start_keyboard(start_menu),
        ]
    )


@main_router.message_created(Command('start'))
async def start(event: MessageCreated):
    max_id = event.message.sender.user_id
    await event.message.answer(
        text='<b>Основное меню чат-бота HiTE PRO!</b>',
        attachments=[
            await get_start_keyboard(start_menu),
        ]
    )

@main_router.message_callback(F.callback.payload == '/start',)
async def start_callback(event: MessageCreated):
    max_id = event.callback.user.user_id
    await event.message.edit(
        text='<b>Основное меню чат-бота HiTE PRO!</b>',
        attachments=[
            await get_start_keyboard(start_menu),
        ]
    )


@main_router.message_callback(F.callback.payload == '/info',)
async def info(event: MessageCreated, amo_api: AmoCRMWrapper, fields_id: dict):
    max_id = event.callback.user.user_id
    logger.info(max_id)
    customer = amo_api.get_customer_by_max_id(max_id)  #Переделать на max_id
    if customer.get('status_code'):
        if customer.get('max_id_in_db'):
            customer = customer.get('response')
            responsible_manager = amo_api.get_responsible_user_by_id(int(customer.get('responsible_user_id')))
            customer['manager'] = responsible_manager
            customer_params = amo_api.get_customer_params(customer, fields_id=fields_id)
            await event.message.edit(text=account_info(customer_params),
                                       attachments=[await get_contacts_list(customer_params.id)])
        else:
            kb = InlineKeyboardBuilder()
            kb.add(
                RequestContactButton(text='Авторизоваться')
            )
            await event.message.edit(text=f'Здравствуйте.\n'
                                         f'Поделитесь своим номером телефона для использования бота.👇',
                                       attachments=[kb.as_markup()])
    else:
        await event.message.answer(text='Ошибка! Помогите нам её исправить. Сообщите об этой ошибке в онлайн-форме:',
                                   attachments=[await problem_button()])



@main_router.message_created(F.message.body.attachments[...].type == AttachmentType.CONTACT)
async def contact_received(event: MessageCreated, amo_api: AmoCRMWrapper, fields_id: dict):
    max_id = event.message.sender.user_id
    contact_attachment = next(
        (
            attachment
            for attachment in (event.message.body.attachments or [])
            if attachment.type == AttachmentType.CONTACT
        ),
        None,
    )
    if contact_attachment is None:
        return

    contact_phone = extract_phone_from_vcf(contact_attachment.payload.vcf_info or "")

    customer = amo_api.get_customer_by_phone(contact_phone)

    if customer[0]:
        contact_id = customer[2].get('id')
        responsible_manager = amo_api.get_responsible_user_by_id(int(customer[1].get('responsible_user_id')))
        customer[1]['manager'] = responsible_manager
        customer_params = amo_api.get_customer_params(customer[1], fields_id=fields_id)
        amo_api.put_max_id_to_customer(customer_params.id, max_id)
        amo_api.put_max_id_to_contact(id_contact=contact_id,
                                      max_id=max_id,
                                      fields_id=fields_id.get('contacts_fields_id'))

        await event.message.edit(text=f'Вы успешно авторизовались в чат боте HiTE PRO!\n\n'
                                  f'Можете посмотреть информацию из Вашего профиля и воспользоваться '
                                  f'магазином HiTE PRO👇',
                                   attachments=[await authorized_client(start_menu)])
    else:
        await event.message.answer(text=f'{customer[1]}\n\n'
                                  f'Воспользоваться чат-ботом могут только авторизованные партнёры.\n'
                                  f'👇 Если вы действующий партнёр компании HiTE PRO, '
                                  f'сообщите об этой ошибке в онлайн-форме.',
                                  attachments=[await problem_button()])


# Хэндлер для обработки инлайн кнопки "Показать контакты"
@main_router.message_callback(F.callback.payload.startswith('contacts_list'))
async def open_contacts_list_handler(event: MessageCallback, amo_api: AmoCRMWrapper):
    last_message = event.message.body.text
    payload = event.callback.payload
    customer_id = payload.split('_')[2]
    customer = amo_api.get_customer_by_id(customer_id, with_contacts=True)
    contacts_list_id = [contact.get('id') for contact in customer[1]['_embedded']['contacts']]
    last_message = last_message + '\n\n<b>Привязанные контакты к профилю</b>\n'

    for contact_id in contacts_list_id:
        contact_data = Contact(**amo_api.get_contact_by_id(contact_id))
        last_message = last_message + str(contact_data)

    await event.message.edit(text=last_message, attachments=[await hide_contacts_list(customer_id)])


# Хэндлер для обработки инлайн кнопки "Скрыть контакты"
@main_router.message_callback(F.callback.payload.startswith('hide_contacts_list'))
async def hide_contacts_list_handler(event: MessageCallback):
    payload = event.callback.payload
    customer_id = payload.split('_')[3]
    last_message = event.message.body.text
    hide_index = last_message.find('Привязанные')
    new_text = last_message[:hide_index]

    await event.message.edit(text=new_text, attachments=[await get_contacts_list(customer_id)])


@main_router.message_callback(F.callback.payload == '/contacts')  # Хэндлер для обработки команды /contacts
async def contacts(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('contact_message'), attachments=[await get_start_button()])


@main_router.message_callback(F.callback.payload == '/forum')
async def forum(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('forum_message'), attachments=[await forum_button()])

@main_router.message_callback(F.callback.payload == '/materials')
async def materials(event: MessageCallback):
    await event.message.edit(text='<b>Полезные материалы HiTE PRO.</b>\n\n'
                                          '👇 Используйте кнопки ниже, чтобы выбрать раздел.',
                             attachments=[await helpfull_materials_keyboard(helpfull_materials_menu)])

@main_router.message_callback(F.callback.payload == 'first_message')
async def first_message(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('helpful_materials').get('first_message'),
                             attachments=[await back_button()])

@main_router.message_callback(F.callback.payload == 'second_message')
async def second_message(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('helpful_materials').get('second_message'),
                             attachments=[await back_button()])

@main_router.message_callback(F.callback.payload == 'third_message')
async def third_message(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('helpful_materials').get('third_message'),
                             attachments=[await back_button()])

@main_router.message_callback(F.callback.payload == 'forth_message')
async def forth_message(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('helpful_materials').get('forth_message'),
                             attachments=[await back_button()])

@main_router.message_callback(F.callback.payload == 'five_message')
async def five_message(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('helpful_materials').get('five_message'),
                             attachments=[await back_button()])


@main_router.message_callback(F.callback.payload == '/partners')
async def partners(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('partner_kanal'),
                             attachments=[await get_start_button()])

@main_router.message_callback(F.callback.payload == '/manager')
async def manager(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('manager'),
                             attachments=[await manager_button()])


@main_router.message_callback(F.callback.payload == '/support')
async def support(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('support'),
                             attachments=[await support_button()])


@main_router.message_callback(F.callback.payload == '/problem')
async def problem(event: MessageCallback):
    await event.message.edit(text=Lexicon_RU.get('problem'),
                             attachments=[await problem_button()])
from maxapi.types import CallbackButton, LinkButton
from maxapi.utils.inline_keyboard import InlineKeyboardBuilder



# Главная inline клавиатура
async def get_start_keyboard(commands: dict): # Формирование главной инлайн клавиатуры
    kb_bl = InlineKeyboardBuilder()
    buttons: list = [
        CallbackButton(text=text,
                       payload=data) for data, text in commands.items() if data != '/start'
    ]
    kb_bl.add(*buttons)
    kb_bl.adjust(1)

    return kb_bl.as_markup()


async def get_contacts_list(customer_id): # Формирование кнопки раскрытия списка контактов партнёра
    button = CallbackButton(text='Список связанных контактов', payload=f'contacts_list_{customer_id}')
    kb_bl = InlineKeyboardBuilder().add(button)
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))
    kb_bl.adjust(1)

    return kb_bl.as_markup()


async def problem_button():  # Формирование клавиатуры для заполнения формы отзыва на бота
    button = LinkButton(
        text='Заполнить форму',
        url='https://forms.gle/wnxcfdTsPpHtNCcy9'
    )
    kb_bl = InlineKeyboardBuilder()
    kb_bl.add(button)
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))
    kb_bl.adjust(1)

    return kb_bl.as_markup()

async def authorized_client(commands: dict):
    kb_bl = InlineKeyboardBuilder()
    buttons: list = [
        CallbackButton(text=text,
                       payload=data) for data, text in commands.items() if data in ['/shop', '/info']
    ]
    kb_bl.add(*buttons)
    return kb_bl.as_markup()


async def hide_contacts_list(customer_id): # Формирование кнопки скрытия списка контактов партнёра
    kb_bl = InlineKeyboardBuilder()
    button = CallbackButton(text='Скрыть список контактов', payload=f'hide_contacts_list_{customer_id}')
    kb_bl.add(button)
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))
    kb_bl.adjust(1)
    return kb_bl.as_markup()

async def get_start_button():
    kb_bl = InlineKeyboardBuilder()
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))
    return kb_bl.as_markup()


async def forum_button(): # Формирование клавиатуры перехода на форум
    kb_bl = InlineKeyboardBuilder()
    button = LinkButton(
        text='Перейти на форум',
        url='https://max.ru/join/woDgvK-CGSe5x9DKQ_rZLMGwf9mT_DvvLA6Cv__iq6U'
    )
    kb_bl.add(button)
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))
    kb_bl.adjust(1)

    return kb_bl.as_markup()


async def helpfull_materials_keyboard(texts: dict):
    kb_bl = InlineKeyboardBuilder()
    buttons: list = [
        CallbackButton(text=text,
                       payload=data) for text, data in texts.items()
    ]
    kb_bl.add(*buttons)
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))
    kb_bl.adjust(1)
    return kb_bl.as_markup()

async def back_button():
    button = CallbackButton(text='Назад',
                            payload='/materials')
    kb_bl = InlineKeyboardBuilder().add(button)
    return kb_bl.as_markup()

async def manager_button():  # Формирование клавиатуры для связи с менеджером
    button_whatsapp = LinkButton(
        text="🟢 WhatsApp",
        url='https://wa.me/79251930861'
    )
    button_telegram = LinkButton(
        text='🔵 Telegram',
        url='https://t.me/+79251930861'
    )
    button_MAX = LinkButton(
        text='🟣 MAX',
        url='https://max.ru/u/f9LHodD0cOLRJPZ-Vm5lXdFA6YvPYESWoU7_n6imsgqQorxD9nvTdH9pXxU'
    )
    kb_bl = InlineKeyboardBuilder().add(button_whatsapp, button_telegram, button_MAX)
    kb_bl.add(CallbackButton(text='В главное меню', payload='/start'))

    kb_bl.adjust(1)
    return kb_bl.as_markup()


async def support_button(): # Формирование клавиатуры для связи с тех. поддержкой
    kb_bl = InlineKeyboardBuilder()
    button_whatsapp = LinkButton(
        text="🟢 WhatsApp",
        url='https://wa.me/79251894560'
    )
    button_telegram = LinkButton(
        text="🔵 Telegram",
        url='https://t.me/+79251894560'
    )
    button_MAX = LinkButton(
        text="🟣 MAX",
        url='https://max.ru/u/f9LHodD0cOLgkmm1pw0Fy8nY2N3E9npARi6-3lC_qZ_FVzXQu8WdfUF0rGs'
    )
    start_button = CallbackButton(text='В главное меню', payload='/start')
    buttons = [button_whatsapp, button_telegram, button_MAX, start_button]
    kb_bl.add(*buttons)
    kb_bl.adjust(1)
    return kb_bl.as_markup()
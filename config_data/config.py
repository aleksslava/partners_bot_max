import os.path
from dataclasses import dataclass
import dotenv
from environs import Env
from pathlib import Path
from dataclasses import dataclass


BASE_DIR = Path(__file__).resolve().parent.parent

fields_id = {
    'manager_id_field': 1506979, # Поле отв. менеджер
    'tg_id_field': 1104992, # Поле tg_id партнёра
    'max_id_field': 1106314, # Поле max_id партнёра
    'status_id_field': 972634,
    'by_this_period_id_field': 1104934,
    'bonuses_id_field': 971580,
    'town_id_field': 972054,
    'full_price': 1105022,
    'pipeline_id': 1628622, #  7411865 - воронка тест 1628622 - воронка партнёры
    'tag_id': 606054,
    'need_help_tag': 607773,
    'status_id_order': 32809260, #  61586805 - статус переговоры 32809260 - статус новый заказ
    'status_id_kp': 39080307, # статус КП отправлено
    'chat_id': -4950490417,
    'catalog_id': 1682,
    'contacts_fields_id': {
        'tg_id_field': 1097296,
        'max_id_field': 1105813,
        'tg_username_field': 1097294
    },

}

# Класс с токеном бота MAX
@dataclass
class MaxBot:
    token: str  #Токен для доступа к боту
    api_url: str | None



# Класс с данными для подключения к API AMO
@dataclass
class AmoConfig:
    amocrm_subdomain: str
    amocrm_client_id: str
    amocrm_client_secret: str
    amocrm_redirect_url: str
    amocrm_access_token: str | None
    amocrm_refresh_token: str | None
    amocrm_secret_code: str
    path_to_env: str

@dataclass
class Config:
    max_bot: MaxBot
    amo_config: AmoConfig
    amo_fields: dict





# Функция создания экземпляра класса config
def load_config(path: str | None = BASE_DIR / '.env'):
    env: Env = Env()
    env.read_env(path)

    return Config(
        max_bot=MaxBot(
            token=env("MAX_BOT_TOKEN", None) or env("BOT_TOKEN"),
            api_url=env("MAX_API_URL", None),
        ),
        amo_config=AmoConfig(
            path_to_env=path,
            amocrm_subdomain=env("AMOCRM_SUBDOMAIN"),
            amocrm_client_id=env("AMOCRM_CLIENT_ID"),
            amocrm_client_secret=env("AMOCRM_CLIENT_SECRET"),
            amocrm_redirect_url=env("AMOCRM_REDIRECT_URL"),
            amocrm_access_token=env("AMOCRM_ACCESS_TOKEN"),
            amocrm_refresh_token=env("AMOCRM_REFRESH_TOKEN"),
            amocrm_secret_code=env("AMOCRM_SECRET")
        ),
        amo_fields=fields_id,
    )










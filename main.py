import asyncio
import logging

from maxapi import Bot, Dispatcher

from config_data.config import load_config, Config
from maxapi.enums import parse_mode

from amo_api.amo_api import AmoCRMWrapper
from handlers.main_handlers import main_router
from middleware.amo_api import AmoApiMiddleware

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
)


config: Config = load_config()

bot = Bot(token=config.max_bot.token, parse_mode=parse_mode.ParseMode.HTML)
amo_api = AmoCRMWrapper(
    path=config.amo_config.path_to_env,
    amocrm_subdomain=config.amo_config.amocrm_subdomain,
    amocrm_client_id=config.amo_config.amocrm_client_id,
    amocrm_redirect_url=config.amo_config.amocrm_redirect_url,
    amocrm_client_secret=config.amo_config.amocrm_client_secret,
    amocrm_secret_code=config.amo_config.amocrm_secret_code,
    amocrm_access_token=config.amo_config.amocrm_access_token,
    amocrm_refresh_token=config.amo_config.amocrm_refresh_token,
)


dp = Dispatcher()
dp.include_routers(main_router)


async def run() -> None:
    logger.info("Starting hitepro_edu_bot for MAX")

    dp.middleware(AmoApiMiddleware(amo_api, fields_id=config.amo_fields))

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(run())
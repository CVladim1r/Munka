from aiogram import Dispatcher

from bot.handlers.admin import register_admin_handlers
from bot.handlers.employer import register_other_handlers
from bot.handlers.job_seeker import register_user_handlers


def register_all_handlers(dp: Dispatcher) -> None:
    handlers = (
        register_user_handlers,
        register_admin_handlers,
        register_other_handlers,
    )
    for handler in handlers:
        handler(dp)

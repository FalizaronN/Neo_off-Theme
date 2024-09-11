__version__ = (1, 0, 2)

#         █▄ █ █▄ ▄▀█ ▄▀█ ██▄ █▀▄ █▀█
#         █ ▀█ █ ▀█▀ █▀█ █▄█ █▄▀ █▄█
#              © Copyright 2024
#             https://t.me/W1l1z
#
# 🔒      Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html
#             N  E  X  A  L  I  Z  E

#meta developer: @W1l1z

# scope: hikka_only
# scope: hikka_min 1.6.0

import asyncio
from datetime import datetime
import pytz
from telethon.tl.functions.account import UpdateProfileRequest

from .. import loader, utils

@loader.tds
class TimeInNickMod(loader.Module):
    """Модуль для добавления текущего времени в ник и обновления его каждую минуту (По умолчанию: МСК)"""

    strings = {"name": "TimeInNick"}

    def __init__(self):
        self.running = False
        self.timezone = 'Europe/Moscow' 

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def timecmd(self, message):
        """Включить/выключить обновление времени в нике"""
        if self.running:
            self.running = False
            await message.edit("<emoji document_id=5213260226194583825>📌</emoji> <b>Обновление времени в нике остановлено</b> <emoji document_id=5213260226194583825>📌</emoji>")
        else:
            self.running = True
            await message.edit("<emoji document_id=5213260226194583825>📌</emoji> <b>Обновление времени в нике запущено</b> <emoji document_id=5213260226194583825>📌</emoji>")
            self.client.loop.create_task(self.update_nick())

    async def time_mskcmd(self, message):
        """Переключить время на МСК"""
        self.timezone = 'Europe/Moscow'
        await message.edit("<emoji document_id=5213260226194583825>📌</emoji> <b>Время в нике будет отображаться по МСК</b> <emoji document_id=5213260226194583825>📌</emoji>")
    
    async def time_ekbcmd(self, message):
        """Переключить время на ЕКБ"""
        self.timezone = 'Asia/Yekaterinburg'
        await message.edit("<emoji document_id=5213260226194583825>📌</emoji> <b>Время в нике будет отображаться по ЕКБ</b> <emoji document_id=5213260226194583825>📌</emoji>")

    async def time_omskcmd(self, message):
        """Переключить время на ОМСК"""
        self.timezone = 'Asia/Omsk'
        await message.edit("<emoji document_id=5213260226194583825>📌</emoji> <b>Время в нике будет отображаться по ОМСК</b> <emoji document_id=5213260226194583825>📌</emoji>")

    async def time_samaracmd(self, message):
        """Переключить время на Самару"""
        self.timezone = 'Europe/Samara'
        await message.edit("<emoji document_id=5213260226194583825>📌</emoji> <b>Время в нике будет отображаться по ОМСК</b> <emoji document_id=5213260226194583825>📌</emoji>")

    async def update_nick(self):
        while self.running:
            
            tz = pytz.timezone(self.timezone)
            current_time = datetime.now(tz).strftime("%H:%M")
            
            double_struck_time = self.to_double_struck(current_time)
            double_struck_bar = "𝕀"  

            me = await self.client.get_me()
            current_nick = me.first_name.split('𝕀')[0].strip()
            
            new_nick = f"{current_nick} {double_struck_bar} {double_struck_time}"
            try:
                await self.client(UpdateProfileRequest(first_name=new_nick))
            except Exception as e:
                print(f"Ошибка при обновлении ника: {e}")
            
            now = datetime.now()
            sleep_time = 60 - now.second
            await asyncio.sleep(sleep_time)

    def to_double_struck(self, text):
        """Преобразует текст в шрифт Double Struck"""
        normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        double_struck = "𝔸𝔹ℂ𝔻𝔼𝔽𝔾ℍ𝕀𝕁𝕂𝕃𝕄ℕ𝕆ℙℚℝ𝕊𝕋𝕌𝕍𝕎𝕏𝕐ℤ𝕒𝕓𝕔𝕕𝕖𝕗𝕘𝕙𝕚𝕛𝕜𝕝𝕞𝕟𝕠𝕡𝕢𝕣𝕤𝕥𝕦𝕧𝕨𝕩𝕪𝕫𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡"
        translation = str.maketrans(normal, double_struck)
        return text.translate(translation)
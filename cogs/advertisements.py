import discord

from discord.ext import commands, tasks
from datetime import datetime, timedelta
import pytz


class Advertisements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # ID del canal donde quieres enviar los anuncios
        self.channel_id = 1165179143646883951
        self.sent_notifications = set()  # Añade esto

        self.events = {
            "Devil Square": (["9:30", "18:30"], "https://www.guiamuonline.com/quest-mu-online/devil-square"),
            "Chaos Castle": (["12:15", "18:15", "21:15"], "https://www.guiamuonline.com/quest-mu-online/506-chaos-castle-reloaded"),
            "Red Dragon": (["12:15", "20:15"], "https://muonlinefanz.com/guide/hunting/red-dragon/"),
            "Blood Castle": (["12:25", "22:25"], "https://www.guiamuonline.com/quest-mu-online/blood-castle"),
            "Moss Merchant": (["12:30", "20:30"], "https://guiamuonline.com/npc-sistema/moss"),
            "Medusa": (["16:30"], "https://www.guiamuonline.com/boss/medusa"),
            "Golden Invasion": (["16:30"], "https://www.guiamuonline.com/eventos-mu-online/invasion-monster/golden-invasion"),
            "Core Magriffi": (["19:15"], "https://www.guiamuonline.com/eventos-mu-online/evento-boss/core-magriffy"),
            "Loren Deep": (["20:00"], "https://www.guiamuonline.com/eventos-mu-online/loren-deep"),
            "Kundun": (["22:30"], "https://www.guiamuonline.com/eventos-mu-online/evento-boss/kalima-kundun"),
            "Viejo pascuero invasion": (["23:59"], "https://www.guiamuonline.com/eventos-mu-online/invasion-monster/santas-village"),
        }
        self.roles = {
            "Devil Square": ("👿", 1166848413250355431),
            "Chaos Castle": ("🏰", 1166848360469233724),
            "Red Dragon": ("🐉", 1166848613587095632),
            "Blood Castle": ("🩸", 1166848668872212571),
            "Moss Merchant": ("🛒", 1166848707891830824),
            "Medusa": ("🐍", 1166848761583128766),
            "Golden Invasion": ("🥇", 1166848796211294398),
            "Core Magriffi": ("🌐", 1166848819464507522),
            "Loren Deep": ("🌊", 1166848840821903401),
            "Kundun": ("👑", 1166848931515338762),
            "Viejo pascuero invasion": ("🎅", 1166848992282427412)}
        self.check_events.start()

    def cog_unload(self):
        self.check_events.cancel()
        self.clear_sent_notifications.cancel()  # Añade esto

    @tasks.loop(minutes=0.5)
    async def check_events(self):
        now = datetime.now(pytz.timezone('America/Santiago'))
        print(f"Comprobando eventos a las {now.strftime('%H:%M:%S')}")
        for event, (times, url) in self.events.items():
            for time_str in times:
                # Obtiene la hora y los minutos de time_str
                hour, minute = map(int, time_str.split(':'))
                # Establece la hora y los minutos en el objeto datetime actual
                event_time = now.replace(
                    hour=hour, minute=minute, second=0, microsecond=0)

                # Si event_time es menor que now, entonces el evento ya ocurrió hoy, así que lo ignoramos
                if event_time < now:
                    print(
                        f"El evento {event} programado para las {event_time.strftime('%H:%M:%S')} ya ocurrió hoy.")
                    continue

                print(
                    f"Verificando el evento {event} programado para las {event_time.strftime('%H:%M:%S')}")
                print(f"Diferencia de tiempo para {event}: {event_time - now}")

                now_rounded = now.replace(second=0, microsecond=0)
                event_time_rounded = event_time.replace(
                    second=0, microsecond=0)

                print(f"Tiempo actual redondeado: {now_rounded}")
                print(f"Tiempo del evento redondeado: {event_time_rounded}")
                print(
                    f"Condición 1: {now_rounded > event_time_rounded - timedelta(minutes=10)}")
                print(
                    f"Condición 2: {now_rounded < event_time_rounded - timedelta(minutes=9)}")
                event_key = f"{event}_{event_time_rounded.strftime('%Y-%m-%d %H:%M')}"
                if event_key in self.sent_notifications:
                    continue  # Si ya se ha enviado una notificación para este evento, salta al siguiente

                if now_rounded > event_time_rounded - timedelta(minutes=10) and now_rounded < event_time_rounded:
                    print(f"Preparando para enviar aviso del evento {event}")
                    self.sent_notifications.add(event_key)
                    channel = self.bot.get_channel(self.channel_id)
                    if channel:  # Verifica si el canal es válido
                        # Obtén el ID del rol correspondiente al evento
                        role_id = self.roles[event][1]
                        # Obtén el objeto Role usando get_role
                        role = channel.guild.get_role(role_id)
                        if role:  # Verifica si el rol es válido
                            print(
                                f"Enviando aviso del evento {event} con mención al rol {role.name}")
                            embed = discord.Embed(
                                title=f"Evento: {event}",
                                description=f"El evento {event} comenzará en 10 minutos! Más info [aquí]({url}). {role.mention}",
                                color=discord.Color.blue()
                            )
                            await channel.send(embed=embed)
                        else:
                            print(f"Rol con ID {role_id} no encontrado")
                    else:
                        print(f"Canal con ID {self.channel_id} no encontrado")

    @tasks.loop(hours=24)  # Añade esto
    async def clear_sent_notifications(self):
        self.sent_notifications.clear()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.check_events.is_running():
            self.check_events.start()
        if not self.clear_sent_notifications.is_running():  # Añade esto
            self.clear_sent_notifications.start()


async def setup(bot) -> None:
    await bot.add_cog(Advertisements(bot))

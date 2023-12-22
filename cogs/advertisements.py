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
            # "Moss Merchant": (["12:30", "20:30"], "https://guiamuonline.com/npc-sistema/moss"),
            
            "Devil Square": (["00:20", "00:50", "01:20", "01:50", "02:20", "02:50", "03:20", "03:50", "04:20", "04:50", "05:20", "05:50", "06:20", "06:50", "07:20", "07:50", "08:20", "08:50", "09:20", "09:50", "10:20", "10:50", "11:20", "11:50", "12:20", "12:50", "13:20", "13:50", "14:20", "14:50", "15:20", "15:50", "16:20", "16:50", "17:20", "17:50", "18:20", "18:50", "19:20", "19:50", "20:20", "20:50", "21:20", "21:50", "22:20", "22:50", "23:20", "23:50"], "https://www.guiamuonline.com/quest-mu-online/devil-square"),
            "Chaos Castle": (["01:00", "03:00", "05:00", "07:00", "09:00", "11:00", "13:00", "15:00", "17:00", "19:00", "21:00", "23:00"], "https://www.guiamuonline.com/quest-mu-online/506-chaos-castle-reloaded"),
            "Blood Castle": (["00:10", "00:40", "01:10", "01:40", "02:10", "02:40", "03:10", "03:40", "04:10", "04:40", "05:10", "05:40", "06:10", "06:40", "07:10", "07:40", "08:10", "08:40", "09:10", "09:40", "10:10", "10:40", "11:10", "11:40", "12:10", "12:40", "13:10", "13:40", "14:10", "14:40", "15:10", "15:40", "16:10", "16:40", "17:10", "17:40", "18:10", "18:40", "19:10", "19:40", "20:10", "20:40", "21:10", "21:40", "22:10", "22:40", "23:10", "23:40"], "https://www.guiamuonline.com/quest-mu-online/blood-castle"),
            "Red Dragon": (["23:10"], "https://muonlinefanz.com/guide/hunting/red-dragon/"),
            "Tigers": (["00:25", "01:25", "02:25", "03:25", "04:25", "05:25", "06:25", "07:25", "08:25", "09:25", "10:25", "11:25", "12:25", "13:25", "14:25", "15:25", "16:25", "17:25", "18:25", "19:25", "20:25", "21:25", "22:25", "23:25"], "#"),
            "Golden Goblins": (["00:10", "01:10", "02:10", "03:10", "04:10", "05:10", "06:10", "07:10", "08:10", "09:10", "10:10", "11:10", "12:10", "13:10", "14:10", "15:10", "16:10", "17:10", "18:10", "19:10", "20:10", "21:10", "22:10", "23:10"], "#"),
            "Golden Invasion": (["12:00","22:00"], "https://www.guiamuonline.com/eventos-mu-online/invasion-monster/golden-invasion"),
            "Ice Queen": (["00:01","04:01","08:01","12:01","16:01","20:01"], "#"),
            "Balrog": (["00:00" ,"08:00","16:00"], "#"),
            "Hero Mutant": (["12:00","23:50"], "#"),
        }
        self.roles = {
            "Devil Square": ("👿", 1166848413250355431),
            "Chaos Castle": ("🏰", 1166848360469233724),
            "Blood Castle": ("🩸", 1166848668872212571),
            "Red Dragon": ("🐉", 1166848613587095632),
            "Tigers": ("🐅", 1166848761583128766),
            "Golden Goblins": ("👺", 1166848707891830824),
            "Golden Invasion": ("🥇", 1166848796211294398),
            "Ice Queen": ("🌊", 1166848819464507522),
            "Balrog": ("👑", 1166848840821903401),
            "Hero Mutant": ("🤖", 1166848992282427412)}
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
                                description=f"El evento {event} comenzará en 10 minutos! Más info [aquí]({url}).",
                                color=discord.Color.blue()
                            )
                            msj_mention= f"{role.mention}"
                            await channel.send(msj_mention,embed=embed)
                        else:
                            print(f"Rol con ID {role_id} no encontrado")
                    else:
                        print(f"Canal con ID {self.channel_id} no encontrado")

    @tasks.loop(hours=24)
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


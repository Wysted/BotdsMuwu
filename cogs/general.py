""""
Copyright © Krypton 2019-2023 - https://github.com/kkrypt0nn (https://krypton.ninja)
Description:
🐍 A simple template to start to code your own and personalized discord bot in Python programming language.

Version: 6.1.0
"""

import platform
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from datetime import datetime, timedelta
import pytz

tz = pytz.timezone("America/Santiago")


class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)

    # Message context menu command
    async def remove_spoilers(
        self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """
        Removes the spoilers from the message. This command requires the MESSAGE_CONTENT intent to work properly.

        :param interaction: The application command interaction.
        :param message: The message that is being interacted with.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
        embed = discord.Embed(
            title="Message without spoilers",
            description=message.content.replace("||", ""),
            color=0xBEBEFE,
        )
        if spoiler_attachment is not None:
            embed.set_image(url=attachment.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
        self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        """
        Grabs the ID of the user.

        :param interaction: The application command interaction.
        :param user: The user that is being interacted with.
        """
        embed = discord.Embed(
            description=f"The ID of {user.mention} is `{user.id}`.",
            color=0xBEBEFE,
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="help", description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.config["prefix"]
        embed = discord.Embed(
            title="Help", description="List of available commands:", color=0xBEBEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for command in commands:
                description = command.description.partition("\n")[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Get some useful (or not) information about the bot.",
    )
    async def botinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the bot.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description="Used [Krypton's](https://krypton.ninja) template",
            color=0xBEBEFE,
        )
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="Krypton#7331", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(
            name="Prefix:",
            value=f"/ (Slash Commands) or {self.bot.config['prefix']} for normal commands",
            inline=False,
        )
        embed.set_footer(text=f"Requested by {context.author}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, context: Context) -> None:
        """
        Get some useful (or not) information about the server.

        :param context: The hybrid command context.
        """
        roles = [role.name for role in context.guild.roles]
        if len(roles) > 50:
            roles = roles[:50]
            roles.append(f">>>> Displayin [50/{len(roles)}] Roles")
        roles = ", ".join(roles)

        embed = discord.Embed(
            title="**Server Name:**", description=f"{context.guild}", color=0xBEBEFE
        )
        if context.guild.icon is not None:
            embed.set_thumbnail(url=context.guild.icon.url)
        embed.add_field(name="Server ID", value=context.guild.id)
        embed.add_field(name="Member Count", value=context.guild.member_count)
        embed.add_field(
            name="Text/Voice Channels", value=f"{len(context.guild.channels)}"
        )
        embed.add_field(
            name=f"Roles ({len(context.guild.roles)})", value=roles)
        embed.set_footer(text=f"Created at: {context.guild.created_at}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="ping",
        description="Check if the bot is alive.",
    )
    async def ping(self, context: Context) -> None:
        """
        Check if the bot is alive.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"The bot latency is {round(self.bot.latency * 1000)}ms.",
            color=0xBEBEFE,
        )
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get the invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: Context) -> None:
        """
        Get the invite link of the bot to be able to invite it.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here]({self.bot.config['invite_link']}).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Get the invite link of the discord server of the bot for some support.",
    )
    async def server(self, context: Context) -> None:
        """
        Get the invite link of the discord server of the bot for some support.

        :param context: The hybrid command context.
        """
        embed = discord.Embed(
            description=f"Join the support server for the bot by clicking [here](https://discord.gg/mTBrXyWxAF).",
            color=0xD75BF4,
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="8ball",
        description="Ask any question to the bot.",
    )
    @app_commands.describe(question="The question you want to ask.")
    async def eight_ball(self, context: Context, *, question: str) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """
        answers = [
            "It is certain.",
            "It is decidedly so.",
            "You may rely on it.",
            "Without a doubt.",
            "Yes - definitely.",
            "As I see, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again later.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        embed = discord.Embed(
            title="**My Answer:**",
            description=f"{random.choice(answers)}",
            color=0xBEBEFE,
        )
        embed.set_footer(text=f"The question was: {question}")
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="eventos",
        description="Eventos del server MUWU",
    )
    @app_commands.describe()
    async def events(self, context: Context) -> None:
        """
        Ask any question to the bot.

        :param context: The hybrid command context.
        :param question: The question that should be asked by the user.
        """

        hora_actual = datetime.now(tz)
        hora_formateada = hora_actual.strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(
            title="**Los eventos son los siguientes:**",
            description=f"Lista de eventos",
            color=0xBEBEFE,
        )
        events = {
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
            "Viejo pascuero invasion": (["00:00"], "https://www.guiamuonline.com/eventos-mu-online/invasion-monster/santas-village")
        }
        for event, (times, link) in events.items():
            if times:  # solo añadir el campo si hay horarios
                # Unir todos los horarios con una coma
                text = " - ".join(times)
                closest_time = None
                for time in times:
                    event_time_str = f"{hora_actual.strftime('%Y-%m-%d')} {time}"
                    event_time = datetime.strptime(
                        event_time_str, '%Y-%m-%d %H:%M')
                    # Asegurar que el evento tenga la zona horaria
                    event_time = tz.localize(event_time)

                    # Ajustar al día siguiente si el evento ya pasó hoy
                    if event_time < hora_actual:
                        event_time += timedelta(days=1)

                    if closest_time is None or (event_time - hora_actual) < (closest_time - hora_actual):
                        closest_time = event_time

                # Formatear la hora más cercana y añadir al embed
                closest_time_str = closest_time.strftime("%H:%M")
                # Calcular el tiempo restante y formatearlo
                remaining_time = closest_time - hora_actual
                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                remaining_time_str = f"{int(hours)}h {int(minutes)}m"
                embed.add_field(
                    name=f"{event}",
                    value=f"📅 {text} \n\n  `El evento empezara en {remaining_time_str}` [🤓]({link})",
                    inline=False
                )

        embed.set_footer(text=f"Hora servidor : {hora_formateada}")
        await context.send(embed=embed)


async def setup(bot) -> None:
    await bot.add_cog(General(bot))

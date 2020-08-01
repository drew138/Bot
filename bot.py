# bot.py
import os
import requests
from datetime import datetime
import gspread
import discord
from discord.ext import commands
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


def authorize_google(func):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets'",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open().sheet1

    def wrapper_function(*args, **kwargs):
        return func(*args, sheet=sheet, **kwargs)
    return wrapper_function


@authorize_google
def get_column(column, sheet=sheet):
    return sheet.col_values(column)


@authorize_google
def retrieve_data(sheet=sheet):
    return sheet.get_all_records()


sheet.findall("valor")

'''
client = discord.Client()
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hola {member.name}, bienvenido a Grupo Sistemas 2020-2!'
    )


client.run(TOKEN)
'''

bot = commands.Bot(command_prefix='!')


@bot.command(name='add', help='- Añade un examen en una fecha especificada')
async def add(ctx, materia, semana):
    courses = requests.get()
    if 1 <= semana <= 18 and materia in courses:
        weeks = requests.post()
    else:
        response = "Lo siento, la materia o la fecha especificada es invalida\n"
        await ctx.send(response)


@bot.command(name='ver_examenes_semana', help='- Te dice los examenes de la semana')
async def exams(ctx, materia, semana):
    courses = requests.get()
    if 1 <= semana <= 18 and materia in courses:
        weeks = requests.post()
    else:
        response = "Lo siento, la materia o la fecha especificada es invalida\n"
        await ctx.send(response)


@bot.command(name='pair', help='- Aplicación para programar en grupos')
async def pair_programming(ctx):
    replit = "programa en grupos con: \nhttps://repl.it/"
    await ctx.send(replit)


@bot.command(pass_context=True)
async def addrole(ctx, role: discord.Role, member: discord.Member = None):
    member = member or ctx.message.author
    await client.add_roles(member, role)
    # https://stackoverflow.com/questions/48987006/how-to-make-a-discord-bot-that-gives-roles-in-python


@bot.command(name='semana', help='- Te dice la semana actual')
async def current_week(ctx):
    num_weeks = get_column(1)
    date_weeks = get_column(2)


@bot.command(name='ver_numero_semana', help='- Te dice el numero de la semana')
async def weeknum(ctx):

    response = "SEMANAS\tFECHAS\n" \
               "2\t\t1 agosto\n" \
               "3\t\t8 agosto\n" \
               "4\t\t15 agosto\n"\
               "5\t\t22 agosto\n"\
               "6\t\t29 agosto\n"\
               "7\t\t5 septiembre\n"\
               "8\t\t12 septiembre\n"\
               "9\t\t19 septiembre\n"\
               "\tRECESO\n"\
               "10\t\t3 octubre\n"\
               "11\t\t10 octubre\n"\
               "12\t\t17 octubre\n"\
               "13\t\t24 octubre\n"\
               "14\t\t31 octubre\n"\
               "15\t\t7 noviembre\n"\
               "16\t\t14 noviembre\n"\
               "17\t\t21 noviembre\n"\
               "18\t\t28 noviembre\n"\
               "19\t\t5 diciembre\n"\
               "20\t\t12 diciembre\n"

    await ctx.send(response)


# bot.run(TOKEN)

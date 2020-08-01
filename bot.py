# bot.py
import os
import requests
from prettytable import PrettyTable
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
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open("WEBSERVERFECHASDISCORD").sheet1

    def wrapper_function(*args):
        return func(*args, sheet)

    return wrapper_function


@authorize_google
def get_column(column, sheet):
    return sheet.col_values(column)


@authorize_google
def cell_up(row, column, value, sheet):
    sheet.update_cell(row, column, value)


@authorize_google
def get_row(row, sheet):
    return sheet.row_values(row)


@authorize_google
def get_cell(column, row, sheet):
    return sheet.cell(column, row).value


@authorize_google
def retrieve_data(sheet):
    return sheet.get_all_records()


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
async def add(ctx, materia, semana, examen):
    courses = get_row(1)
    semana = int(semana)
    if 1 <= semana <= 20 and materia in courses:
        column = courses.index(materia) + 1
        old = get_cell(semana, column)

        if old:
            new = ", ".join([old, examen])
        else:
            new = examen

        cell_up(semana, column, new)

        response = "El examen ha sido agregado"
        await ctx.send(response)
    else:
        response = "Lo siento, la materia o la fecha especificada es invalida\n"
        await ctx.send(response)


@bot.command(name='ver_examenes_materia', help='- Te dice los examenes de la semana')
async def exams(ctx, semana, materia=None):
    response = ""
    header = get_row(1)
    if materia:
        courses = header[2:]
        if 1 <= int(semana) <= 20 and materia in courses:
            column = header.index(materia) + 1
            cell = get_cell(semana, column)
            if cell:
                response = f"Para la semana {semana} de la materia {materia} hay: \n{cell}"
            else:
                response = f"Para la semana {semana} de la materia {materia} NO HAY examenes"
        else:
            response = "Lo siento, la materia o la fecha especificada es invalida\n"
    else:
        header = get_row(1)
        response = PrettyTable(header)
        row = get_row(semana)

        for index, element in enumerate(row):
            ele = element.split(',')
            row[index] = ele

        response.add_column(row)

        response = f"```{response}```"

    await ctx.send(response)


@bot.command(name='quitar', help='- Eliminar un examen')
async def delete(ctx, semana, materia, examen):
    courses = get_row(1)
    semana = int(semana)
    if 1 <= semana <= 20 and materia in courses:
        column = courses.index(materia) + 1
        exams = (get_cell(semana, column)).split(', ')

        newlist = [k for k in exams if k != examen]

        if newlist:
            exams = ", ".join(newlist)
        else:
            exams = ""

        cell_up(semana, column, exams)

        response = "El examen ha sido eliminado"
        await ctx.send(response)
    else:
        response = "Lo siento, la materia o la fecha especificada es invalida\n"
        await ctx.send(response)


@bot.command(name='pair', help='- Aplicación para programar en grupos')
async def pair_programming(ctx):
    replit = "programa en grupos con: \nhttps://repl.it/"
    await ctx.send(replit)


'''
@bot.command(pass_context=True)
async def addrole(ctx, role: discord.Role, member: discord.Member = None):
    member = member or ctx.message.author
    await client.add_roles(member, role)
    # https://stackoverflow.com/questions/48987006/how-to-make-a-discord-bot-that-gives-roles-in-python
'''


@bot.command(name='semana', help='- Te dice la semana actual')
async def current_week(ctx):
    date = datetime.now()
    num_weeks = get_column(1)[1:]
    date_weeks = list(map(lambda x: datetime.strptime(x, '%d/%m/%Y'), get_column(2)[1:]))
    sizeweeks = len(date_weeks) - 1

    for index, dates in enumerate(zip(num_weeks, date_weeks)):
        week, dateweek = dates

        if (index < sizeweeks) and (dateweek <= date <= date_weeks[index + 1]):
            response = f"La semana actual es la: {week}"
            await ctx.send(response)
            break
        elif index == sizeweeks:
            response = f"La semana actual es la: {week}"
            await ctx.send(response)
            break


@bot.command(name='ver_numero_semana', help='- Te dice el numero de la semana')
async def weeknum(ctx):
    table = PrettyTable()
    header = ['Semanas', 'Fechas']
    table.add_column(header[0], get_column(1)[1:])
    table.add_column(header[1], get_column(2)[1:])
    await ctx.send(f"```{table}```")


bot.run(TOKEN)

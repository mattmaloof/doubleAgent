import os
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from discord.ext.commands import MissingRequiredArgument
from discord.ext.commands import CommandInvokeError
from discord.ext.commands import MissingRole
from Google import Create_Service
from gspread_formatting import *
from discord import message

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
client = commands.Bot(command_prefix = '.') #created instance of bot and set it to client variable
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]
requests = []
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
googleClient = gspread.authorize(creds)
spreadsheet_id = '1KGW_MlcN68xtJ0ZPWgRzUcNQJ0riHu19fBTUGg5EzIU'
sheet_id = '2003992854'
sheetAB_id = '300876247'
sheetMain = googleClient.open("MM21 Abusement Park LvL Tracker").sheet1
sheetUsers = googleClient.open("MM21 Abusement Park LvL Tracker").worksheet("users")
sheetABMain = googleClient.open("MM21 Abusement Park LvL Tracker").worksheet("AB LvL")
sheetABUsers = googleClient.open("MM21 Abusement Park LvL Tracker").worksheet("ABusers")

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

next_row = next_available_row(sheetUsers)

@client.event   #made first event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send(f'{ctx.message.author.mention}, you have entered an invalid command.\n'
                       f'Type \'.commands\' for a full list of available commands.')
        return
    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f'{ctx.message.author.mention}, you are missing an argument for the command entered.\n'
                       f'Type \'.commands\' for a full list of available commands.')
        return
    if isinstance(error, MissingRole):
        await ctx.send(f'{ctx.message.author.mention}, you do not have the required role to use this command.\n')
        return
    raise error


@client.command()
async def updateall(ctx, power, offOvr, defOvr):
    try:
        id = str(ctx.author.id)
        cell = sheetUsers.find(id[:-6])
        if 2000 < int(power) < 4000 and 80 < int(offOvr) < 95 and 80 < int(defOvr) < 95:
            id = str(ctx.author.id)
            cell = sheetUsers.find(id[:-6])
            name = sheetUsers.cell(cell.row, cell.col-1).value
            locationCell = sheetMain.find(name)
            sheetMain.update_cell(locationCell.row, 4, power)
            sheetMain.update_cell(locationCell.row, 5, offOvr)
            sheetMain.update_cell(locationCell.row, 6, defOvr)
            await ctx.send(f'{ctx.message.author.mention}, your information has successfully been updated!')
        if 2000 > int(power) or int(power) > 4000:
            await ctx.send(f'{ctx.message.author.mention}, power value must be between 2000 and 4000.')
        if 80 > int(offOvr) or int(offOvr) > 95:
            await ctx.send(f'{ctx.message.author.mention}, offensive overall value must be between 80 and 95.')
        if 80 > int(defOvr) or int(defOvr) > 95:
            await ctx.send(f'{ctx.message.author.mention}, defensive overall value must be between 80 and 95.')
    except gspread.exceptions.CellNotFound:
        id = str(ctx.author.id)
        cell = sheetABUsers.find(id[:-6])
        if 2000 < int(power) < 4000 and 80 < int(offOvr) < 95 and 80 < int(defOvr) < 95:
            id = str(ctx.author.id)
            cell = sheetABUsers.find(id[:-6])
            name = sheetABUsers.cell(cell.row, cell.col-1).value
            locationCell = sheetABMain.find(name)
            sheetABMain.update_cell(locationCell.row, 4, power)
            sheetABMain.update_cell(locationCell.row, 5, offOvr)
            sheetABMain.update_cell(locationCell.row, 6, defOvr)
            await ctx.send(f'{ctx.message.author.mention}, your information has successfully been updated!')
        if 2000 > int(power) or int(power) > 4000:
            await ctx.send(f'{ctx.message.author.mention}, power value must be between 2000 and 4000.')
        if 80 > int(offOvr) or int(offOvr) > 95:
            await ctx.send(f'{ctx.message.author.mention}, offensive overall value must be between 80 and 95.')
        if 80 > int(defOvr) or int(defOvr) > 95:
            await ctx.send(f'{ctx.message.author.mention}, defensive overall value must be between 80 and 95.')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
@commands.has_role('Mod')
async def lvlsummaryAP(ctx, leagueName, ourScore, oppScore, ourRank, players, ourCompDrives, oppCompDrives):
    try:
        name = sheetMain.find(leagueName)
        row = sheetMain.find("Opponent Score")
        row2 = sheetMain.find("Our Rank")
        row3 = sheetMain.find("Our completed drives")
        sheetMain.update_cell(row.row - 1, name.col, ourScore)
        sheetMain.update_cell(row.row, name.col, oppScore)
        sheetMain.update_cell(row2.row , name.col, ourRank)
        sheetMain.update_cell(row2.row+1 , name.col, players)
        sheetMain.update_cell(row3.row , name.col, ourCompDrives)
        sheetMain.update_cell(row3.row+1 , name.col, oppCompDrives)
        await ctx.send(f'{ctx.message.author.mention}, information has successfully been updated!')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, make sure your league name input\'s capitalization is correct.')

@client.command()
@commands.has_role('Mod')
async def lvlsummaryAB(ctx, leagueName, ourScore, oppScore, ourRank, players, ourCompDrives, oppCompDrives):
    try:
        name = sheetABMain.find(leagueName)
        row = sheetABMain.find("Opponent Score")
        row2 = sheetABMain.find("Our Rank")
        row3 = sheetABMain.find("Our completed drives")
        sheetABMain.update_cell(row.row - 1, name.col, ourScore)
        sheetABMain.update_cell(row.row, name.col, oppScore)
        sheetABMain.update_cell(row2.row , name.col, ourRank)
        sheetABMain.update_cell(row2.row+1 , name.col, players)
        sheetABMain.update_cell(row3.row , name.col, ourCompDrives)
        sheetABMain.update_cell(row3.row+1 , name.col, oppCompDrives)
        await ctx.send(f'{ctx.message.author.mention}, information has successfully been updated!')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, make sure your league name input\'s capitalization is correct.')

@client.command()
async def updatepow(ctx, power):
    try:
        if 2000 < int(power) < 4000:
            id = str(ctx.author.id)
            cell = sheetUsers.find(id[:-6])
            name = sheetUsers.cell(cell.row, cell.col - 1).value
            locationCell = sheetMain.find(name)
            sheetMain.update_cell(locationCell.row, 4, power)
            await ctx.send(f'{ctx.message.author.mention}, your power has successfully been updated!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, power value must be between 2000 and 4000.')
    except gspread.exceptions.CellNotFound:
        if 2000 < int(power) < 4000:
            id = str(ctx.author.id)
            cell = sheetABUsers.find(id[:-6])
            name = sheetABUsers.cell(cell.row, cell.col - 1).value
            locationCell = sheetABMain.find(name)
            sheetABMain.update_cell(locationCell.row, 4, power)
            await ctx.send(f'{ctx.message.author.mention}, your power has successfully been updated!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, power value must be between 2000 and 4000.')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
async def updateoff(ctx, offOvr):
    try:
        if 80 < int(offOvr) < 95:
            id = str(ctx.author.id)
            cell = sheetUsers.find(id[:-6])
            name = sheetUsers.cell(cell.row, cell.col - 1).value
            locationCell = sheetMain.find(name)
            sheetMain.update_cell(locationCell.row, 5, offOvr)
            await ctx.send(f'{ctx.message.author.mention}, your offensive overall has successfully been updated!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, offensive overall value must be between 80 and 95.')
    except gspread.exceptions.CellNotFound:
        if 80 < int(offOvr) < 95:
            id = str(ctx.author.id)
            cell = sheetABUsers.find(id[:-6])
            name = sheetABUsers.cell(cell.row, cell.col - 1).value
            locationCell = sheetABMain.find(name)
            sheetABMain.update_cell(locationCell.row, 5, offOvr)
            await ctx.send(f'{ctx.message.author.mention}, your offensive overall has successfully been updated!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, offensive overall value must be between 80 and 95.')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
async def updatedef(ctx, defOvr):
    try:
        if 80 < int(defOvr) < 95:
            id = str(ctx.author.id)
            cell = sheetUsers.find(id[:-6])
            name = sheetUsers.cell(cell.row, cell.col - 1).value
            locationCell = sheetMain.find(name)
            sheetMain.update_cell(locationCell.row, 6, defOvr)
            await ctx.send(f'{ctx.message.author.mention}, your defensive overall has successfully been updated!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, defensive overall value must be between 80 and 95.')
    except gspread.exceptions.CellNotFound:
        if 80 < int(defOvr) < 95:
            id = str(ctx.author.id)
            cell = sheetABUsers.find(id[:-6])
            name = sheetABUsers.cell(cell.row, cell.col - 1).value
            locationCell = sheetABMain.find(name)
            sheetABMain.update_cell(locationCell.row, 6, defOvr)
            await ctx.send(f'{ctx.message.author.mention}, your defensive overall has successfully been updated!')
        else:
            await ctx.send(f'{ctx.message.author.mention}, defensive overall value must be between 80 and 95.')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
@commands.has_role("Abusement Park")
async def setupAP(ctx, userName):
    global next_row
    try:
        id = str(ctx.author.id)
        cell = sheetUsers.find(id[:-6])
        await ctx.send(f'{ctx.message.author.mention}, you have already been set up!')
    except gspread.exceptions.CellNotFound:
        id = str(ctx.author.id)
        sheetUsers.update_acell("A{}".format(next_row), userName)
        sheetUsers.update_acell("B{}".format(next_row), id[:-6])
        next_row = next_available_row(sheetUsers)
        await ctx.send(f'{ctx.message.author.mention}, you have successfully been set up!')

@client.command()
@commands.has_role("Bandits")
async def setupAB(ctx, userName):
    global next_row
    try:
        id = str(ctx.author.id)
        cell = sheetABUsers.find(id[:-6])
        await ctx.send(f'{ctx.message.author.mention}, you have already been set up!')
    except gspread.exceptions.CellNotFound:
        id = str(ctx.author.id)
        sheetABUsers.update_acell("A{}".format(next_row), userName)
        sheetABUsers.update_acell("B{}".format(next_row), id[:-6])
        next_row = next_available_row(sheetABUsers)
        await ctx.send(f'{ctx.message.author.mention}, you have successfully been set up!')

@client.command()
@commands.has_role('Mod')
async def newlvlAP(ctx, clanName, rank, date):
    request_body = {
        'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 12,
                        'endIndex': 13
                    }
                }
            }
        ]
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body = request_body
    ).execute()
    sheetMain.update_cell(1, 13, clanName)
    sheetMain.update_cell(2, 13, rank)
    sheetMain.update_cell(3, 13, date)
    await ctx.send(f'{ctx.message.author.mention}, you have successfully created a new lvl with clan {clanName} ranked {rank} on {date}.')

@client.command()
@commands.has_role('Mod')
async def newlvlAB(ctx, clanName, rank, date):
    request_body = {
        'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': sheetAB_id,
                        'dimension': 'COLUMNS',
                        'startIndex': 12,
                        'endIndex': 13
                    }
                }
            }
        ]
    }
    service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheet_id,
        body = request_body
    ).execute()
    sheetABMain.update_cell(1, 13, clanName)
    sheetABMain.update_cell(2, 13, rank)
    sheetABMain.update_cell(3, 13, date)
    await ctx.send(f'{ctx.message.author.mention}, you have successfully created a new lvl with clan {clanName} ranked {rank} on {date}.')

@client.command()
async def rank(ctx):
    try:
        id = str(ctx.author.id)
        cell = sheetUsers.find(id[:-6])
        name = sheetUsers.cell(cell.row, cell.col - 1).value
        locationCell = sheetMain.find(name)
        rank = sheetMain.cell(locationCell.row, 1).value
        await ctx.send(f'{ctx.message.author.mention}, your current rank is {rank}!')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
async def lvlscore(ctx, score):
    try:
        id = str(ctx.author.id)
        cell = sheetUsers.find(id[:-6])
        name = sheetUsers.cell(cell.row, cell.col - 1).value
        locationCell = sheetMain.find(name)
        sheetMain.update_cell(locationCell.row, 13, score)
        if int(score) == 24:
            emoji = u"\U0001F40D"
            await message.Message.add_reaction(ctx.message, emoji)
        await ctx.send(f'{ctx.message.author.mention}, your score for the current LvL has been updated to {score}!')
    except gspread.exceptions.CellNotFound:
        id = str(ctx.author.id)
        cell = sheetABUsers.find(id[:-6])
        name = sheetABUsers.cell(cell.row, cell.col - 1).value
        locationCell = sheetABMain.find(name)
        sheetABMain.update_cell(locationCell.row, 13, score)
        if int(score) == 24:
            emoji = u"\U0001F40D"
            await message.Message.add_reaction(ctx.message, emoji)
        await ctx.send(f'{ctx.message.author.mention}, your score for the current LvL has been updated to {score}!')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
async def pastlvlscore(ctx, clanName, score):
    try:
        id = str(ctx.author.id)
        cell = sheetUsers.find(id[:-6])
        name = sheetUsers.cell(cell.row, cell.col - 1).value
        locationCell = sheetMain.find(name)
        index = sheetMain.find(clanName)
        sheetMain.update_cell(locationCell.row, index.col, score)
        await ctx.send(f'{ctx.message.author.mention}, your score for the most recent LvL against {clanName} has been updated to {score}!')
    except gspread.exceptions.CellNotFound:
        id = str(ctx.author.id)
        cell = sheetABUsers.find(id[:-6])
        name = sheetABUsers.cell(cell.row, cell.col - 1).value
        locationCell = sheetABMain.find(name)
        index = sheetABMain.find(clanName)
        sheetABMain.update_cell(locationCell.row, index.col, score)
        await ctx.send(
            f'{ctx.message.author.mention}, your score for the most recent LvL against {clanName} has been updated to {score}!')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
async def counterlist(ctx):
    await ctx.send(f'{ctx.message.author.mention}, the list of current play counters include:\n'
                   f'HB Blast\n'
                   f'HB Power Sweep\n'
                   f'HB Base\n'
                   f'Middle Slant\n'
                   f'Middle Slant 2PT\n'
                   f'Double Drags\n'
                   f'Double Drags 2PT\n'
                   f'WR Drag 2PT\n'
                   f'PA Spot 2PT\n'
                   f'PA Switch Dig\n'
                   f'PA Slot Crosses\n'
                   f'Posts\n'
                   f'X Follow\n'
                   f'TE Angle\n'
                   f'TE Out\n'
                   f'WR Corner\n'
                   f'Post Drags\n'
                   f'Z Spot\n'
                   f'Hail Mary\n'
                   f'Inside Swtich 2PT\n'
                   f'PA Fork 2PT\n'
                   f'Slot Flags\n'
                   f'Sluggo\n'
                   f'Seattle\n'
                   f'HB Plunge\n'
                   f'01 Trap\n'
                   f'PA Clearout\n'
                   f'Spot Opt 2PT\n'
                   f'HB Base 2PT\n'
                   f'PA Power O\n'
                   f'HB Zone\n'
                   f'PA Spot\n'
                   f'Blast Alert X Smoke')
@client.command()
async def counter(ctx, play):
    if play.lower() == "HB Blast".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **4-3 Cover 1 Robber Press**')
    elif play.lower() == "HB Power Sweep".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Sam Mike 2**')
    elif play.lower() == "HB Base".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **\nVert : Mike Scrape 3 Press, Cover 6 Press'
                       f'\nPederson : Sam Mike 2**')
    elif play.lower() == "Middle Slant".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Mike Scrape Press 3, 1 QB Contain Spy (3-4 Find By Formation)**')
    elif play.lower() == "Middle Slant 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Tango**')
    elif play.lower() == "Double Drags".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Sam Blitz 2, 1 QB Contain Spy (3-4 Find By Formation)**')
    elif play.lower() == "Double Drags 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Sam Blitz 2, Dime Blitz 2**')
    elif play.lower() == "WR Drag 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **QB Contain*')
    elif play.lower() == "PA Spot 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 1 Contain Spy 4-3**')
    elif play.lower() == "PA Switch Dig".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Silver Shoot 2**')
    elif play.lower() == "PA Slot Crosses".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 3 (first one in 3-4)**')
    elif play.lower() == "Posts".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 3 (first one in 3-4)**')
    elif play.lower() == "X Follow".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **SS Scrape 3, Cov 3 Contain**')
    elif play.lower() == "TE Angle".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Pinch Buck 0, Strong Slant 3**')
    elif play.lower() == "TE Out".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **3 Double Buzz, Mike Dime Blitz**')
    elif play.lower() == "WR Corner".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 4 Drop Zone**')
    elif play.lower() == "Z Spot".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 4 Drop Zone**')
    elif play.lower() == "Hail Mary".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 3 Cloud Wk, Cover 2 Man Dime**')
    elif play.lower() == "Inside Switch 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **4 Buzz Flats**')
    elif play.lower() == "PA Fork 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Dime Blitz 2**')
    elif play.lower() == "Slot Flags".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 2 Dime**')
    elif play.lower() == "Sluggo".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **CB Dogs Man**')
    elif play.lower() == "Seattle".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 6 Press**')
    elif play.lower() == "HB Plunge".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **LB Dogs**')
    elif play.lower() == "01 Trap".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **LB Dogs, Weak Blitz**')
    elif play.lower() == "PA Clearout".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **DBL TE Bracket, Mike Dime Blitz**')
    elif play.lower() == "Spot Opt 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Cover 1 Robber Press Dime**')
    elif play.lower() == "HB Base 2PT".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Thunder Smoke**')
    elif play.lower() == "PA Power O".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **1 DB Blitz**')
    elif play.lower() == "HB Zone".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **4-3 Cover 2 Press**')
    elif play.lower() == "PA Spot".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **4 Buzz Flats, Sam Blitz 2**')
    elif play.lower() == "Blast Alert X Smoke".lower():
        await ctx.send(f'{ctx.message.author.mention}, counter(s): **Pinch Dog 2 Press**')
    else:
        await ctx.send(f'{ctx.message.author.mention}, there are no counters currently inputted for {play}')

    return

@client.command()
async def info(ctx):
    try:
        id = str(ctx.author.id)
        cell = sheetUsers.find(id[:-6])
        name = sheetUsers.cell(cell.row, cell.col-1).value
        locationCell = sheetMain.find(name)
        await ctx.send(f'{ctx.message.author.mention}, '
                       f'\nPower = {sheetMain.cell(locationCell.row, 4).value}'
                       f'\nOffOvr = {sheetMain.cell(locationCell.row, 5).value}'
                       f'\nDefOvr = {sheetMain.cell(locationCell.row, 6).value}'
                       f'\nTop 100 30-Day = {sheetMain.cell(locationCell.row, 8).value}'
                       f'\nTop 100 All-Time = {sheetMain.cell(locationCell.row, 9).value}'
                       f'\n7-Day Average = {sheetMain.cell(locationCell.row, 10).value}'
                       f'\n30-Day Average = {sheetMain.cell(locationCell.row, 11).value}'
                       f'\nAll-Time Average = {sheetMain.cell(locationCell.row, 12).value}')
    except gspread.exceptions.CellNotFound:
        id = str(ctx.author.id)
        cell = sheetABUsers.find(id[:-6])
        name = sheetABUsers.cell(cell.row, cell.col - 1).value
        locationCell = sheetABMain.find(name)
        await ctx.send(f'{ctx.message.author.mention}, '
                       f'\nPower = {sheetABMain.cell(locationCell.row, 4).value}'
                       f'\nOffOvr = {sheetABMain.cell(locationCell.row, 5).value}'
                       f'\nDefOvr = {sheetABMain.cell(locationCell.row, 6).value}'
                       f'\nTop 100 30-Day = {sheetABMain.cell(locationCell.row, 8).value}'
                       f'\nTop 100 All-Time = {sheetABMain.cell(locationCell.row, 9).value}'
                       f'\n7-Day Average = {sheetABMain.cell(locationCell.row, 10).value}'
                       f'\n30-Day Average = {sheetABMain.cell(locationCell.row, 11).value}'
                       f'\nAll-Time Average = {sheetABMain.cell(locationCell.row, 12).value}')
    except gspread.exceptions.CellNotFound:
        await ctx.send(f'{ctx.message.author.mention}, you must first type \'.setup ExactInGameName\' to use this command!')

@client.command()
async def commands(ctx):
    await ctx.send(f'{ctx.message.author.mention}, the available list of commands are:\n'
                   f'**.setupAB(or .setupAP) inGameName** | Example: .setupAB(or .setupAP) Syukaan\n'
                   f'**.updateall power offOvr defOvr** | Example: .updateall 2530 84 85\n'
                   f'**.updatepow power** | Example: .updatepow 2500\n'
                   f'**.updateoff offOvr** | Example: .updateoff 84\n'
                   f'**.updatedef defOvr** | Example: .updatedef 85\n'
                   f'**.rank**\n'
                   f'**.lvlscore score** | Example: .lvlscore 24\n'
                   f'**.pastlvlscore clanName score** | Example: .pastlvlscore "Hellfire Club" 24\n'
                   f'**.counter "play"** | Example: .counter "Hail Mary"\n'
                   f'**.counterlist**\n'
                   f'**.info**\n\n'
                   f'**---- ADMIN COMMANDS BELOW ----**\n\n'
                   f'**.newlvlAB(or .newlvlAP) clanName rank date** | Example: .newlvlAB(or .newlvlAP) "Hellfire Club" 25 9-28\n'
                   f'**.lvlsummaryAB(or .lvlsummaryAP) clanName ourScore oppScore ourRank players ourCompDrives oppCompDrives** | '
                   f'Example: .lvlsummaryAB(or .lvlsummaryAP) DANT 250 200 25 18 52 50')

client.run('NzU5ODA5NjcyNzEwMTkzMTgy.X3C55g.h-AasGwt9He3dbsD8M1-fHyGjfY') #running bot using its token
from time import sleep
import discord
import json
import datetime

from discord.ext import commands
from datetime import datetime, timedelta
from discord import SelectMenu, SelectOption, Button, ButtonStyle

import keep_alive
import functions

intents = discord.Intents.all()
intents.members = True

async def get_prefix(client, message):
	guild = message.guild
	with open("extra.json", "r") as ex:
		data = json.load(ex)
	for i in range(len(data["prefix"])):
		if list(data["prefix"][i].keys())[0] == str(guild.id):
			prefix = data["prefix"][i][str(guild.id)]
			break
	return prefix
	

client = commands.Bot(command_prefix=get_prefix, help_command=None, intents=intents)
#DiscordComponents(client)

@client.event
async def on_ready() :
    time=datetime.now()
    print("------\nBot Connecté\nESGI_Bot\n"+str(client.user.id)+"\nBot lancé le "+str(time.strftime("%d-%m-%Y à %H:%M:%S")+"\n------"))

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="$help"))

@client.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix):
	with open("extra.json", "r") as ex:
		data = json.load(ex)

	for i in range(len(data["prefix"])):
		if list(data["prefix"][i].keys())[0] == str(ctx.guild.id):
			data["prefix"][i][str(ctx.guild.id)] = prefix
			break

	with open("extra.json", "w") as ex:
		json.dump(data, ex)

	await ctx.send(embed=discord.Embed(title=f"Le nouveau préfix est {prefix}"))

@commands.cooldown(1, 2, commands.BucketType.user)
@client.command()
async def help(ctx):
	with open("extra.json", "r") as ex:
		data = json.load(ex)

	for i in range(len(data["prefix"])):
		if list(data["prefix"][i].keys())[0] == str(ctx.message.guild.id):
			prefixe = data["prefix"][i][str(ctx.guild.id)]
			break

	embed = discord.Embed(
	    title="__**Liste des commandes**__",
	    description=f"Prefix du bot = `{prefixe}` \n\n **Gestion Devoirs** (Staff Only) : \n\n`show_homeworks`, `add_homeworks`, `delete_homeworks`, `refresh_homeworks` \n\n *Pour annuler une commande tapez `$cancel`* \n\n **Serveur** (Staff Only) : \n\n`prefix`",
	    colour=5213)
	await ctx.send(embed=embed)

@client.command(aliases=["tableau_devoirs", "sh"])
@commands.has_permissions(manage_guild=True)
async def show_homeworks(ctx, actualize = None):

	if actualize == None:
		await ctx.message.delete()

	global ctx_g
	ctx_g = ctx

	date = datetime.today().strftime("%d/%m/%y")
	day_nb = datetime.strptime(date, "%d/%m/%y").weekday()
	date = datetime.strptime(date, "%d/%m/%y")
	day_monday = (date - timedelta(days=day_nb))

	with open("extra.json", "r") as ex:
		data = json.load(ex)
	day_monday = (day_monday + timedelta(days=data["page"]*7))

	m, t, w, th, f = day_monday.strftime("%d/%m"), (day_monday + timedelta(days=1)).strftime("%d/%m"), (day_monday + timedelta(days=2)).strftime("%d/%m"), (day_monday + timedelta(days=3)).strftime("%d/%m"), (day_monday + timedelta(days=4)).strftime("%d/%m")
	sc = {"1.0" : "🇬🇧 Anglais : Groupe 1", "1.1" : "🇬🇧 Anglais : Groupe 2", "1.2" : "🇬🇧 Anglais : Groupe 3", "1.3" : "🇬🇧 Anglais : Groupe 4", "1.4" : "🇬🇧 Anglais : Groupe 5", "2" : "<:python:1030146564481626233> Algorithme et structure de données ", "3" : "<:reseau:1030143415867949106> Architecture des réseaux", "4" : "<:circuits:1030144701887688804> Circuits logiques et architecture d'un ordinateur", "5" : "<:entreprise:1030147079961595944> Connaissance de l'Entreprise", "6" : "<:excel:1030144814395699292> Développement VBA Excel", "7" : "<:web:1030145124904206487> Développement Web", "8" : "<:langageC:1030145002392789032> Langage C", "9" : "<:linux:1030145431155527680> Linux utilisation avancée", "10" : "<:bdd:1030141546378567791> Modélisation Bases de Données", "11" : "<:ihmicon:1030145867077914675> Modélisation et IHM", "12" : "<:reseaux:1030145569374613574> Réseaux Sociaux et e-Réputation", "13" : "<:job:1030146054802374677> Techniques de recherche d'emploi"}
	with open("homeworks.json", "r") as hw:
		data = json.load(hw)

	hw_text = []
	hw_days = [day_monday.strftime("%d/%m/%Y"), (day_monday + timedelta(days=1)).strftime("%d/%m/%Y"), (day_monday + timedelta(days=2)).strftime("%d/%m/%Y"), (day_monday + timedelta(days=3)).strftime("%d/%m/%Y"), (day_monday + timedelta(days=4)).strftime("%d/%m/%Y")]
	for i in hw_days:
		if i not in data.keys():
			hw_text.append("Pas de devoir pour ce jour là")
		else:
			temp_list = []
			for j in data[i].keys():
				details = "\n➜ ".join(data[i][j])
				temp_list.append(f"**__{sc[j]} :__**\n➜ {details}")
			temp_list = [k for k in temp_list if k[-2:] != "➜ "]
			hw_text.append("\n\n".join(temp_list))

	embed = discord.Embed(
		title = "Devoirs de la 1A4",
		description = f"Pour la semaine du {m} au {f}",
		color = 14614528)
	embed.add_field(name=f"ㅤ\n➽ Lundi {m}", value=hw_text[0], inline=False)
	embed.add_field(name=f"ㅤ\n➽ Mardi {t}", value=hw_text[1], inline=False)
	embed.add_field(name=f"ㅤ\n➽ Mercredi {w}", value=hw_text[2], inline=False)
	embed.add_field(name=f"ㅤ\n➽ Jeudi {th}", value=hw_text[3], inline=False)
	embed.add_field(name=f"ㅤ\n➽ Vendredi {f}", value=hw_text[4], inline=False)
	embed.set_thumbnail(url = "https://imgur.com/lWZeSnu.png")
	embed.set_footer(text="Made by Léo#6774 and Zack adde#9698 (Beautiful Beta-Tester)")

	if actualize == None:
		
		EmbedHomeworks = await ctx.send(embed = embed, components=[[
			Button(label="Semaine précédente",
					custom_id="Before",
					style=ButtonStyle.blurple),
			Button(label="Cette semaine",
					custom_id="Now",
					style=ButtonStyle.green),
			Button(label="Semaine suivante",
					custom_id="After",
					style=ButtonStyle.blurple)]])
		functions.save_mess(EmbedHomeworks.id, EmbedHomeworks.channel.id)
	
	elif actualize == True:

		infos = functions.get_mess()
		channel = client.get_channel(infos[1])
		msg = await channel.fetch_message(infos[0]) 
		await msg.edit(embed = embed, components=[[
			Button(label="Semaine précédente",
					custom_id="Before",
					style=ButtonStyle.blurple),
			Button(label="Cette semaine",
					custom_id="Now",
					style=ButtonStyle.green),
			Button(label="Semaine suivante",
					custom_id="After",
					style=ButtonStyle.blurple)]])
	
@client.command(aliases=["ajouter_devoir", "ah"])
@commands.has_permissions(manage_guild=True)
async def add_homeworks(ctx):
	
	global ctx_g
	ctx_g = ctx
	cancel = False
	msg_with_selects = await ctx.send("Dans quelle matière veux-tu ajouter un devoir ? ", components = [[
			SelectMenu(custom_id = "subjects", options = [
				SelectOption(emoji="🇬🇧", label="Anglais", value="1"),
				SelectOption(emoji="<:python:1030146564481626233>", label="Algo / Structure Données", description="M. Bienvenue", value="2"),
				SelectOption(emoji="<:reseau:1030143415867949106>", label="Architecture des réseaux", description="Mme. Oulmi", value="3"),
				SelectOption(emoji="<:circuits:1030144701887688804>", label="Circuits logiques / Archi", description="M. Neveu", value="4"),
				SelectOption(emoji="<:entreprise:1030147079961595944>", label="Connaisance Entreprise", description="M. Fedida", value="5"),
				SelectOption(emoji="<:excel:1030144814395699292>", label="Développement VBA Excel", description="M. Delon", value="6"),
				SelectOption(emoji="<:web:1030145124904206487>", label="Développement WEB", description="M. Skrzypczyk", value="7"),
				SelectOption(emoji="<:langageC:1030145002392789032>", label="Langage C", description="M. Trancho", value="8"),
				SelectOption(emoji="<:linux:1030145431155527680>", label="Linux utilisation avancé", description="M. Neveu", value="9"),
				SelectOption(emoji="<:bdd:1030141546378567791>", label="Modélisation BDD", description="M. Delon", value="10"),
				SelectOption(emoji="<:ihmicon:1030145867077914675>", label="Modélisation et IHM", description="M. Serval", value="11"),
				SelectOption(emoji="<:reseaux:1030145569374613574>", label="Réseaux Sociaux / e-Répu", description="Mme. Arachtingi", value="12"),
				SelectOption(emoji="<:job:1030146054802374677>", label="Techniques d'emploi", description="Mme. Cramaussel", value="13")],
				placeholder = "Matière", max_values = 1)
	]])
	
	def check_selection(i: discord.Interaction, select_menu):
		return i.author == ctx.author and i.message == msg_with_selects

	interaction, select_menu = await client.wait_for('selection_select', check=check_selection)
	
	if int(select_menu._values[0]) == 1:
		msg_with_selects2 = await interaction.respond("A quel groupe veux-tu ajouter des devoirs ? ", components = [[
			SelectMenu(custom_id = "subjects", options = [
				SelectOption(emoji="🇬🇧", label="Groupe 1", value="1.0"),
				SelectOption(emoji="🇬🇧", label="Groupe 2", value="1.1"),
				SelectOption(emoji="🇬🇧", label="Groupe 3", value="1.2"),
				SelectOption(emoji="🇬🇧", label="Groupe 4", value="1.3"),
				SelectOption(emoji="🇬🇧", label="Groupe 5", value="1.4")],
				placeholder = "Choix du groupe", max_values = 1)
		]])

		def check_selection2(i: discord.Interaction, select_menu):
			return i.author == ctx.author and i.message == msg_with_selects2
		
		interaction, select_menu = await client.wait_for('selection_select', check=check_selection2)
	else:
		msg_with_selects2 = ""

	msg = await interaction.respond("Pour quelle date ? (Sous le format JJ/MM/AAAA)")

	good = False
	while not good:
		date_hw = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout=240)
		if functions.check_date(date_hw.content):
			good = True
		else:
			await msg.edit(content = "Votre date n'est pas correcte, veuillez en redonner une correct (JJ/MM/AAAA)")
	
	if date_hw.content != "$cancel":

		msg_hw = await interaction.respond("Ecrit le devoir à faire : ")

		homework = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout=240)

		if homework.content != "$cancel":

			with open("homeworks.json", "r") as hw:
				data = json.load(hw)

			if not date_hw.content in data.keys():
				data[date_hw.content] = {"1.0": [], "1.1": [], "1.2": [], "1.3": [], "1.4": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": [], "8": [], "9": [], "10": [], "11": [], "12": [], "13": []}
			data[date_hw.content][select_menu._values[0]].append(homework.content)

			with open("homeworks.json", "w") as hw:
				json.dump(data, hw)
		
			await ctx.send(f"✅ Devoir enregistré pour le {date_hw.content} ! ✅")

			await show_homeworks(ctx, True)
		else:
			await ctx.send(":x: Commande annulée ! :x:")
	else:
		await ctx.send(":x: Commande annulée ! :x:")
	
	await msg_hw.delete()
	await msg.delete()
	if msg_with_selects2 != "":
		await msg_with_selects2.delete()
	await msg_with_selects.delete()
	await ctx.message.delete()

@client.command(aliases=["supprimer_devoir", "dh"])
@commands.has_permissions(manage_guild=True)
async def delete_homeworks(ctx):
	
	msg_date = await ctx.send("Pour quelle date souhaitez-vous supprimer un devoir ? (Sous le format JJ/MM/AAAA)")
	
	good = False
	while not good:
		date_hw = await client.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author, timeout=240)
		if functions.check_date(date_hw.content):
			good = True
		else:
			await msg_date.edit(content = "Votre date n'est pas correcte, veuillez en redonner une correct (JJ/MM/AAAA)")

	if date_hw.content != "$cancel":

		with open("homeworks.json", "r") as hw:
			data = json.load(hw)

		if date_hw.content not in data.keys():
			await ctx.send("Pas de devoir pour ce jour là")
		else:
			emotes = {"1.0" : "🇬🇧", "1.1" : "🇬🇧", "1.2" : "🇬🇧", "1.3" : "🇬🇧", "1.4" : "🇬🇧", "2" : "<:python:1030146564481626233>", "3" : "<:reseau:1030143415867949106>", "4" : "<:circuits:1030144701887688804>", "5" : "<:entreprise:1030147079961595944>", "6" : "<:excel:1030144814395699292>", "7" : "<:web:1030145124904206487>", "8" : "<:langageC:1030145002392789032>", "9" : "<:linux:1030145431155527680>", "10" : "<:bdd:1030141546378567791>", "11" : "<:ihmicon:1030145867077914675>", "12" : "<:reseaux:1030145569374613574>", "13" : "<:job:1030146054802374677>", "14" : "🇬🇧", "15" : "🇬🇧", "16" : "🇬🇧", "17" : "🇬🇧", "18" : "🇬🇧"}
			sc = {"1.0" : "🇬🇧 Anglais : Groupe 1", "1.1" : "🇬🇧 Anglais : Groupe 2", "1.2" : "🇬🇧 Anglais : Groupe 3", "1.3" : "🇬🇧 Anglais : Groupe 4", "1.4" : "🇬🇧 Anglais : Groupe 5", "2" : "<:python:1030146564481626233> Algorithme et structure de données ", "3" : "<:reseau:1030143415867949106> Architecture des réseaux", "4" : "<:circuits:1030144701887688804> Circuits logiques et architecture d'un ordinateur", "5" : "<:entreprise:1030147079961595944> Connaissance de l'Entreprise", "6" : "<:excel:1030144814395699292> Développement VBA Excel", "7" : "<:web:1030145124904206487> Développement Web", "8" : "<:langageC:1030145002392789032> Langage C", "9" : "<:linux:1030145431155527680> Linux utilisation avancée", "10" : "<:bdd:1030141546378567791> Modélisation Bases de Données", "11" : "<:ihmicon:1030145867077914675> Modélisation et IHM", "12" : "<:reseaux:1030145569374613574> Réseaux Sociaux et e-Réputation", "13" : "<:job:1030146054802374677> Techniques de recherche d'emploi"}
			sc2 = {"1.0" : "Anglais : Groupe 1", "1.1" : "Anglais : Groupe 2", "1.2" : "Anglais : Groupe 3", "1.3" : "Anglais : Groupe 4", "1.4" : "Anglais : Groupe 5", "2" : "Algo / Structure Données", "3" : "Architecture des réseaux", "4" : "Circuits logiques / Archi", "5" : "Connaisance Entreprise", "6" : "Développement VBA Excel", "7" : "Développement WEB", "8" : "Langage C", "9" : "Linux utilisation avancé", "10" : "Modélisation BDD", "11" : "Modélisation et IHM", "12" : "Réseaux Sociaux / e-Répu", "13" : "Techniques d'emploi", "14" : "Anglais : Groupe 1", "15" : "Anglais : Groupe 2", "16" : "Anglais : Groupe 3", "17" : "Anglais : Groupe 4", "18" : "Anglais : Groupe 5"} 
			
			temp_list = []
			sl = []
			for j in data[date_hw.content].keys():
				if data[date_hw.content][j] != []:
					details = "\n➜ ".join(data[date_hw.content][j])
					temp_list.append(f"**__{sc[j]} :__**\n➜ {details}")
					sl.append(j)
			temp_list = "\n\n".join(temp_list)

			embed = discord.Embed(
				title = "Devoir(s) ce jour là",
				color = 14614528)
			embed.add_field(name=f"ㅤ\n➽ {date_hw.content}", value=temp_list, inline=False)
			embed.set_thumbnail(url = "https://imgur.com/lWZeSnu.png")
			embed.set_footer(text="Made by Léo#6774 and Zack adde#9698 (Beautiful Beta-Tester)")
			
			msg = await ctx.send(embed=embed, components = [[SelectMenu(custom_id = "subjects", options = [SelectOption(emoji=emotes[label], label=sc2[label], value=label) for label in sl], placeholder = "Choix de la matière", max_values = 1)]])

			def check_selection(i: discord.Interaction, select_menu):
				return i.author == ctx.author and i.message == msg

			interaction, select_menu = await client.wait_for('selection_select', check=check_selection)

			hw_list = []
			for i in data[date_hw.content][select_menu._values[0]]:
				hw_list.append("***" + str(len(hw_list)+1) + ")*** " + i)
			hw = "\n".join(hw_list)

			embed = discord.Embed(
				title = f"Devoir pour la matière __**{sc[select_menu._values[0]]}**__",
				color = 14614528)
			embed.add_field(name=f"ㅤ\n➽ Liste des devoirs :\nㅤ", value=hw, inline=False)
			embed.set_thumbnail(url = "https://imgur.com/lWZeSnu.png")
			embed.set_footer(text="Made by Léo#6774 and Zack adde#9698 (Beautiful Beta-Tester)")

			sleep(2)

			await msg.edit(embed=embed, components = [[SelectMenu(custom_id = "subjects", options = [SelectOption(label=f"Devoir Numéro : {str(i+1)}", value=str(i)) for i in range(len(hw_list))], placeholder = "Choix du devoir", max_values = 1)]])

			def check_selection2(i: discord.Interaction, select_menu):
				return i.author == ctx.author and i.message == msg

			interaction, select_menu2 = await client.wait_for('selection_select', check=check_selection2)

			with open("homeworks.json", "r") as hw:
				data = json.load(hw)

			del data[date_hw.content][select_menu._values[0]][int(select_menu2._values[0])]

			hw_for_this_day = False
			for i in list(data[date_hw.content].values()):
				if i != []:
					hw_for_this_day = True
			
			if hw_for_this_day == False:
				del data[date_hw.content]

			with open("homeworks.json", "w") as hw:
				json.dump(data, hw)

			await ctx.message.delete()
			await msg_date.delete()
			await msg.delete()
			await ctx.send(f"✅ Devoir de la matière __**{sc[select_menu._values[0]]}**__ le ***{date_hw.content}*** supprimé ! ✅")

			await show_homeworks(ctx, True)
	else:
		await ctx.message.delete()
		await msg_date.delete()
		await ctx.send(":x: Commande annulée ! :x:")
		
@client.command(aliases = ["actualiser_devoirs", "rh"])
@commands.has_permissions(manage_guild=True)
async def refresh_homeworks(ctx):
	await ctx.message.delete()
	await show_homeworks(ctx, True)

@client.event
async def on_button_click(interaction: discord.Interaction, button):
	global ctx_g
	if button.custom_id == "After":
		with open("extra.json", "r") as ex:
			data = json.load(ex)
		data["page"] += 1
		with open("extra.json", "w") as ex:
			json.dump(data, ex)
	elif button.custom_id == "Now":
		with open("extra.json", "r") as ex:
			data = json.load(ex)
		data["page"] = 0
		with open("extra.json", "w") as ex:
			json.dump(data, ex)
	elif button.custom_id == "Before":
		with open("extra.json", "r") as ex:
			data = json.load(ex)
		data["page"] -= 1
		with open("extra.json", "w") as ex:
			json.dump(data, ex)
	await show_homeworks(ctx_g, True)

@client.event
async def on_guild_join(guild):
	with open("extra.json", "r") as ex:
		try:
			data = json.load(ex)
		except json.decoder.JSONDecodeError:
			data = {"prefix":[]}
	data["prefix"].append({str(guild.id): "$"})
	with open("extra.json", "w") as ex:
		json.dump(data, ex)


@client.event
async def on_command_error(ctx, error):

	if isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour effectuer cette commande !")
		
#keep_alive.keep_alive()

client.run("TOKEN")
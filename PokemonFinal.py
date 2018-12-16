import urllib.parse
import requests 
import json
import sqlite3
import pprint 
import matplotlib.pyplot as plt
import csv 



pokemon_api = "https://pokeapi.co/api/v2/pokemon/"#Pokemon API key
pokemon_api2 = "https://pokeapi.co/api/v2/pokemon/1/"

pokemon_data = requests.get(pokemon_api).json()


def get_data(url):
	x = requests.get(url).json()
	return x 

def get_stats(pokemon_dict):
	stat_dict = {}
	pokemon_stats = pokemon_dict['stats']
	for item in pokemon_stats:
		stat = item['stat']
		stat_num = item['base_stat']
		name = stat['name']
		if name not in stat_dict:
			stat_dict[name] = 0
		stat_dict[name] += stat_num
	return stat_dict

def get_type(pokemon_dict):
	type_dict = pokemon_dict['types'][0]
	poke_type = type_dict['type']['name']
	return poke_type

def get_name(pokemon_dict):
	forms = pokemon_dict['forms'][0]
	name = forms['name']
	return name 

pokemon_url_list = []

for x in range(101):
	p_url = pokemon_api + str(x) + '/'
	pokemon_url_list.append(p_url)
del(pokemon_url_list[0])

conn = sqlite3.connect('pokemon.sqlite')
cur = conn.cursor()


#making data table#
name_list = []
type_list = []
speed_list = []
special_defense_list = [] 
special_attack_list = []
attack_list = []
defense_list = []
hp_list = []
for url in pokemon_url_list:
	data = get_data(url)
	stats = get_stats(data)
	name = get_name(data)
	poke_type = get_type(data)
	name_list.append(name)
	type_list.append(poke_type)
	speed_list.append(stats['speed'])
	special_defense_list.append(stats['special-defense'])
	special_attack_list.append(stats['special-attack'])
	attack_list.append(stats['attack'])
	defense_list.append(stats['defense'])
	hp_list.append(stats['hp'])
cur.execute('DROP TABLE IF EXISTS Pokemon')
cur.execute('CREATE TABLE Pokemon(name TEXT, type TEXT, health INTEGER, speed INTEGER, attack INTEGER, defense INTEGER, special_attack INTEGER, special_defense INTEGER)')
for x in range(len(pokemon_url_list)):
	cur.execute('INSERT INTO Pokemon(name, type, health, speed, attack, defense, special_attack, special_defense) VALUES (?,?,?,?,?,?,?,?)' , (name_list[x], type_list[x], hp_list[x], speed_list[x], attack_list[x], defense_list[x], special_attack_list[x], special_defense_list[x]))
conn.commit()


cursor = cur.execute('SELECT type, name, attack, health FROM Pokemon')

master_dict = {}
for line in cursor:
	p_type = line[0]
	name = line[1]
	attack_data = line[2]
	health_data = line[3]
	if p_type not in master_dict:
		master_dict[p_type] = []
	master_dict[p_type].append((name,attack_data, health_data))
for types in master_dict:
	item = master_dict[types]
	counter_a = 0
	counter_b = 0
	for poke in item:
		if poke[1] > counter_a:
			counter_a = poke[1]
			deadly = poke

	
	master_dict[types] = [deadly]

with open('Pokemon.csv', 'w', newline = '') as csvfile:
	fieldnames = ['Type', 'Name', 'Attack', 'Health']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
	writer.writeheader()
	for item in master_dict:
		writer.writerow({'Type': item, 'Name': master_dict[item][0][0], "Attack":master_dict[item][0][1], "Health":master_dict[item][0][2]})


color_list = ['green', 'red', 'gray', 'blue', 'olive', 'orange', 'yellow', 'saddlebrown', 'pink', 'lawngreen', 'black', 'm', 'lightsteelblue', 'teal']

fig, ax = plt.subplots()
groups = list(master_dict.keys())

test_list = []
for x in master_dict:
	y = master_dict[x][0]
	test_list.append(y)
	poke_names = []
	stats_list = []
	for item in test_list:
		poke_names.append(item[0])
		stats_list.append((item[1], item[2]))


poketup = zip(stats_list, poke_names, color_list, groups)
for z in poketup:
	x,y = z[0]
	name = z[1]
	color = z[2]
	group = z[3]
	ax.scatter(x,y, c = color, s = 50, label = name +":"+ group, alpha = 0.8, edgecolors = 'none')

ax.legend(loc="best", bbox_to_anchor=(0.46, .8),ncol=2,prop={'size': 6})
ax.grid(True)
plt.title('Deadliest Pokemon by Type')
plt.xlabel('Attack')
plt.ylabel('Health')
plt.show()





























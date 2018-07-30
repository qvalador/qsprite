#!/usr/bin/env python
# encoding: utf-8
import requests
import json
from fuzzywuzzy import fuzz, process
from conf import *

BASE_URL = 'http://pokeapi.co'

species_names = []
item_names = []
move_names = []
ability_names = []

colours = {
	'normal': 0xA8A878,
	'fire': 0xEE8130,
	'water': 0x6390F0,
	'electric': 0xF7D02C,
	'grass': 0x7AC74C,
	'ice': 0x96D9D6,
	'fighting': 0xC22E28,
	'poison': 0xA33EA1,
	'ground': 0xE2BF65,
	'flying': 0xA98FF3,
	'psychic': 0xF95587,
	'bug': 0xA6B91A,
	'rock': 0xB6A136,
	'ghost': 0x735797,
	'dragon': 0x6F35FC,
	'dark': 0x705746,
	'steel': 0xB7B7CE,
	'fairy': 0xD685AD,
}

with open(cog_dir + "pokedex/data/pokemon-names.txt") as f:
    species_names = f.read().splitlines()
    
with open(cog_dir + "pokedex/data/item-names.txt") as f:
    item_names = f.read().splitlines()
    
with open(cog_dir + "pokedex/data/move-names.txt") as f:
    move_names = f.read().splitlines()
    
with open(cog_dir + "pokedex/data/ability-names.txt") as f:
    ability_names = f.read().splitlines()
    
def get_query(arg, index):
    indices = {"pokemon": species_names, "item": item_names, "move": move_names, "ability": ability_names}
    return process.extractOne(arg, indices[index])[0]
 
def query_pokeapi(resource_url):
    url = '{0}{1}'.format(BASE_URL, resource_url)
    response = requests.get(url)
 
    if response.status_code == 200:
        return json.loads(response.text)
    return None
    
def item_basic(query):
    query = get_query(query, "item")
    item = query_pokeapi('/api/v2/item/{}/'.format(query))
    
    sprite = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/{}.png".format(query)
    description = item['effect_entries'][0]['short_effect']
    
    response = {"name": item['names'][0]['name'], "sprite": sprite, "description": description}
    return(response)
    
def ability_basic(query):
    query = get_query(query, "ability")
    ability = query_pokeapi('/api/v2/ability/{}/'.format(query))

    description = ability['effect_entries'][0]['short_effect']
    
    response = {"name": ability['names'][0]['name'], "description": description}
    return(response)
    
def move_basic(query):
    query = get_query(query, "move")
    move = query_pokeapi('/api/v2/move/{}/'.format(query))
    
    name = move['names'][0]['name']
    effect_chance = move['effect_chance']
    description = move['effect_entries'][0]['effect'].replace("$effect_chance", str(effect_chance))
    type = move['type']['name']
    colour = colours[type]
    accuracy = "{}%".format(move['accuracy']) if move['accuracy'] else "N/A"
    power = move['power'] if move['power'] else 0
    
    return {"name": name, "description": description, "type": type, "colour": colour, "accuracy": accuracy, "power": power, "effect chance": effect_chance}
    
    
def pokemon_basic(query):
    query = get_query(query, "pokemon")
    pokemon = query_pokeapi('/api/v2/pokemon/{}/'.format(query))
    species = query_pokeapi('/api/v2/pokemon-species/{}/'.format(query))
    
    def get_types(pokemon):
        types = []
        if len(pokemon['types']) > 1:
            types.append(pokemon['types'][1]['type']['name'])
        types.append(pokemon['types'][0]['type']['name'])
        return types
        
    def get_abilities(pokemon):
        abilities = []
        if not pokemon['abilities'][0]['is_hidden']:
            abilities.append(pokemon['abilities'][0]['ability']['name'].replace("-", " "))
        if len(pokemon['abilities']) > 1:
            abilities.append(pokemon['abilities'][1]['ability']['name'].replace("-", " "))
        if len(pokemon['abilities']) > 2:
            abilities.append(pokemon['abilities'][2]['ability']['name'].replace("-", " "))
        if pokemon['abilities'][0]['is_hidden']:
            abilities.append("*{}*".format(pokemon['abilities'][0]['ability']['name'].replace("-", " ")))
        return abilities
            
     
    sprite = "https://veekun.com/dex/media/pokemon/main-sprites/omegaruby-alphasapphire/{}.png".format(pokemon['id'])
    
    infobit = "{} {}".format(
    "<{}>".format("/".join(get_types(pokemon))),
    "[{}]".format("/".join(get_abilities(pokemon))))
    
    description = species['flavor_text_entries'][1]['flavor_text']
    
    colour = colours[get_types(pokemon)[0]]
    
    
    return({"name": pokemon['name'], "infobit": infobit, "description": description, "sprite": sprite, "colour": colour, "stats": {"hp": pokemon['stats'][5]['base_stat'], "attack": pokemon['stats'][4]['base_stat'], "defence": pokemon['stats'][3]['base_stat'], "special attack": pokemon['stats'][2]['base_stat'], "special defence": pokemon['stats'][1]['base_stat'], "speed": pokemon['stats'][0]['base_stat']}})
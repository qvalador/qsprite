import pokedex.lookup
from pokedex.db import connect, tables, util
from urllib.parse import quote

session = connect()

colors = {
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
    'misc': 0xE888C0,
    'medicine': 0xF87840,
    'poké balls': 0xE8b828,
    'tms and hms': 0xA8E848,
    'berries': 0x40C040,
    'mail': 0x28D0C8,
    'battle items': 0x5080E8,
    'key items': 0x9858F0
}

def lookup_thing(query):
    return pokedex.lookup.PokedexLookup(session=session,).lookup(query)

def sanitize(link):
    """sanitize a string to be inserted into a url."""
    return quote(link.lower())

def get_pokemon(obj):
    """return a dict with keys id, name, type, abilities, stats, link, sprite, and color."""
    if not obj.is_default: # if it's an alternate form
        link = '{name}?form={form}'.format( # don't want quote() to catch ? and =
            name = sanitize(obj.species.name),
            form = sanitize(obj.default_form.form_identifier),
        )
        sprite = '{}-{}.png'.format(obj.species.id, obj.default_form.form_identifier.lower())
    else:
        link = sanitize(obj.species.name)
        sprite = '{}.png'.format(obj.species.id)

    stat_names = ["hp", "atk", "def", "spatk", "spdef", "spd"]
    base_stats = [stat.base_stat for stat in obj.stats]
    stats = dict(zip(stat_names, base_stats)) # (x, y) -> {x: y}
    stats["bst"] = sum(base_stats)

    # sumo doesn't have a national dex :<
    if obj.species.id < 722:
        version = 26
    else:
        version = 28

    return {
        "table": "pokemon",
        "id": obj.species.id,
        "name": obj.name,
        "species": obj.species.genus,
        "type": [ptype.name for ptype in obj.types],
        "flavor": util.get(session, tables.PokemonSpeciesFlavorText, id=(obj.species.id,version,9)).flavor_text.replace('\n', ' '),
        "abilities": [ability.name for ability in obj.abilities],
        "hidden": obj.hidden_ability.name if obj.hidden_ability else None,
        "stats": stats,
        "link": 'https://veekun.com/dex/pokemon/' + link,
        "party": 'https://veekun.com/dex/media/pokemon/icons/' + sprite,
        "sprite": 'https://veekun.com/dex/media/pokemon/main-sprites/ultra-sun-ultra-moon/' + sprite,
        "color": colors[obj.types[0].name.lower()]
        }

def get_item(obj):
    """return a dict with keys name, effect, link, color, and sprite."""
    if obj.pocket.name == "TMs and HMs":
        sprite_name = 'tm-normal'
    else:
        sprite_name = sanitize(obj.name).replace('%20', '-')
    return {
            "table": "item",
            "name": obj.name,
            "effect": obj.short_effect.as_text(),
            "link": 'https://veekun.com/dex/items/' + sanitize(obj.name),
            "color": colors[obj.pocket.name.lower()],
            "sprite": "https://veekun.com/dex/media/items/{}.png".format(sprite_name)
        }

def get_move(obj):
    """return a dict with keys name, type, damage class, power, accuracy, pp, effect, link, sprite, and color."""
    return {
        "table": "move",
        "name": obj.name,
        "type": obj.type.name,
        "damage class": obj.damage_class.name,
        "power": obj.power,
        "accuracy": obj.accuracy,
        "pp": obj.pp,
        "effect": obj.short_effect.as_text(),
        "link": 'https://veekun.com/dex/moves/' + sanitize(obj.name),
        "sprite": 'https://veekun.com/dex/media/items/' + "tm-{}.png".format(obj.type.name.lower()),
        "color": colors[obj.type.name.lower()]
        }

def get_ability(obj):
    """return a dict with keys name, effect, and link."""
    return {
            "table": "ability",
            "name": obj.name,
            "effect": obj.short_effect.as_text(),
            "link": 'https://veekun.com/dex/abilities/' + sanitize(obj.name)
        }

def get_nature(obj):
    """return a dict with keys name, up, down, and link."""
    up = obj.increased_stat.name
    down = obj.decreased_stat.name
    if up == down:
        up = None
        down = None
    return {
            "table": "nature",
            "name": obj.name,
            "up": up,
            "down": down,
            "link": 'https://veekun.com/dex/natures/' + sanitize(obj.name)
        }

def get_thing(query):
    if not query:
        return False
    obj = query[0]
    
    if isinstance(obj, tables.PokemonForm):
        obj = obj.pokemon
    elif isinstance(obj, tables.PokemonSpecies):
        obj = obj.default_pokemon

    cases = {tables.Pokemon: get_pokemon, tables.Item: get_item, tables.Move: get_move, tables.Ability: get_ability, tables.Nature: get_nature}
    for item in cases:
        if isinstance(obj, item):
            result = cases[item](obj)
    return result
       
if __name__ == "__main__":
    print(get_thing(lookup_thing(input('What do you want to lookup?\n> '))))
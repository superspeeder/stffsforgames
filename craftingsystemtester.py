class Recipe:
    def __init__(self, result, result_count, ingredients):
        self.ingredients, self.result = ingredients, result
        self.result_count = result_count

    def canCraft(self, inventory):
        for item, count in self.ingredients.items():
            if item in inventory:
                if not count <= inventory[item]:
                    return (False, ("notenough.item", item, count - inventory[item]))
            else:
                return (False, ("missing.item", item))


# Returns inventory
def craft(inventory, recipe):
    can_craft = recipe.canCraft(inventory)
    if not can_craft[0]:
        if can_craft[1][0] == "notenough.item":
            print("Not Enough {i}, You need {x} more".format(i=can_craft[1][1], x=can_craft[1][2]))
            return inventory
        elif can_craft[1][0] == "missing.item":
            print("You hav no {i}".format(i=can_craft[1][1]))
            return inventory

    for item, count in recipe.ingredients:
        inventory[item] = inventory[item] - count
        if inventory[item] == 0:
            del inventory[item]

    if recipe.result in inventory:
        inventory[recipe.result] = inventory[recipe.result] + recipe.result_count

    else:
        inventory[recipe.result] = recipe.result_count

    return inventory



def loadMaterials(data):
    materials = {}

    for line in data.splitlines():
        id_, name = line.split("=")
        materials[id_] = name

    return materials

def convertMaterialListToItemList(materiallist):
    # ItemListFormat: {id:{"name":name,"properties":properties}}
    items = {}

    for id, name in materiallist.items():
        items[id] = {"name":name, "properties":{}}

    return items




with open("materials.txt", "r") as materialfile:
    mat = loadMaterials(materialfile.read())

items = convertMaterialListToItemList(mat)

recipes = {} # name : recipe

inventory = {}

def runText():
    action = None
    while action != "exit":
        input_act = input("> ")
        if input_act == "exit":
            action = "exit"


        acts = input_act.split(" ")
        if acts[0] == "craft":
            inventory = craft(inventory, acts[1])
        if acts[0][0] == "/":
            command = acts[0][1:]
            if command == "giveme":
                if acts[1] in inventory:
                    inventory[acts[1]] = inventory[acts[1]] + int(acts[2])
                else:
                    inventory[acts[1]] = int(acts[2])

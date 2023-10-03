import pandas as pd


class Product:
    def __init__(self, name, price, volume, fat, category,
                 muscle=0, lung=0, liver=0, kidney=0, spleen=0, heart=0,
                 fish=0, pansen=0, rfk=0, vegetable=0, fruit=0, inventory=0):
        self.name = name
        self.price = price
        self.volume = volume
        self.fat = fat
        self.category = category
        self.inventory = inventory
        self.muscle = muscle
        self.fish = fish
        self.liver = liver
        self.lung = lung
        self.kidney = kidney
        self.spleen = spleen
        self.heart = heart
        self.pansen = pansen
        self.rfk = rfk
        self.vegetable = vegetable
        self.fruit = fruit
        self.price_per_kg = self.calc_price_per_kg()
        self.composition = {
            'Muscle': muscle + fish,
            'Intestinals': liver + lung + kidney + spleen + heart,
            'Pansen': pansen,
            'RFK': rfk,
            'Vegetable': vegetable,
            'Fruit': fruit
        }

    def calc_price_per_kg(self):
        return round((self.price / self.volume) * 1000, 2)


def process_products(products, comp):
    df = pd.DataFrame({
        'Name': [p.name for p in products], 'Category': [p.category for p in products],
        'Inventory': [p.inventory for p in products],
        'Price [€/kg]': [p.price_per_kg for p in products], 'Price': [p.price for p in products],
        'Volume': [p.volume for p in products], 'Fat': [p.fat for p in products]
    })

    cont_comp = pd.DataFrame([[c, p.name, p.composition[c]]
                             for c in comp.index for p in products], columns=['Component', 'Name', 'Share'])

    a = []
    for p in products:
        a.append(['Liver', p.name, p.liver])
        a.append(['Heart', p.name, p.heart])
        a.append(['Kidney', p.name, p.kidney])
        a.append(['Spleen', p.name, p.spleen])
    int_comp = pd.DataFrame(a)

    return df, cont_comp, int_comp


def check_components(df):
    assert df['Share'].sum() == 2, 'Components do not add up to 100%'


def calc_demand(mod, comp, weeklydemand):
    share = pd.DataFrame([
        ['Muscle', mod['Meat']],
        ['Intestinals', mod['Meat']],
        ['Pansen', mod['Meat']],
        ['RFK', mod['Meat']],
        ['Vegetable', mod['Veg & Fruit']],
        ['Fruit', mod['Veg & Fruit']]
    ], columns=['Component', 'Share']).set_index('Component')

    comp_pie = share * comp
    demand = comp_pie * weeklydemand

    return comp_pie, demand


# inventory
def add_inventory(df, product, inventory):
    assert df['Name'].isin([product]).any(), f'{product} not in DataFrame'
    df.loc[df['Name'] == product, 'Inventory'] = inventory

# constants.py

# Define the allowed units for each entity type
entity_unit_map = {
    'width': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'depth': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'height': {'centimetre', 'foot', 'inch', 'metre', 'millimetre', 'yard'},
    'item_weight': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'maximum_weight_recommendation': {'gram', 'kilogram', 'microgram', 'milligram', 'ounce', 'pound', 'ton'},
    'voltage': {'kilovolt', 'millivolt', 'volt'},
    'wattage': {'kilowatt', 'watt'},
    'item_volume': {'centilitre', 'cubic foot', 'cubic inch', 'cup', 'decilitre', 'fluid ounce', 'gallon', 'imperial gallon', 'litre', 'microlitre', 'millilitre', 'pint', 'quart'}
}

# Create a set of all allowed units for quick lookups
allowed_units = {unit for units in entity_unit_map.values() for unit in units}

# Optional: Define unit conversion rates if needed for later use
unit_conversion_rates = {
    'gram': 1,
    'kilogram': 1000,
    'microgram': 0.001,
    'milligram': 0.001,
    'ounce': 28.3495,
    'pound': 453.592,
    'ton': 1000000,
    'centimetre': 0.01,
    'foot': 0.3048,
    'inch': 0.0254,
    'metre': 1,
    'millimetre': 0.001,
    'yard': 0.9144,
    'kilovolt': 1000,
    'millivolt': 0.001,
    'volt': 1,
    'kilowatt': 1000,
    'watt': 1,
    'centilitre': 0.01,
    'cubic foot': 0.3048 ** 3,
    'cubic inch': 0.0254 ** 3,
    'cup': 0.236588,
    'decilitre': 0.1,
    'fluid ounce': 0.0295735,
    'gallon': 3.78541,
    'imperial gallon': 4.54609,
    'litre': 1,
    'microlitre': 1e-6,
    'millilitre': 1e-3,
    'pint': 0.473176,
    'quart': 0.946353
}

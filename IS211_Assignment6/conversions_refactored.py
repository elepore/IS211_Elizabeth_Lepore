
class ConversionNotPossible(Exception):
    pass

def convert(fromUnit, toUnit, value):

    temperature_conversions = {
        ("Celsius", "Kelvin"): lambda c: c + 273.15,
        ("Celsius", "Fahrenheit"): lambda c: (c * 9/5) + 32,
        ("Kelvin", "Celsius"): lambda k: k - 273.15,
        ("Kelvin", "Fahrenheit"): lambda k: (k - 273.15) * 9/5 + 32,
        ("Fahrenheit", "Celsius"): lambda f: (f - 32) * 5/9,
        ("Fahrenheit", "Kelvin"): lambda f: (f - 32) * 5/9 + 273.15,
        ("Fahrenheit", "Fahrenheit"): lambda f: f,
        ("Kelvin", "Kelvin"): lambda f: f,
        ("Celsius", "Celsius"): lambda f: f
    }
    
    distance_conversions = {
        ("Miles", "Yards"): lambda m: m * 1760,
        ("Miles", "Meters"): lambda m: m * 1609.34,
        ("Yards", "Miles"): lambda y: y / 1760,
        ("Yards", "Meters"): lambda y: y * 0.9144,
        ("Meters", "Miles"): lambda m: m / 1609.34,
        ("Meters", "Yards"): lambda m: m / 0.9144,
        ("Meters", "Meters"): lambda m: m, 
        ("Yards", "Yards"): lambda m: m,
        ("Miles", "Miles"): lambda m: m 
    }

    all_conversions = {**temperature_conversions, **distance_conversions}
    conversion_func = all_conversions.get((fromUnit, toUnit))
    if conversion_func:
        return conversion_func(value)
    else:
        raise ConversionNotPossible(f"Conversion from {fromUnit} to {toUnit} is not possible.")

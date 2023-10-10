def convertCelsiusToKelvin(celsius):
    kelvins = celsius + 273.15
    return kelvins

def convertCelsiusToFahrenheit(celsius):
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

def convertFahrenheitToCelsius(fahrenheit):
    celsius = (fahrenheit - 32) * 5/9
    return celsius

def convertFahrenheitToKelvin(fahrenheit):
    kelvins = (fahrenheit + 459.67) * 5/9
    return kelvins

def convertKelvinToCelsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

def convertKelvinToFahrenheit(kelvin):
    fahrenheit = (kelvin * 9/5) - 459.67
    return fahrenheit
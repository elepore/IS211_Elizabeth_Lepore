from conversions import (convertCelsiusToKelvin, convertCelsiusToFahrenheit, 
                         convertKelvinToCelsius, convertKelvinToFahrenheit,
                         convertFahrenheitToKelvin, convertFahrenheitToCelsius)
from conversions_refactored import convert, ConversionNotPossible

def print_and_assert(test, result, expected, places):
    print(f"Test: {test}, Expected: {expected}, Got: {result}")
    assert round(result, places) == round(expected, places), f"Assertion Error: {test}"

def test_temperature_conversions():
    print_and_assert('Celsius To Kelvin specific function', convertCelsiusToKelvin(0), 273.15, places=2)
    print_and_assert('Celsius To Kelvin specific function', convertCelsiusToKelvin(100), 373.15, places=2)
    print_and_assert('Celsius To Kelvin specific function', convertCelsiusToKelvin(-273.15), 0, places=2)
    print_and_assert('Celsius To Kelvin specific function', convertCelsiusToKelvin(24), 297.15, places=2)
    print_and_assert('Celsius To Kelvin specific function', convertCelsiusToKelvin(-324), -50.85, places=2)

    print_and_assert('Celsius To Fahrenheit specific function', convertCelsiusToFahrenheit(0), 32, places=2)
    print_and_assert('Celsius To Fahrenheit specific function',convertCelsiusToFahrenheit(100), 212, places=2)
    print_and_assert('Celsius To Fahrenheit specific function',convertCelsiusToFahrenheit(-40), -40, places=2)
    print_and_assert('Celsius To Fahrenheit specific function',convertCelsiusToFahrenheit(213), 415.4, places=2)
    print_and_assert('Celsius To Fahrenheit specific function',convertCelsiusToFahrenheit(-392), -673.6, places=2)

    print_and_assert('Kelvin To Celsius specific function', convertKelvinToCelsius(273.15), 0, places=2)
    print_and_assert('Kelvin To Celsius specific function', convertKelvinToCelsius(373.15), 100, places=2)
    print_and_assert('Kelvin To Celsius specific function', convertKelvinToCelsius(0), -273.15, places=2)
    print_and_assert('Kelvin To Celsius specific function', convertKelvinToCelsius(213), -60.15, places=2)
    print_and_assert('Kelvin To Celsius specific function', convertKelvinToCelsius(123), -150.15, places=2)

    print_and_assert('Kelvin To Fahrenheit specific function', convertKelvinToFahrenheit(273.15), 32, places=2)
    print_and_assert('Kelvin To Fahrenheit specific function', convertKelvinToFahrenheit(373.15), 212, places=2)
    print_and_assert('Kelvin To Fahrenheit specific function', convertKelvinToFahrenheit(0), -459.67, places=2)
    print_and_assert('Kelvin To Fahrenheit specific function', convertKelvinToFahrenheit(34), -398.47, places=2)
    print_and_assert('Kelvin To Fahrenheit specific function', convertKelvinToFahrenheit(-214), -844.87, places=2)

    print_and_assert('Fahrenheit To Kelvin specific function', convertFahrenheitToKelvin(32), 273.15, places=2)
    print_and_assert('Fahrenheit To Kelvin specific function',convertFahrenheitToKelvin(212), 373.15, places=2)
    print_and_assert('Fahrenheit To Kelvin specific function', convertFahrenheitToKelvin(-459.67), 0, places=2)
    print_and_assert('Fahrenheit To Kelvin specific function', convertFahrenheitToKelvin(324), 435.37, places=2)
    print_and_assert('Fahrenheit To Kelvin specific function', convertFahrenheitToKelvin(-324), 75.37, places=2)

    print_and_assert('Fahrenheit To Celsius specific function', convertFahrenheitToCelsius(32), 0, places=2)
    print_and_assert('Fahrenheit To Celsius specific function', convertFahrenheitToCelsius(212), 100, places=2)
    print_and_assert('Fahrenheit To Celsius specific function', convertFahrenheitToCelsius(-40), -40, places=2)
    print_and_assert('Fahrenheit To Celsius specific function', convertFahrenheitToCelsius(-123), -86.11, places=2)
    print_and_assert('Fahrenheit To Celsius specific function', convertFahrenheitToCelsius(231), 110.56, places=2)

def test_temperature_conversions_refactored():
    print_and_assert('Celsius to Kelvin general function', convert("Celsius", "Kelvin", 0), 273.15, places=2)
    print_and_assert('Celsius to Fahrenheit general function', convert("Celsius", "Fahrenheit", 100), 212, places=2)
    print_and_assert('Kelvin to Fahrenheit general function', convert("Kelvin", "Fahrenheit", 0), -459.67, places=2)
    print_and_assert('Fahrenheit to Celsius general function', convert("Fahrenheit", "Celsius", 32), 0, places=2)
    print_and_assert('Fahrenheit to Kelvin general function', convert("Fahrenheit", "Kelvin", 25), 269.26, places=2)
    print_and_assert('Fahrenheit to Fahrenheit general function', convert("Fahrenheit", "Fahrenheit", 25), 25, places=2)
    print_and_assert('Kelvin to Kelvin general function', convert("Kelvin", "Kelvin", 25), 25, places=2)
    print_and_assert('Celsius to Celsius general function', convert("Celsius", "Celsius", 25), 25, places=2)

def test_distance_conversions_refactored():
    print_and_assert('Miles to Yards general function', convert("Miles", "Yards", 1), 1760, places=2)
    print_and_assert('Yards to Meters general function', convert("Yards", "Meters", 1760), 1609.34, places=2)
    print_and_assert('Meters to Miles general function', convert("Meters", "Miles", 1609.34), 1, places=2)
    print_and_assert('Yards to Miles general function', convert("Yards", "Miles", 2000), 1.14, places=2)
    print_and_assert('Meters to Yards general function', convert("Meters", "Yards", 304), 332.46, places=2)
    print_and_assert('Yards to Yards general function', convert("Yards", "Yards", 304), 304, places=2)
    print_and_assert('Meters to Meters general function', convert("Meters", "Meters", 304), 304, places=2)
    print_and_assert('Miles to Miles general function', convert("Miles", "Miles", 304), 304, places=2)

def test_invalid_conversions():
    convert("Celsius", "Miles", 100)
    convert("Meters", "Kelvin", 1000)

if __name__ == '__main__':
    test_temperature_conversions()
    test_temperature_conversions_refactored()
    test_distance_conversions_refactored()
    test_invalid_conversions()

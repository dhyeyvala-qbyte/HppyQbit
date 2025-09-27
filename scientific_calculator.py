import math

class ScientificCalculator:
    def __init__(self):
        self.memory = 0
        self.angle_mode = "degrees"  # or "radians" 
        
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
    
    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero!")
        return x / y
    
    def power(self, x, y):
        return x ** y
    
    def square_root(self, x):
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number!")
        return math.sqrt(x)
    
    def cube_root(self, x):
        if x >= 0:
            return x ** (1/3)
        else:
            return -((-x) ** (1/3))
    
    def factorial(self, x):
        if x < 0 or x != int(x):
            raise ValueError("Factorial only defined for non-negative integers!")
        return math.factorial(int(x))
    
    def percentage(self, x, y):
        """Calculate x% of y"""
        return (x / 100) * y
    
    # Trigonometric functions
    def _to_radians(self, angle):
        if self.angle_mode == "degrees":
            return math.radians(angle)
        return angle
    
    def _from_radians(self, result):
        if self.angle_mode == "degrees":
            return math.degrees(result)
        return result
    
    def sin(self, x):
        return math.sin(self._to_radians(x))
    
    def cos(self, x):
        return math.cos(self._to_radians(x))
    
    def tan(self, x):
        rad = self._to_radians(x)
        if math.cos(rad) == 0:
            raise ValueError("Tangent undefined at this angle!")
        return math.tan(rad)
    
    def asin(self, x):
        if x < -1 or x > 1:
            raise ValueError("Arcsine domain error: input must be between -1 and 1")
        return self._from_radians(math.asin(x))
    
    def acos(self, x):
        if x < -1 or x > 1:
            raise ValueError("Arccosine domain error: input must be between -1 and 1")
        return self._from_radians(math.acos(x))
    
    def atan(self, x):
        return self._from_radians(math.atan(x))
    
    # Hyperbolic functions
    def sinh(self, x):
        return math.sinh(x)
    
    def cosh(self, x):
        return math.cosh(x)
    
    def tanh(self, x):
        return math.tanh(x)
    
    # Logarithmic functions
    def log(self, x, base=10):
        if x <= 0:
            raise ValueError("Logarithm undefined for non-positive numbers!")
        if base <= 0 or base == 1:
            raise ValueError("Invalid logarithm base!")
        return math.log(x, base)
    
    def ln(self, x):
        if x <= 0:
            raise ValueError("Natural logarithm undefined for non-positive numbers!")
        return math.log(x)
    
    def log10(self, x):
        if x <= 0:
            raise ValueError("Log base 10 undefined for non-positive numbers!")
        return math.log10(x)
    
    def log2(self, x):
        if x <= 0:
            raise ValueError("Log base 2 undefined for non-positive numbers!")
        return math.log2(x)
    
    # Exponential functions
    def exp(self, x):
        return math.exp(x)
    
    def exp10(self, x):
        return 10 ** x
    
    def exp2(self, x):
        return 2 ** x
    
    # Other mathematical functions
    def abs_value(self, x):
        return abs(x)
    
    def floor(self, x):
        return math.floor(x)
    
    def ceil(self, x):
        return math.ceil(x)
    
    def round_num(self, x, decimals=0):
        return round(x, decimals)
    
    def modulo(self, x, y):
        if y == 0:
            raise ValueError("Cannot calculate modulo with zero!")
        return x % y
    
    def gcd(self, x, y):
        return math.gcd(int(x), int(y))
    
    def lcm(self, x, y):
        return abs(int(x) * int(y)) // self.gcd(x, y)
    
    # Constants
    def pi(self):
        return math.pi
    
    def e(self):
        return math.e
    
    def tau(self):
        return math.tau
    
    # Memory functions
    def memory_store(self, value):
        self.memory = value
        return f"Stored {value} in memory"
    
    def memory_recall(self):
        return self.memory
    
    def memory_clear(self):
        self.memory = 0
        return "Memory cleared"
    
    def memory_add(self, value):
        self.memory += value
        return f"Added {value} to memory. Memory now: {self.memory}"
    
    def memory_subtract(self, value):
        self.memory -= value
        return f"Subtracted {value} from memory. Memory now: {self.memory}"
    
    # Angle mode functions
    def set_degrees(self):
        self.angle_mode = "degrees"
        return "Angle mode set to degrees"
    
    def set_radians(self):
        self.angle_mode = "radians"
        return "Angle mode set to radians"
    
    def get_angle_mode(self):
        return self.angle_mode


def display_menu():
    print("\n" + "="*60)
    print("          SCIENTIFIC CALCULATOR")
    print("="*60)
    print("Basic Operations:")
    print("  1. Addition (+)        2. Subtraction (-)     3. Multiplication (*)")
    print("  4. Division (/)        5. Power (**)          6. Square Root (√)")
    print("  7. Cube Root (∛)       8. Factorial (!)       9. Percentage (%)")
    print("  10. Modulo (%)         11. Absolute Value")
    print("\nTrigonometric Functions:")
    print("  12. sin                13. cos                14. tan")
    print("  15. asin               16. acos               17. atan")
    print("  18. sinh               19. cosh               20. tanh")
    print("\nLogarithmic Functions:")
    print("  21. log (base 10)      22. ln (natural log)   23. log (custom base)")
    print("  24. log2 (base 2)")
    print("\nExponential Functions:")
    print("  25. e^x                26. 10^x               27. 2^x")
    print("\nOther Functions:")
    print("  28. Floor              29. Ceiling            30. Round")
    print("  31. GCD                32. LCM")
    print("\nConstants:")
    print("  33. π (pi)             34. e                  35. τ (tau)")
    print("\nMemory Functions:")
    print("  36. Store (MS)         37. Recall (MR)        38. Clear (MC)")
    print("  39. Add to Memory      40. Subtract from Memory")
    print("\nSettings:")
    print("  41. Set Degrees        42. Set Radians        43. Check Angle Mode")
    print("\n  0. Exit")
    print("="*60)


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a valid number.")


def main():
    calc = ScientificCalculator()
    
    print("Welcome to the Scientific Calculator!")
    
    while True:
        display_menu()
        
        try:
            choice = int(input("\nEnter your choice (0-43): "))
            
            if choice == 0:
                print("Thank you for using the Scientific Calculator!")
                break
                
            elif choice == 1:  # Addition
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                print(f"Result: {x} + {y} = {calc.add(x, y)}")
                
            elif choice == 2:  # Subtraction
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                print(f"Result: {x} - {y} = {calc.subtract(x, y)}")
                
            elif choice == 3:  # Multiplication
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                print(f"Result: {x} × {y} = {calc.multiply(x, y)}")
                
            elif choice == 4:  # Division
                x = get_number("Enter dividend: ")
                y = get_number("Enter divisor: ")
                try:
                    print(f"Result: {x} ÷ {y} = {calc.divide(x, y)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 5:  # Power
                x = get_number("Enter base: ")
                y = get_number("Enter exponent: ")
                print(f"Result: {x}^{y} = {calc.power(x, y)}")
                
            elif choice == 6:  # Square Root
                x = get_number("Enter number: ")
                try:
                    print(f"Result: √{x} = {calc.square_root(x)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 7:  # Cube Root
                x = get_number("Enter number: ")
                print(f"Result: ∛{x} = {calc.cube_root(x)}")
                
            elif choice == 8:  # Factorial
                x = get_number("Enter number: ")
                try:
                    print(f"Result: {int(x)}! = {calc.factorial(x)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 9:  # Percentage
                x = get_number("Enter percentage: ")
                y = get_number("Enter number: ")
                print(f"Result: {x}% of {y} = {calc.percentage(x, y)}")
                
            elif choice == 10:  # Modulo
                x = get_number("Enter dividend: ")
                y = get_number("Enter divisor: ")
                try:
                    print(f"Result: {x} mod {y} = {calc.modulo(x, y)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 11:  # Absolute Value
                x = get_number("Enter number: ")
                print(f"Result: |{x}| = {calc.abs_value(x)}")
                
            elif choice == 12:  # sin
                x = get_number(f"Enter angle in {calc.angle_mode}: ")
                print(f"Result: sin({x}) = {calc.sin(x)}")
                
            elif choice == 13:  # cos
                x = get_number(f"Enter angle in {calc.angle_mode}: ")
                print(f"Result: cos({x}) = {calc.cos(x)}")
                
            elif choice == 14:  # tan
                x = get_number(f"Enter angle in {calc.angle_mode}: ")
                try:
                    print(f"Result: tan({x}) = {calc.tan(x)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 15:  # asin
                x = get_number("Enter value (-1 to 1): ")
                try:
                    print(f"Result: arcsin({x}) = {calc.asin(x)} {calc.angle_mode}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 16:  # acos
                x = get_number("Enter value (-1 to 1): ")
                try:
                    print(f"Result: arccos({x}) = {calc.acos(x)} {calc.angle_mode}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 17:  # atan
                x = get_number("Enter value: ")
                print(f"Result: arctan({x}) = {calc.atan(x)} {calc.angle_mode}")
                
            elif choice == 18:  # sinh
                x = get_number("Enter value: ")
                print(f"Result: sinh({x}) = {calc.sinh(x)}")
                
            elif choice == 19:  # cosh
                x = get_number("Enter value: ")
                print(f"Result: cosh({x}) = {calc.cosh(x)}")
                
            elif choice == 20:  # tanh
                x = get_number("Enter value: ")
                print(f"Result: tanh({x}) = {calc.tanh(x)}")
                
            elif choice == 21:  # log base 10
                x = get_number("Enter number: ")
                try:
                    print(f"Result: log₁₀({x}) = {calc.log10(x)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 22:  # ln
                x = get_number("Enter number: ")
                try:
                    print(f"Result: ln({x}) = {calc.ln(x)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 23:  # log custom base
                x = get_number("Enter number: ")
                base = get_number("Enter base: ")
                try:
                    print(f"Result: log₍{base}₎({x}) = {calc.log(x, base)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 24:  # log base 2
                x = get_number("Enter number: ")
                try:
                    print(f"Result: log₂({x}) = {calc.log2(x)}")
                except ValueError as e:
                    print(f"Error: {e}")
                    
            elif choice == 25:  # e^x
                x = get_number("Enter exponent: ")
                print(f"Result: e^{x} = {calc.exp(x)}")
                
            elif choice == 26:  # 10^x
                x = get_number("Enter exponent: ")
                print(f"Result: 10^{x} = {calc.exp10(x)}")
                
            elif choice == 27:  # 2^x
                x = get_number("Enter exponent: ")
                print(f"Result: 2^{x} = {calc.exp2(x)}")
                
            elif choice == 28:  # Floor
                x = get_number("Enter number: ")
                print(f"Result: floor({x}) = {calc.floor(x)}")
                
            elif choice == 29:  # Ceiling
                x = get_number("Enter number: ")
                print(f"Result: ceil({x}) = {calc.ceil(x)}")
                
            elif choice == 30:  # Round
                x = get_number("Enter number: ")
                decimals = int(get_number("Enter decimal places: "))
                print(f"Result: round({x}, {decimals}) = {calc.round_num(x, decimals)}")
                
            elif choice == 31:  # GCD
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                print(f"Result: GCD({int(x)}, {int(y)}) = {calc.gcd(x, y)}")
                
            elif choice == 32:  # LCM
                x = get_number("Enter first number: ")
                y = get_number("Enter second number: ")
                print(f"Result: LCM({int(x)}, {int(y)}) = {calc.lcm(x, y)}")
                
            elif choice == 33:  # π
                print(f"π = {calc.pi()}")
                
            elif choice == 34:  # e
                print(f"e = {calc.e()}")
                
            elif choice == 35:  # τ
                print(f"τ = {calc.tau()}")
                
            elif choice == 36:  # Memory Store
                value = get_number("Enter value to store: ")
                print(calc.memory_store(value))
                
            elif choice == 37:  # Memory Recall
                print(f"Memory: {calc.memory_recall()}")
                
            elif choice == 38:  # Memory Clear
                print(calc.memory_clear())
                
            elif choice == 39:  # Memory Add
                value = get_number("Enter value to add to memory: ")
                print(calc.memory_add(value))
                
            elif choice == 40:  # Memory Subtract
                value = get_number("Enter value to subtract from memory: ")
                print(calc.memory_subtract(value))
                
            elif choice == 41:  # Set Degrees
                print(calc.set_degrees())
                
            elif choice == 42:  # Set Radians
                print(calc.set_radians())
                
            elif choice == 43:  # Check Angle Mode
                print(f"Current angle mode: {calc.get_angle_mode()}")
                
            else:
                print("Invalid choice! Please select a number from 0-43.")
                
        except ValueError:
            print("Invalid input! Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
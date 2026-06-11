"""
Simple Calculator Module

This module provides basic arithmetic operations and a Calculator class
that maintains a running total.
"""


class Calculator:
    """A simple calculator that maintains a running total."""
    
    def __init__(self):
        """Initialize calculator with zero total."""
        self.total = 0
        self.history = []
    
    def add(self, number):
        """Add a number to the total.
        
        Args:
            number: The number to add
            
        Returns:
            The new total
        """
        self.total += number
        self.history.append(f"+ {number}")
        return self.total
    
    def subtract(self, number):
        """Subtract a number from the total.
        
        Args:
            number: The number to subtract
            
        Returns:
            The new total
        """
        self.total -= number
        self.history.append(f"- {number}")
        return self.total
    
    def multiply(self, number):
        """Multiply the total by a number.
        
        Args:
            number: The multiplier
            
        Returns:
            The new total
        """
        self.total *= number
        self.history.append(f"* {number}")
        return self.total
    
    def divide(self, number):
        """Divide the total by a number.
        
        Args:
            number: The divisor (must not be zero)
            
        Returns:
            The new total
            
        Raises:
            ValueError: If number is zero
        """
        if number == 0:
            raise ValueError("Cannot divide by zero")
        
        self.total /= number
        self.history.append(f"/ {number}")
        return self.total
    
    def clear(self):
        """Reset the calculator to zero."""
        self.total = 0
        self.history.clear()
        return self.total
    
    def get_history(self):
        """Get the calculation history.
        
        Returns:
            List of operations performed
        """
        return self.history.copy()
    
    def __str__(self):
        """Return string representation."""
        return f"Calculator(total={self.total})"


def add_numbers(a, b):
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def subtract_numbers(a, b):
    """Subtract b from a.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Difference of a and b
    """
    return a - b


def multiply_numbers(a, b):
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b


def divide_numbers(a, b):
    """Divide a by b.
    
    Args:
        a: Numerator
        b: Denominator (must not be zero)
        
    Returns:
        Quotient of a and b
        
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate_expression(expression):
    """Evaluate a mathematical expression.
    
    Args:
        expression: String containing mathematical expression
        
    Returns:
        Result of the expression
        
    Examples:
        >>> calculate_expression("2 + 3")
        5.0
        >>> calculate_expression("10 * 2")
        20.0
    """
    # Simple implementation - in real code, use a proper parser
    try:
        result = eval(expression)  # Note: eval() is dangerous in production!
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {expression}") from e


if __name__ == "__main__":
    # Example usage
    calc = Calculator()
    print(f"Initial: {calc}")
    
    calc.add(10)
    print(f"After adding 10: {calc}")
    
    calc.subtract(3)
    print(f"After subtracting 3: {calc}")
    
    calc.multiply(2)
    print(f"After multiplying by 2: {calc}")
    
    calc.divide(2)
    print(f"After dividing by 2: {calc}")
    
    print(f"\nHistory: {calc.get_history()}")
    
    # Using standalone functions
    print(f"\n2 + 3 = {add_numbers(2, 3)}")
    print(f"10 - 4 = {subtract_numbers(10, 4)}")
    print(f"5 * 6 = {multiply_numbers(5, 6)}")
    print(f"20 / 4 = {divide_numbers(20, 4)}")

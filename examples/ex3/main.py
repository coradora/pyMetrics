def factorial(n):
    """Calculates the factorial of a non-negative integer n."""
    if n < 0:
        raise ValueError("Factorial is only defined for non-negative integers.")
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

def main():
    number = int(input("Enter a non-negative integer: "))
    print(f"Factorial of {number} is: {factorial(number)}")

if __name__ == "__main__":
    main()
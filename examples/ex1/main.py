import random

def generate_random_number():
    return random.randint(1, 20)

def is_even(number):
    # Returns True if the number is even, False if odd
    return number % 2 == 0

def main():
    while True:
        random_number = generate_random_number()
        print(f"Generated number: {random_number}")

        for number in range(1, random_number + 1):
            if is_even(number):
                print(f"{number} is even.")
            else:
                print(f"{number} is odd.")
        
        # Ask the user if they want to run the loop again
        continue_prompt = input("Generate a new number? (y/n): ")
        if continue_prompt.lower() != 'y':
            break

if __name__ == "__main__":
    main()

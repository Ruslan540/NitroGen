import requests
import random
import string
import time

def generate_code(length=19):
    """Generates a random 19-character alphanumeric code."""
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

def check_code_validity(code):
    """Checks if the generated Discord gift code is valid."""
    url = f"https://discord.com/api/v8/entitlements/gift-codes/{code}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        elif response.status_code == 429:
            # Handle rate limiting by pausing and retrying after some time
            print("Rate limit hit. Waiting before retrying...")
            time.sleep(5)  # Wait before retrying; adjust time based on the rate limit headers
            return check_code_validity(code)
        else:
            return False
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def main(num_codes):
    """Generates the specified number of Discord gift codes and checks their validity."""
    for _ in range(num_codes):
        generated_code = generate_code()
        full_code = f"https://discord.gift/{generated_code}"
        
        if check_code_validity(generated_code):
            print(f"Valid code: {full_code}")
        else:
            print(f"Invalid code: {full_code}")

if __name__ == "__main__":
    try:
        num_codes_to_generate = int(input("Enter the number of codes to generate: "))
        if num_codes_to_generate > 1500:
            main(num_codes_to_generate)
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

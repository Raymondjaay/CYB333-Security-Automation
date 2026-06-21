import string

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one number.")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "admin",
        "letmein"
    ]

    if password.lower() in common_passwords:
        score = 0
        feedback.append("This password is too common.")

    if score >= 6:
        strength = "Strong"
    elif score >= 4:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, score, feedback


def main():
    print("Password Strength Checker")

    password = input("Enter a password: ")

    strength, score, feedback = check_password_strength(password)

    print(f"\nStrength: {strength}")
    print(f"Score: {score}")

    if feedback:
        print("\nSuggestions:")
        for item in feedback:
            print("-", item)


main()

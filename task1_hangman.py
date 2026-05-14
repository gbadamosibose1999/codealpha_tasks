import random

# A small list of words to guess
WORDS = ["python", "banana", "rocket", "laptop", "bridge"]

def display_word(word, guessed_letters):
    """Show the word with blanks for unguessed letters"""
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def hangman():
    print("=" * 40)
    print("       Welcome to HANGMAN! 🎮")
    print("=" * 40)

    # Pick a random word
    word = random.choice(WORDS)
    guessed_letters = []
    wrong_guesses = 0
    max_wrong = 6

    print(f"\nGuess the word! It has {len(word)} letters.")
    print("You have 6 wrong guesses allowed.\n")

    while wrong_guesses < max_wrong:
        # Show current state
        print(f"Word: {display_word(word, guessed_letters)}")
        print(f"Wrong guesses left: {max_wrong - wrong_guesses}")
        print(f"Letters guessed: {', '.join(guessed_letters) if guessed_letters else 'None'}")

        # Check if player won
        if all(letter in guessed_letters for letter in word):
            print(f"\n🎉 YOU WON! The word was: {word.upper()}")
            break

        # Get player's guess
        guess = input("\nGuess a letter: ").lower().strip()

        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("⚠️  Please enter a single letter only!")
            continue

        if guess in guessed_letters:
            print(f"⚠️  You already guessed '{guess}'! Try another.")
            continue

        guessed_letters.append(guess)

        if guess in word:
            print(f"✅ '{guess}' is in the word!")
        else:
            wrong_guesses += 1
            print(f"❌ '{guess}' is NOT in the word!")

        print("-" * 30)
    else:
        print(f"\n💀 GAME OVER! The word was: {word.upper()}")

    print("\nThanks for playing!\n")

if __name__ == "__main__":
    hangman()

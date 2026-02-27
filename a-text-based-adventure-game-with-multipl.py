```python
import time
import sys
import random

def slow_print(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_separator():
    slow_print("\n" + "="*50 + "\n")

def get_choice(options):
    while True:
        for i, option in enumerate(options, 1):
            slow_print(f"  [{i}] {option}")
        try:
            choice = input("\n> ").strip()
            if choice.lower() == "xyzzy":
                slow_print("\n✨ A hollow voice says 'Fool.'")
                continue
            if choice.lower() == "hello sailor":
                slow_print("\n🐟 The ancient sailor's greeting echoes through the void. Nothing happens. Or does it?")
                continue
            if choice.lower() == "help":
                slow_print("\n📖 You're on your own, adventurer. Trust your instincts.")
                continue
            if choice.lower() in ["quit", "exit"]:
                slow_print("\nFarewell, adventurer. The world fades to black...")
                sys.exit()
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return idx
            slow_print("Invalid choice. Try again.")
        except ValueError:
            slow_print("Please enter a number.")

class Game:
    def __init__(self):
        self.inventory = []
        self.flags = {}
        self.name = ""
        self.secret_count = 0

    def start(self):
        slow_print("\n" + "="*50)
        slow_print("   THE LOST KINGDOM OF ALDENMOOR")
        slow_print("="*50)
        slow_print("\nA text adventure of mystery, danger, and destiny.")
        slow_print("Type a number to choose your path.")
        slow_print("(Psst... try typing strange things sometimes.)\n")
        
        self.name = input("What is your name, adventurer? > ").strip()
        if not self.name:
            self.name = "Stranger"
        
        if self.name.lower() == "gandalf":
            slow_print(f"\nYou shall not pass... just kidding, {self.name}. Welcome. 🧙")
            self.secret_count += 1
        elif self.name.lower() in ["link", "zelda"]:
            slow_print(f"\n*Zelda music plays* It's dangerous to go alone, {self.name}!")
            self.secret_count += 1
        elif self.name.lower() == "guybrush threepwood":
            slow_print("\nMighty pirate detected. I'm selling these fine leather jackets.")
            self.secret_count += 1
        else:
            slow_print(f"\nWelcome, {self.name}. Your legend begins now.")
        
        time.sleep(1)
        self.forest_entrance()

    def forest_entrance(self):
        print_separator()
        slow_print(f"You, {self.name}, stand at the edge of the Darkwood Forest.")
        slow_print("The trees loom tall, their branches clawing at a grey sky.")
        slow_print("Behind you lies your quiet village. Before you — unknown.")
        slow_print("\nA dying traveler collapses at your feet and gasps:")
        slow_print("'The Crystal of Dawn... stolen from Aldenmoor... you must...")
        slow_print("He presses a MAP into your hand and goes still.")
        self.inventory.append("map")
        slow_print("\n📜 You received: MAP")
        
        print_separator()
        slow_print("Three paths diverge before you:")
        choice = get_choice([
            "Take the left path through the dense undergrowth",
            "Follow the right path along a babbling brook",
            "Walk straight ahead toward a distant tower",
            "Examine the map carefully",
            "Search the traveler's body"
        ])
        
        if choice == 0:
            self.left_path()
        elif choice == 1:
            self.right_path()
        elif choice == 2:
            self.tower_path()
        elif choice == 3:
            self.examine_map()
        elif choice == 4:
            self.search_traveler()

    def examine_map(self):
        print_separator()
        slow_print("You unfold the tattered map.")
        slow_print("It shows three landmarks:")
        slow_print("  🌿 LEFT  - The Witch's Hollow")
        slow_print("  💧 RIGHT - The River Shrine")
        slow_print("  🏰 CENTER - The Shadow Tower")
        slow_print("\nScrawled in red ink at the bottom:")
        slow_print("'DO NOT TRUST THE TOWER KEEPER'")
        self.flags["saw_map_warning"] = True
        
        print_separator()
        slow_print("Now which path do you take?")
        choice = get_choice([
            "Left path — The Witch's Hollow",
            "Right path — The River Shrine",
            "Center path — The Shadow Tower"
        ])
        
        if choice == 0:
            self.left_path()
        elif choice == 1:
            self.right_path()
        else:
            self.tower_path()

    def search_traveler(self):
        print_separator()
        slow_print("You kneel beside the traveler.")
        slow_print("In his coat pocket you find a small VIAL of glowing blue liquid.")
        slow_print("A note attached reads: 'Drink only in darkest need.'")
        self.inventory.append("healing vial")
        slow_print("\n💊 You received: HEALING VIAL")
        
        if random.random() < 0.3:
            slow_print("\n...You also find a half-eaten sandwich.")
            slow_print("It looks surprisingly fresh. You pocket it.")
            self.inventory.append("mysterious sandwich")
            slow_print("🥪 You received: MYSTERIOUS SANDWICH")
            self.secret_count += 1
        
        print_separator()
        slow_print("Which path do you take?")
        choice = get_choice([
            "Left path through the undergrowth",
            "Right path along the brook",
            "Straight toward the tower"
        ])
        
        if choice == 0:
            self.left_path()
        elif choice == 1:
            self.right_path()
        else:
            self.tower_path()

    def left_path(self):
        print_separator()
        slow_print("You push through the dense undergrowth.")
        slow_print("Thorns catch your cloak. Strange eyes blink from the shadows.")
        slow_print("After an hour of walking, you reach a clearing.")
        slow_print("\nAt the center stands a crooked cottage, smoke rising from its chimney.")
        slow_print("A sign above the door reads: 'MADAME ZELARA — SEER, HEALER, BAKER'")
        
        choice = get_choice([
            "Knock on the cottage door",
            "Peek through the window first",
            "Avoid the cottage and push deeper into the forest"
        ])
        
        if choice == 0:
            self.meet_zelara()
        elif choice == 1:
            self.peek_window()
        else:
            self.deep_forest()

    def peek_window(self):
        print_separator()
        slow_print("You creep to the window and peer inside.")
        slow_print("An old woman dances alone to music you cannot hear,")
        slow_print("stirring a massive cauldron.")
        slow_print("She suddenly STOPS and turns directly toward you.")
        slow_print("\n'I can SEE you, you know,' she calls cheerfully.")
        slow_print("'Come in, come in. The stew won't eat itself.'")
        self.meet_zelara()

    def meet_zelara(self):
        print_separator()
        slow_print("Madame Zelara is ancient, with silver hair and sharp green eyes.")
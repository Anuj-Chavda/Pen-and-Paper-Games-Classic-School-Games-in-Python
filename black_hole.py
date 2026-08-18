ROWS = 6

DIRECTIONS = [
    (-1, -1),
    (-1,  0),
    ( 0, -1),
    ( 0,  1),
    ( 1,  0),
    ( 1,  1)
]

# Every hole has a permanent coordinate.
board = {
    (x, y): None
    for x in range(ROWS)
    for y in range(x + 1)
}

used_tickets = {
    "A": set(),
    "B": set()
}


def valid_position(x, y):
    return (x, y) in board


def display_board():
    print("\n" + "=" * 60)

    for x in range(ROWS):

        # Indent each row to make the triangle
        print(" " * ((ROWS - x - 1) * 4), end="")

        for y in range(x + 1):

            value = board[(x, y)]

            if value is None:
                print("[   ]", end=" ")
            else:
                number, player = value
                print(f"[{number}{player}]", end=" ")

        print()

    print("=" * 60)


def display_coordinates():
    print("\nCoordinates of holes:")

    for x in range(ROWS):

        print(" " * ((ROWS - x - 1) * 4), end="")

        for y in range(x + 1):

            # Show the coordinate when the hole is empty
            if board[(x, y)] is None:
                print(f"({x},{y})", end=" ")

            else:
                number, player = board[(x, y)]
                print(f"{number}{player}", end=" ")

        print()


def get_neighbors(x, y):

    neighbors = []

    for dx, dy in DIRECTIONS:

        nx = x + dx
        ny = y + dy

        if valid_position(nx, ny):
            neighbors.append((nx, ny))

    return neighbors


def player_turn(player):

    print("\n" + "#" * 60)
    print(f"PLAYER {player}")
    print("#" * 60)

    display_board()
    display_coordinates()

    # ------------------------------------------
    # Show available tickets
    # ------------------------------------------

    available = [
        n for n in range(1, 11)
        if n not in used_tickets[player]
    ]

    print("\nAvailable tickets:")
    print(available)

    # ------------------------------------------
    # Choose exact coordinate
    # ------------------------------------------

    while True:

        try:

            x = int(input("\nEnter X (row): "))
            y = int(input("Enter Y (position): "))

        except ValueError:

            print("Enter numbers only.")
            continue

        # Check that coordinate actually exists
        if not valid_position(x, y):

            print(f"({x},{y}) is NOT a valid hole.")

            # For example:
            # row 5 has (5,0) through (5,5)

            continue

        # Check whether that EXACT hole is occupied
        if board[(x, y)] is not None:

            number, old_player = board[(x, y)]

            print(
                f"({x},{y}) is already occupied "
                f"by [{number}{old_player}]!"
            )

            continue

        break

    # ------------------------------------------
    # Choose ticket
    # ------------------------------------------

    while True:

        try:
            ticket = int(input("Enter ticket (1-10): "))

        except ValueError:

            print("Enter a number.")
            continue

        if ticket < 1 or ticket > 10:

            print("Ticket must be between 1 and 10.")
            continue

        if ticket in used_tickets[player]:

            print(
                f"Player {player} already used "
                f"ticket {ticket}!"
            )

            continue

        break

    # ------------------------------------------
    # PUT TICKET IN EXACT COORDINATE
    # ------------------------------------------

    board[(x, y)] = (ticket, player)

    used_tickets[player].add(ticket)

    print(
        f"\nPlayer {player} placed "
        f"[{ticket}{player}] at ({x},{y})"
    )


def find_black_hole():

    for coordinate in board:

        if board[coordinate] is None:
            return coordinate

    return None


def show_black_hole(x, y):

    print("\n" + "#" * 60)
    print(f"BLACK HOLE = ({x},{y})")
    print("#" * 60)

    neighbors = get_neighbors(x, y)

    print("\nAdjacent holes:")

    for nx, ny in neighbors:

        value = board[(nx, ny)]

        if value is None:

            print(f"({nx},{ny}) -> EMPTY")

        else:

            number, player = value

            print(
                f"({nx},{ny}) -> [{number}{player}]"
            )


def determine_winner(x, y):

    neighbors = get_neighbors(x, y)

    adjacent = {
        "A": [],
        "B": []
    }

    for nx, ny in neighbors:

        value = board[(nx, ny)]

        if value is not None:

            number, player = value

            adjacent[player].append(number)

    print("\n" + "#" * 60)
    print("RESULT")
    print("#" * 60)

    print(f"\nBlack Hole: ({x},{y})")

    print("A adjacent tickets:", adjacent["A"])
    print("B adjacent tickets:", adjacent["B"])

    if not adjacent["A"] and not adjacent["B"]:
        print("\nDRAW - no adjacent tickets.")
        return

    if not adjacent["A"]:
        print("\nPLAYER B WINS!")
        return

    if not adjacent["B"]:
        print("\nPLAYER A WINS!")
        return

    lowest_a = min(adjacent["A"])
    lowest_b = min(adjacent["B"])

    print(f"\nA lowest: {lowest_a}")
    print(f"B lowest: {lowest_b}")

    if lowest_a < lowest_b:
        print("\n🏆 PLAYER A WINS!")

    elif lowest_b < lowest_a:
        print("\n🏆 PLAYER B WINS!")

    else:
        print("\nDRAW!")


def main():

    print("\n")
    print("############################################")
    print("#              BLACK HOLE                 #")
    print("############################################")

    print("""
Rules:

• 21 holes
• 20 turns
• A and B alternate
• Tickets are 1-10
• Each player's ticket can be used only once
• A and B can both use the same ticket
• Last empty hole = Black Hole
• Black Hole has up to 6 neighbors
""")

    input("Press ENTER to start...")

    player = "A"

    # Exactly 20 moves
    for turn in range(20):

        print(f"\nTURN {turn + 1}/20")

        player_turn(player)

        # Switch player
        if player == "A":
            player = "B"
        else:
            player = "A"

    # ------------------------------------------
    # Find final empty cell
    # ------------------------------------------

    black_hole = find_black_hole()

    x, y = black_hole

    display_board()

    print("\n")
    print("############################################")
    print("#            BLACK HOLE FOUND              #")
    print(f"#                ({x},{y})                 #")
    print("############################################")

    show_black_hole(x, y)

    determine_winner(x, y)


if __name__ == "__main__":
    main()
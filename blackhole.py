import tkinter as tk
from tkinter import messagebox


# ============================================================
#                    BLACK HOLE
# ============================================================

ROWS = 6

TICKETS = range(1, 11)

# Your exact 6-neighbor coordinate system
DIRECTIONS = (
    (-1, -1),
    (-1,  0),
    ( 0, -1),
    ( 0,  1),
    ( 1,  0),
    ( 1,  1),
)


# ============================================================
#                    COLORS
# ============================================================

BG = "#FFF7FB"
PANEL = "#FFFFFF"

TEXT = "#5B465A"
SUBTEXT = "#9A7F96"

PLAYER_A_COLOR = "#F6A6C1"       # pink
PLAYER_A_DARK = "#D96B96"

PLAYER_B_COLOR = "#B9B7F8"       # lavender
PLAYER_B_DARK = "#7773D1"

EMPTY_COLOR = "#FFE6F0"
EMPTY_OUTLINE = "#E9AFC7"

SELECTED_COLOR = "#FFD166"       # soft yellow

BLACK_HOLE = "#35263A"

TICKET_BG = "#FFF0F6"
TICKET_ACTIVE = "#F7C6D9"
TICKET_DISABLED = "#E8E1E6"


# ============================================================
#                    GAME DATA
# ============================================================

board = {
    (x, y): None
    for x in range(ROWS)
    for y in range(x + 1)
}

used_tickets = {
    "A": set(),
    "B": set()
}

players = {
    "A": "Player A",
    "B": "Player B"
}

current_player = "A"

selected_position = None

game_over = False


# ============================================================
#                    WINDOW
# ============================================================

root = tk.Tk()

root.title("Black Hole ✨")
root.geometry("1050x820")
root.configure(bg=BG)
root.resizable(False, False)


# ============================================================
#                    TOP TITLE
# ============================================================

title = tk.Label(
    root,
    text="✦  BLACK HOLE  ✦",
    font=("Georgia", 28, "bold"),
    fg="#C75B88",
    bg=BG
)

title.pack(pady=(15, 3))


subtitle = tk.Label(
    root,
    text="A battle of numbers, strategy & luck",
    font=("Georgia", 11, "italic"),
    fg=SUBTEXT,
    bg=BG
)

subtitle.pack()


# ============================================================
#                    PLAYER DISPLAY
# ============================================================

player_frame = tk.Frame(
    root,
    bg=BG
)

player_frame.pack(pady=12)


player_a_label = tk.Label(
    player_frame,
    text="",
    font=("Arial", 14, "bold"),
    bg=PLAYER_A_COLOR,
    fg="#70344E",
    padx=25,
    pady=10
)

player_a_label.pack(side="left", padx=12)


player_b_label = tk.Label(
    player_frame,
    text="",
    font=("Arial", 14, "bold"),
    bg=PLAYER_B_COLOR,
    fg="#494582",
    padx=25,
    pady=10
)

player_b_label.pack(side="left", padx=12)


# ============================================================
#                    STATUS
# ============================================================

status = tk.Label(
    root,
    text="",
    font=("Arial", 16, "bold"),
    fg=PLAYER_A_DARK,
    bg=BG
)

status.pack(pady=4)


instruction = tk.Label(
    root,
    text="Click a hole, then choose a ticket.",
    font=("Arial", 11),
    fg=SUBTEXT,
    bg=BG
)

instruction.pack()


# ============================================================
#                    BOARD CANVAS
# ============================================================

canvas = tk.Canvas(
    root,
    width=850,
    height=390,
    bg=BG,
    highlightthickness=0
)

canvas.pack(pady=15)


# Center positions for the triangular board
HOLE_RADIUS = 29
X_GAP = 82
Y_GAP = 63

HOLE_CENTERS = {}


def calculate_positions():

    HOLE_CENTERS.clear()

    center_x = 425

    for x in range(ROWS):

        row_width = x * X_GAP

        start_x = center_x - row_width / 2

        y_position = 45 + x * Y_GAP

        for y in range(x + 1):

            px = start_x + y * X_GAP
            py = y_position

            HOLE_CENTERS[(x, y)] = (px, py)


calculate_positions()


# ============================================================
#                    DRAW BOARD
# ============================================================

def draw_hole(position):

    x, y = position

    px, py = HOLE_CENTERS[position]

    value = board[position]

    # --------------------------------------------------------
    # Colors
    # --------------------------------------------------------

    if position == selected_position:

        fill = SELECTED_COLOR
        outline = "#E7A928"
        width = 5

    elif value is None:

        fill = EMPTY_COLOR
        outline = EMPTY_OUTLINE
        width = 3

    else:

        ticket, player = value

        if player == "A":
            fill = PLAYER_A_COLOR
            outline = PLAYER_A_DARK
        else:
            fill = PLAYER_B_COLOR
            outline = PLAYER_B_DARK

        width = 3

    # --------------------------------------------------------
    # Circle
    # --------------------------------------------------------

    canvas.create_oval(
        px - HOLE_RADIUS,
        py - HOLE_RADIUS,
        px + HOLE_RADIUS,
        py + HOLE_RADIUS,
        fill=fill,
        outline=outline,
        width=width,
        tags=f"hole_{x}_{y}"
    )

    # --------------------------------------------------------
    # Text
    # --------------------------------------------------------

    if value is None:

        text = "♡"

    else:

        ticket, player = value

        text = str(ticket)

    canvas.create_text(
        px,
        py,
        text=text,
        font=("Arial", 15, "bold"),
        fill=TEXT,
        tags=f"hole_{x}_{y}"
    )


def draw_board():

    canvas.delete("all")

    # Soft connecting lines
    for x, y in board:

        px, py = HOLE_CENTERS[(x, y)]

        for nx, ny in get_neighbors(x, y):

            # Draw each connection only once
            if (x, y) < (nx, ny):

                npx, npy = HOLE_CENTERS[(nx, ny)]

                canvas.create_line(
                    px,
                    py,
                    npx,
                    npy,
                    fill="#F1D7E4",
                    width=2
                )

    # Draw circles
    for position in board:
        draw_hole(position)


# ============================================================
#                    NEIGHBORS
# ============================================================

def get_neighbors(x, y):

    result = []

    for dx, dy in DIRECTIONS:

        nx = x + dx
        ny = y + dy

        if (nx, ny) in board:
            result.append((nx, ny))

    return result


# ============================================================
#                    HOLE CLICK
# ============================================================

def canvas_click(event):

    global selected_position

    if game_over:
        return

    clicked = None

    for position, (px, py) in HOLE_CENTERS.items():

        distance = (
            (event.x - px) ** 2 +
            (event.y - py) ** 2
        ) ** 0.5

        if distance <= HOLE_RADIUS:

            clicked = position
            break

    if clicked is None:
        return

    # Already occupied
    if board[clicked] is not None:

        ticket, player = board[clicked]

        status.config(
            text=f"{players[player]} placed {ticket} here.",
            fg=SUBTEXT
        )

        return

    selected_position = clicked

    draw_board()

    x, y = clicked

    status.config(
        text=f"{players[current_player]} • selected ({x},{y})",
        fg=(
            PLAYER_A_DARK
            if current_player == "A"
            else PLAYER_B_DARK
        )
    )


canvas.bind("<Button-1>", canvas_click)


# ============================================================
#                    TICKET PANEL
# ============================================================

ticket_panel = tk.Frame(
    root,
    bg=PANEL,
    padx=15,
    pady=10
)

ticket_panel.pack()


ticket_title = tk.Label(
    ticket_panel,
    text="",
    font=("Arial", 13, "bold"),
    fg=TEXT,
    bg=PANEL
)

ticket_title.pack(pady=(0, 8))


ticket_frame = tk.Frame(
    ticket_panel,
    bg=PANEL
)

ticket_frame.pack()


ticket_buttons = {}


# ============================================================
#                    TICKET CLICK
# ============================================================

def place_ticket(ticket):

    global current_player
    global selected_position

    if game_over:
        return

    if selected_position is None:

        messagebox.showinfo(
            "Choose a hole",
            "First click an empty hole on the board."
        )

        return

    if ticket in used_tickets[current_player]:

        messagebox.showwarning(
            "Ticket already used",
            f"{players[current_player]} already used ticket {ticket}."
        )

        return

    position = selected_position

    # --------------------------------------------------------
    # Store at EXACT coordinate
    # --------------------------------------------------------

    board[position] = (
        ticket,
        current_player
    )

    used_tickets[current_player].add(ticket)

    selected_position = None

    # --------------------------------------------------------
    # Check if 20 cells are filled
    # --------------------------------------------------------

    filled = sum(
        value is not None
        for value in board.values()
    )

    if filled == 20:

        draw_board()
        finish_game()

        return

    # --------------------------------------------------------
    # Switch player
    # --------------------------------------------------------

    current_player = (
        "B"
        if current_player == "A"
        else "A"
    )

    update_ui()
    draw_board()


# ============================================================
#                    TICKET BUTTONS
# ============================================================

for ticket in TICKETS:

    button = tk.Button(
        ticket_frame,
        text=str(ticket),
        font=("Arial", 11, "bold"),
        width=3,
        height=1,
        bg=TICKET_BG,
        fg=TEXT,
        activebackground=TICKET_ACTIVE,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        padx=5,
        pady=5,
        command=lambda t=ticket: place_ticket(t)
    )

    button.pack(side="left", padx=3)

    ticket_buttons[ticket] = button


# ============================================================
#                    UPDATE UI
# ============================================================

def update_ui():

    name = players[current_player]

    status.config(
        text=f"♡  {name}'s turn  ♡",
        fg=(
            PLAYER_A_DARK
            if current_player == "A"
            else PLAYER_B_DARK
        )
    )

    ticket_title.config(
        text=f"{name}'s tickets"
    )

    # --------------------------------------------------------
    # Highlight current player
    # --------------------------------------------------------

    if current_player == "A":

        player_a_label.config(
            relief="solid",
            bd=3
        )

        player_b_label.config(
            relief="flat",
            bd=0
        )

    else:

        player_b_label.config(
            relief="solid",
            bd=3
        )

        player_a_label.config(
            relief="flat",
            bd=0
        )

    # --------------------------------------------------------
    # Ticket buttons
    # --------------------------------------------------------

    for ticket, button in ticket_buttons.items():

        if ticket in used_tickets[current_player]:

            button.config(
                state="disabled",
                bg=TICKET_DISABLED,
                fg="#AAA0AA"
            )

        else:

            button.config(
                state="normal",
                bg=(
                    "#FFE1EC"
                    if current_player == "A"
                    else "#E4E2FF"
                ),
                fg=TEXT
            )


# ============================================================
#                    FIND BLACK HOLE
# ============================================================

def find_black_hole():

    for position, value in board.items():

        if value is None:
            return position

    return None


# ============================================================
#                    GAME OVER
# ============================================================

def finish_game():

    global game_over

    game_over = True

    black_hole = find_black_hole()

    adjacent = get_neighbors(*black_hole)

    # --------------------------------------------------------
    # Determine adjacent numbers
    # --------------------------------------------------------

    numbers = {
        "A": [],
        "B": []
    }

    for position in adjacent:

        value = board[position]

        if value is not None:

            ticket, player = value

            numbers[player].append(ticket)

    # --------------------------------------------------------
    # Draw final board
    # --------------------------------------------------------

    draw_board()

    bx, by = HOLE_CENTERS[black_hole]

    canvas.create_oval(
        bx - HOLE_RADIUS,
        by - HOLE_RADIUS,
        bx + HOLE_RADIUS,
        by + HOLE_RADIUS,
        fill=BLACK_HOLE,
        outline="#111111",
        width=5
    )

    canvas.create_text(
        bx,
        by,
        text="BH",
        font=("Arial", 13, "bold"),
        fill="white"
    )

    # --------------------------------------------------------
    # Highlight adjacent holes
    # --------------------------------------------------------

    for position in adjacent:

        px, py = HOLE_CENTERS[position]

        canvas.create_oval(
            px - HOLE_RADIUS - 5,
            py - HOLE_RADIUS - 5,
            px + HOLE_RADIUS + 5,
            py + HOLE_RADIUS + 5,
            outline="#FFD166",
            width=3
        )

    # --------------------------------------------------------
    # Find winner
    # --------------------------------------------------------

    lowest_a = min(numbers["A"]) if numbers["A"] else None
    lowest_b = min(numbers["B"]) if numbers["B"] else None

    if lowest_a is None and lowest_b is None:

        winner_text = "DRAW!\nNo adjacent tickets."

    elif lowest_a is None:

        winner_text = (
            f"🌸 {players['B']} WINS! 🌸\n\n"
            f"Lowest adjacent ticket: {lowest_b}"
        )

    elif lowest_b is None:

        winner_text = (
            f"🌸 {players['A']} WINS! 🌸\n\n"
            f"Lowest adjacent ticket: {lowest_a}"
        )

    elif lowest_a < lowest_b:

        winner_text = (
            f"🌸 {players['A']} WINS! 🌸\n\n"
            f"{lowest_a}  <  {lowest_b}"
        )

    elif lowest_b < lowest_a:

        winner_text = (
            f"🌸 {players['B']} WINS! 🌸\n\n"
            f"{lowest_b}  <  {lowest_a}"
        )

    else:

        winner_text = (
            "💕 DRAW! 💕\n\n"
            f"Both have {lowest_a}"
        )

    # --------------------------------------------------------
    # Update screen
    # --------------------------------------------------------

    status.config(
        text="✦ GAME OVER ✦",
        fg="#C75B88"
    )

    instruction.config(
        text=(
            f"Black Hole: {black_hole}   •   "
            f"A: {numbers['A']}   •   "
            f"B: {numbers['B']}"
        )
    )

    for button in ticket_buttons.values():
        button.config(state="disabled")

    messagebox.showinfo(
        "✦ Black Hole ✦",
        f"Black Hole: {black_hole}\n\n"
        f"{players['A']}: {numbers['A']}\n"
        f"{players['B']}: {numbers['B']}\n\n"
        f"{winner_text}"
    )


# ============================================================
#                    NAME INPUT
# ============================================================

def start_game():

    name_a = name_a_entry.get().strip()
    name_b = name_b_entry.get().strip()

    if not name_a:
        name_a = "Player A"

    if not name_b:
        name_b = "Player B"

    players["A"] = name_a
    players["B"] = name_b

    name_window.destroy()

    player_a_label.config(
        text=f"🌸 A • {players['A']}"
    )

    player_b_label.config(
        text=f"💜 B • {players['B']}"
    )

    update_ui()
    draw_board()


# ============================================================
#                    NAME WINDOW
# ============================================================

name_window = tk.Toplevel(root)

name_window.title("Welcome to Black Hole")
name_window.geometry("420x350")
name_window.configure(bg=BG)
name_window.resizable(False, False)

name_window.grab_set()


welcome = tk.Label(
    name_window,
    text="✦ BLACK HOLE ✦",
    font=("Georgia", 24, "bold"),
    fg="#C75B88",
    bg=BG
)

welcome.pack(pady=(35, 8))


welcome_sub = tk.Label(
    name_window,
    text="Let's meet today's players ♡",
    font=("Georgia", 12, "italic"),
    fg=SUBTEXT,
    bg=BG
)

welcome_sub.pack(pady=(0, 25))


tk.Label(
    name_window,
    text="🌸 Player A",
    font=("Arial", 12, "bold"),
    fg=PLAYER_A_DARK,
    bg=BG
).pack()

name_a_entry = tk.Entry(
    name_window,
    font=("Arial", 13),
    justify="center",
    bg="#FFF0F6",
    fg=TEXT,
    relief="flat"
)

name_a_entry.pack(
    pady=(5, 18),
    ipady=7
)


tk.Label(
    name_window,
    text="💜 Player B",
    font=("Arial", 12, "bold"),
    fg=PLAYER_B_DARK,
    bg=BG
).pack()

name_b_entry = tk.Entry(
    name_window,
    font=("Arial", 13),
    justify="center",
    bg="#F0EFFF",
    fg=TEXT,
    relief="flat"
)

name_b_entry.pack(
    pady=(5, 20),
    ipady=7
)


start_button = tk.Button(
    name_window,
    text="♡  START GAME  ♡",
    font=("Arial", 12, "bold"),
    bg="#F6A6C1",
    fg="#70344E",
    activebackground="#E98BAE",
    relief="flat",
    padx=25,
    pady=9,
    command=start_game
)

start_button.pack()


# ============================================================
#                    START
# ============================================================

name_a_entry.focus()

root.mainloop()
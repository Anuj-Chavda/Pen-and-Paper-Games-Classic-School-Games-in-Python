import tkinter as tk
from tkinter import messagebox
import random


# ============================================================
# D O T S   &   B O X E S
# ============================================================

class DotsAndBoxes:
    def __init__(self, root):
        self.root = root
        self.root.title("🌸 Dots & Boxes")
        self.root.geometry("1100x800")
        self.root.minsize(900, 700)
        self.root.configure(bg="#FFF7FB")

        # ----------------------------------------------------
        # Color palette
        # ----------------------------------------------------
        self.bg = "#FFF7FB"
        self.card = "#FFFFFF"
        self.dark_pink = "#D94F87"
        self.pink = "#F7A8C4"
        self.light_pink = "#FDE2EC"
        self.text = "#4A3741"
        self.muted = "#967B87"
        self.border = "#F3D5E2"

        self.player_colors = [
            "#F48FB1",   # pink
            "#9FA8DA",   # lavender/blue
            "#80CBC4",   # mint
            "#FFCC80"    # peach
        ]

        self.dot_color = "#594550"
        self.line_width = 5

        self.players = []
        self.current_player = 0
        self.board_size = 6
        self.canvas_size = 650
        self.margin = 55
        self.spacing = 90

        self.lines = set()
        self.boxes = {}
        self.scores = []

        self.canvas = None

        self.show_start_screen()

    # ========================================================
    # START SCREEN
    # ========================================================

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_screen(self):
        self.clear_window()

        container = tk.Frame(
            self.root,
            bg=self.bg
        )
        container.pack(fill="both", expand=True)

        # Header
        title = tk.Label(
            container,
            text="🌸  Dots & Boxes  🌸",
            font=("Helvetica", 34, "bold"),
            fg=self.dark_pink,
            bg=self.bg
        )
        title.pack(pady=(55, 5))

        subtitle = tk.Label(
            container,
            text="A little game of lines, boxes & strategy ♡",
            font=("Helvetica", 13),
            fg=self.muted,
            bg=self.bg
        )
        subtitle.pack(pady=(0, 30))

        card = tk.Frame(
            container,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=2
        )
        card.pack(
            padx=100,
            ipadx=45,
            ipady=30
        )

        # Board size
        tk.Label(
            card,
            text="Choose your board",
            font=("Helvetica", 16, "bold"),
            fg=self.text,
            bg=self.card
        ).pack(pady=(10, 10))

        self.size_var = tk.StringVar(value="6")

        size_frame = tk.Frame(card, bg=self.card)
        size_frame.pack()

        sizes = [4, 5, 6, 8, 10, 12, 16]

        for size in sizes:
            rb = tk.Radiobutton(
                size_frame,
                text=f"{size} × {size}",
                variable=self.size_var,
                value=str(size),
                font=("Helvetica", 11),
                bg=self.card,
                fg=self.text,
                activebackground=self.card,
                activeforeground=self.dark_pink,
                selectcolor=self.light_pink,
                indicatoron=True
            )
            rb.pack(side="left", padx=7)

        # Number of players
        tk.Label(
            card,
            text="Number of players",
            font=("Helvetica", 16, "bold"),
            fg=self.text,
            bg=self.card
        ).pack(pady=(28, 10))

        self.player_count_var = tk.IntVar(value=2)

        player_frame = tk.Frame(card, bg=self.card)
        player_frame.pack()

        for number in range(2, 5):
            rb = tk.Radiobutton(
                player_frame,
                text=f"{number} players",
                variable=self.player_count_var,
                value=number,
                font=("Helvetica", 11),
                bg=self.card,
                fg=self.text,
                activebackground=self.card,
                selectcolor=self.light_pink
            )
            rb.pack(side="left", padx=15)

        # Nicknames
        tk.Label(
            card,
            text="Player nicknames",
            font=("Helvetica", 16, "bold"),
            fg=self.text,
            bg=self.card
        ).pack(pady=(28, 10))

        self.name_entries = []

        names = ["Pinkie", "Lavender", "Minty", "Peachy"]

        for i in range(4):
            row = tk.Frame(card, bg=self.card)

            tk.Label(
                row,
                text=f"Player {i + 1}",
                width=10,
                anchor="w",
                font=("Helvetica", 10, "bold"),
                fg=self.text,
                bg=self.card
            ).pack(side="left")

            entry = tk.Entry(
                row,
                width=22,
                font=("Helvetica", 11),
                bg="#FFF9FC",
                fg=self.text,
                relief="flat",
                highlightthickness=1,
                highlightbackground=self.border,
                highlightcolor=self.pink
            )

            entry.insert(0, names[i])

            entry.pack(
                side="left",
                padx=5,
                ipady=6
            )

            self.name_entries.append(entry)

            # Hide player 3/4 initially
            if i >= 2:
                row.pack_forget()
            else:
                row.pack(pady=4)

        # Need to update visible name fields when player count changes
        self.player_count_var.trace_add(
            "write",
            lambda *args: self.update_name_fields(card)
        )

        start_button = tk.Button(
            card,
            text="🌷  Start Game  🌷",
            command=self.start_game,
            font=("Helvetica", 14, "bold"),
            fg="white",
            bg=self.dark_pink,
            activebackground="#C63E75",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12
        )
        start_button.pack(pady=(30, 10))

    def update_name_fields(self, card):
        count = self.player_count_var.get()

        # Reconstruct the rows based on their parent
        rows = []

        for widget in card.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        if child.cget("text").startswith("Player"):
                            rows.append(widget)
                            break

        # Easier approach: find frames containing our entries
        for entry in self.name_entries:
            parent = entry.master

            if self.name_entries.index(entry) < count:
                parent.pack(pady=4)
            else:
                parent.pack_forget()

    # ========================================================
    # START GAME
    # ========================================================

    def start_game(self):
        self.board_size = int(self.size_var.get())
        count = self.player_count_var.get()

        self.players = []

        for i in range(count):
            name = self.name_entries[i].get().strip()

            if not name:
                name = f"Player {i + 1}"

            self.players.append(name)

        self.scores = [0] * count
        self.current_player = 0
        self.lines = set()
        self.boxes = {}

        self.show_game_screen()

    # ========================================================
    # GAME SCREEN
    # ========================================================

    def show_game_screen(self):
        self.clear_window()

        # Main background
        main = tk.Frame(self.root, bg=self.bg)
        main.pack(fill="both", expand=True)

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = tk.Frame(
            main,
            bg=self.bg
        )
        header.pack(fill="x", padx=30, pady=(20, 10))

        title = tk.Label(
            header,
            text="🌸 Dots & Boxes",
            font=("Helvetica", 26, "bold"),
            fg=self.dark_pink,
            bg=self.bg
        )
        title.pack(side="left")

        self.turn_label = tk.Label(
            header,
            text="",
            font=("Helvetica", 13, "bold"),
            fg=self.text,
            bg=self.light_pink,
            padx=18,
            pady=8
        )
        self.turn_label.pack(side="right")

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------

        content = tk.Frame(main, bg=self.bg)
        content.pack(fill="both", expand=True, padx=25, pady=10)

        # Board card
        board_card = tk.Frame(
            content,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=2
        )
        board_card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        # Scoreboard card
        score_card = tk.Frame(
            content,
            bg=self.card,
            width=270,
            highlightbackground=self.border,
            highlightthickness=2
        )
        score_card.pack(
            side="right",
            fill="y"
        )
        score_card.pack_propagate(False)

        # ----------------------------------------------------
        # Canvas
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            board_card,
            bg="#FFFCFE",
            highlightthickness=0
        )
        self.canvas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        self.canvas.bind(
            "<Configure>",
            lambda event: self.draw_board()
        )

        self.canvas.bind(
            "<Button-1>",
            self.handle_click
        )

        # ----------------------------------------------------
        # Scoreboard
        # ----------------------------------------------------

        tk.Label(
            score_card,
            text="✨ Live Score",
            font=("Helvetica", 19, "bold"),
            fg=self.dark_pink,
            bg=self.card
        ).pack(pady=(25, 5))

        tk.Label(
            score_card,
            text="Boxes claimed",
            font=("Helvetica", 10),
            fg=self.muted,
            bg=self.card
        ).pack(pady=(0, 20))

        self.score_frame = tk.Frame(
            score_card,
            bg=self.card
        )
        self.score_frame.pack(
            fill="x",
            padx=20
        )

        self.score_labels = []

        for i, name in enumerate(self.players):
            row = tk.Frame(
                self.score_frame,
                bg=self.card
            )
            row.pack(fill="x", pady=7)

            color_circle = tk.Label(
                row,
                text="●",
                font=("Helvetica", 18),
                fg=self.player_colors[i],
                bg=self.card
            )
            color_circle.pack(side="left")

            name_label = tk.Label(
                row,
                text=name,
                font=("Helvetica", 11, "bold"),
                fg=self.text,
                bg=self.card
            )
            name_label.pack(side="left", padx=8)

            score_label = tk.Label(
                row,
                text="0",
                font=("Helvetica", 14, "bold"),
                fg=self.player_colors[i],
                bg=self.card
            )
            score_label.pack(side="right")

            self.score_labels.append(score_label)

        # Divider
        tk.Frame(
            score_card,
            height=2,
            bg=self.light_pink
        ).pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.status_label = tk.Label(
            score_card,
            text="Draw a line to begin ♡",
            font=("Helvetica", 11),
            fg=self.muted,
            bg=self.card,
            wraplength=220
        )
        self.status_label.pack(
            padx=20,
            pady=5
        )

        # Bottom buttons
        button_frame = tk.Frame(
            score_card,
            bg=self.card
        )
        button_frame.pack(
            side="bottom",
            pady=20
        )

        tk.Button(
            button_frame,
            text="↻ New Game",
            command=self.show_start_screen,
            font=("Helvetica", 10, "bold"),
            fg=self.dark_pink,
            bg=self.light_pink,
            activebackground="#F9CCDC",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack()

        # Draw initial board
        self.root.after(100, self.draw_board)

    # ========================================================
    # BOARD DRAWING
    # ========================================================

    def calculate_geometry(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        usable = min(width, height) - 100

        if usable < 100:
            usable = 100

        self.spacing = usable / (self.board_size - 1)

        self.margin_x = (width - usable) / 2
        self.margin_y = (height - usable) / 2

    def point(self, row, col):
        x = self.margin_x + col * self.spacing
        y = self.margin_y + row * self.spacing
        return x, y

    def draw_board(self):
        if self.canvas is None:
            return

        self.calculate_geometry()

        self.canvas.delete("all")

        # ----------------------------------------------------
        # Draw completed boxes first
        # ----------------------------------------------------

        for (r, c), player_index in self.boxes.items():

            x1, y1 = self.point(r, c)
            x2, y2 = self.point(r + 1, c + 1)

            color = self.player_colors[player_index]

            # Soft translucent-like effect using light tint
            self.canvas.create_rectangle(
                x1 + 4,
                y1 + 4,
                x2 - 4,
                y2 - 4,
                fill=self.lighten(color, 0.70),
                outline=""
            )

            # Player initial
            initial = self.players[player_index][0].upper()

            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=initial,
                font=("Helvetica", max(12, int(self.spacing / 4)), "bold"),
                fill=color
            )

        # ----------------------------------------------------
        # Draw existing lines
        # ----------------------------------------------------

        for line in self.lines:
            r, c, direction = line

            if direction == "h":
                x1, y1 = self.point(r, c)
                x2, y2 = self.point(r, c + 1)
            else:
                x1, y1 = self.point(r, c)
                x2, y2 = self.point(r + 1, c)

            player_index = self.get_line_owner(line)

            color = (
                self.player_colors[player_index]
                if player_index is not None
                else self.dark_pink
            )

            self.canvas.create_line(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                width=self.line_width,
                capstyle=tk.ROUND
            )

        # ----------------------------------------------------
        # Draw dots
        # ----------------------------------------------------

        dot_radius = 6

        for r in range(self.board_size):
            for c in range(self.board_size):
                x, y = self.point(r, c)

                self.canvas.create_oval(
                    x - dot_radius,
                    y - dot_radius,
                    x + dot_radius,
                    y + dot_radius,
                    fill=self.dot_color,
                    outline=""
                )

        self.update_turn_display()

    # ========================================================
    # LINE OWNER
    # ========================================================

    def get_line_owner(self, line):
        # A line is stored as:
        # (row, col, "h"/"v")
        #
        # We don't directly store ownership in lines.
        # Instead, ownership is encoded separately.

        return self.line_owners.get(line) if hasattr(
            self, "line_owners"
        ) else None

    # ========================================================
    # CLICK HANDLING
    # ========================================================

    def handle_click(self, event):

        if not hasattr(self, "line_owners"):
            self.line_owners = {}

        self.calculate_geometry()

        # Find closest horizontal/vertical edge
        best_line = None
        best_distance = float("inf")

        # Horizontal lines
        for r in range(self.board_size):
            for c in range(self.board_size - 1):

                x1, y1 = self.point(r, c)
                x2, y2 = self.point(r, c + 1)

                distance = self.distance_to_segment(
                    event.x,
                    event.y,
                    x1,
                    y1,
                    x2,
                    y2
                )

                if distance < best_distance:
                    best_distance = distance
                    best_line = (r, c, "h")

        # Vertical lines
        for r in range(self.board_size - 1):
            for c in range(self.board_size):

                x1, y1 = self.point(r, c)
                x2, y2 = self.point(r + 1, c)

                distance = self.distance_to_segment(
                    event.x,
                    event.y,
                    x1,
                    y1,
                    x2,
                    y2
                )

                if distance < best_distance:
                    best_distance = distance
                    best_line = (r, c, "v")

        # Don't accept clicks too far away
        if best_distance > self.spacing * 0.35:
            return

        # Already taken
        if best_line in self.lines:
            return

        self.lines.add(best_line)

        current = self.current_player

        self.line_owners[best_line] = current

        completed = self.check_completed_boxes(best_line)

        if completed > 0:
            self.scores[current] += completed

            self.status_label.config(
                text=f"✨ {self.players[current]} completed "
                     f"{completed} box{'es' if completed != 1 else ''}!"
            )

            # Player gets another turn
        else:
            self.current_player = (
                self.current_player + 1
            ) % len(self.players)

            self.status_label.config(
                text=f"{self.players[self.current_player]}'s turn ♡"
            )

        self.update_scores()
        self.draw_board()

        # Check game over
        total_boxes = (self.board_size - 1) ** 2

        if sum(self.scores) == total_boxes:
            self.end_game()

    # ========================================================
    # CHECK BOXES
    # ========================================================

    def check_completed_boxes(self, line):
        r, c, direction = line

        possible_boxes = []

        if direction == "h":

            # Box below horizontal line
            if r < self.board_size - 1:
                possible_boxes.append((r, c))

            # Box above horizontal line
            if r > 0:
                possible_boxes.append((r - 1, c))

        else:

            # Box right of vertical line
            if c < self.board_size - 1:
                possible_boxes.append((r, c))

            # Box left of vertical line
            if c > 0:
                possible_boxes.append((r, c - 1))

        completed = 0

        for box in possible_boxes:

            if box in self.boxes:
                continue

            br, bc = box

            top = (br, bc, "h")
            bottom = (br + 1, bc, "h")
            left = (br, bc, "v")
            right = (br, bc + 1, "v")

            if (
                top in self.lines and
                bottom in self.lines and
                left in self.lines and
                right in self.lines
            ):
                self.boxes[box] = self.current_player
                completed += 1

        return completed

    # ========================================================
    # SCOREBOARD
    # ========================================================

    def update_scores(self):

        for i, label in enumerate(self.score_labels):
            label.config(text=str(self.scores[i]))

    def update_turn_display(self):

        if not hasattr(self, "turn_label"):
            return

        name = self.players[self.current_player]
        color = self.player_colors[self.current_player]

        self.turn_label.config(
            text=f"♡ {name}'s turn",
            fg=color
        )

    # ========================================================
    # GAME OVER
    # ========================================================

    def end_game(self):

        max_score = max(self.scores)

        winners = [
            self.players[i]
            for i, score in enumerate(self.scores)
            if score == max_score
        ]

        if len(winners) == 1:
            winner_text = f"🏆 {winners[0]} wins! 🏆"
        else:
            winner_text = "🏆 It's a tie! 🏆"

        # Custom popup
        popup = tk.Toplevel(self.root)
        popup.title("Game Over 🌸")
        popup.geometry("460x450")
        popup.configure(bg=self.bg)
        popup.resizable(False, False)

        tk.Label(
            popup,
            text="🎀 Game Over 🎀",
            font=("Helvetica", 27, "bold"),
            fg=self.dark_pink,
            bg=self.bg
        ).pack(pady=(30, 5))

        tk.Label(
            popup,
            text=winner_text,
            font=("Helvetica", 19, "bold"),
            fg=self.text,
            bg=self.bg
        ).pack(pady=10)

        tk.Label(
            popup,
            text=f"Highest score: {max_score} boxes",
            font=("Helvetica", 12),
            fg=self.muted,
            bg=self.bg
        ).pack(pady=(0, 20))

        score_box = tk.Frame(
            popup,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=2
        )
        score_box.pack(
            padx=40,
            fill="x"
        )

        ranking = sorted(
            zip(self.players, self.scores),
            key=lambda x: x[1],
            reverse=True
        )

        medals = ["🥇", "🥈", "🥉", "🌷"]

        for i, (name, score) in enumerate(ranking):

            tk.Label(
                score_box,
                text=f"{medals[i]}  {name}",
                font=("Helvetica", 12, "bold"),
                fg=self.text,
                bg=self.card,
                anchor="w"
            ).grid(
                row=i,
                column=0,
                padx=20,
                pady=8,
                sticky="w"
            )

            tk.Label(
                score_box,
                text=f"{score} boxes",
                font=("Helvetica", 12, "bold"),
                fg=self.player_colors[
                    self.players.index(name)
                ],
                bg=self.card
            ).grid(
                row=i,
                column=1,
                padx=20,
                pady=8
            )

        button_frame = tk.Frame(
            popup,
            bg=self.bg
        )
        button_frame.pack(pady=25)

        tk.Button(
            button_frame,
            text="🌸 Play Again",
            command=lambda: [
                popup.destroy(),
                self.show_start_screen()
            ],
            font=("Helvetica", 11, "bold"),
            fg="white",
            bg=self.dark_pink,
            activebackground="#C63E75",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(side="left", padx=5)

        tk.Button(
            button_frame,
            text="Close",
            command=popup.destroy,
            font=("Helvetica", 11),
            fg=self.dark_pink,
            bg=self.light_pink,
            activebackground="#F9CCDC",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=9
        ).pack(side="left", padx=5)

    # ========================================================
    # UTILITIES
    # ========================================================

    @staticmethod
    def distance_to_segment(px, py, x1, y1, x2, y2):

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5

        t = (
            (px - x1) * dx +
            (py - y1) * dy
        ) / (dx * dx + dy * dy)

        t = max(0, min(1, t))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return (
            (px - closest_x) ** 2 +
            (py - closest_y) ** 2
        ) ** 0.5

    @staticmethod
    def lighten(hex_color, amount=0.7):

        hex_color = hex_color.lstrip("#")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        r = int(r + (255 - r) * amount)
        g = int(g + (255 - g) * amount)
        b = int(b + (255 - b) * amount)

        return f"#{r:02x}{g:02x}{b:02x}"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    game = DotsAndBoxes(root)
    root.mainloop()
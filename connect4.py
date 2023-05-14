from os import name
import tkinter as tk
import csv
from tkinter import messagebox

class Connect4:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.board = [[0 for _ in range(7)] for _ in range(6)]
        self.turn = 1
        self.players = []
        self.winner = None
        self.logfile = "connect4_log.csv"

        # it asks for player names
        self.names_frame = tk.Frame(self.root)
        self.names_frame.pack(padx=50, pady=20)
        tk.Label(self.names_frame, text="Player A:").grid(row=0, column=0)
        self.player_a_entry = tk.Entry(self.names_frame)
        self.player_a_entry.grid(row=0, column=1)
        tk.Label(self.names_frame, text="Player B:").grid(row=1, column=0)
        self.player_b_entry = tk.Entry(self.names_frame)
        self.player_b_entry.grid(row=1, column=1)
        tk.Button(self.names_frame, text="Submit", command=self.submit_names).grid(row=2, column=0, columnspan=2)

        self.game_window = None

    def submit_names(self):
        player_a_name = self.player_a_entry.get()
        player_b_name = self.player_b_entry.get()

        if player_a_name == "" or player_b_name == "":
            tk.messagebox.showerror("Error", "Please enter both player names.")
            return

        self.players = [player_a_name, player_b_name]
        with open(self.logfile, mode='a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([player_a_name, player_b_name])

        # remove name frame
        self.names_frame.destroy()
        self.show_game_window()

    def show_game_window(self):
        # create the game window
        self.game_window = tk.Frame(self.root)
        self.game_window.pack()

        # create board
        self.board_frame = tk.Frame(self.game_window)
        self.board_frame.pack()
        self.buttons = []
        for row in range(6):
            row_buttons = []
            for col in range(7):
                button = tk.Button(self.board_frame, text=" ", width=4, height=2,
                                   command=lambda row=row, col=col: self.make_move(row, col))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.turn_label = tk.Label(self.game_window, text=f"It is {self.players[self.turn-1]}'s turn.")
        self.turn_label.pack()

        # exit button
        tk.Button(self.game_window, text="Exit", command=self.root.destroy).pack()
        # make the button that will show top 5
        tk.Button(self.game_window, text="Show Top 5", command=self.display_top5).pack()

    def make_move(self, row, col):
        if self.winner:
            return

        # checks column
        if self.board[0][col] != 0:
            return

        # lowest empty row, x and o used instead of colors because of mac compatibility and tkinter
        for i in range(5, -1, -1):
            if self.board[i][col] == 0:
                self.board[i][col] = self.turn
                self.buttons[i][col].configure(text="X" if self.turn == 1 else "O")
                self.check_winner()
                self.turn = 2 if self.turn == 1 else 1
                self.turn_label.configure(text=f"It is {self.players[self.turn-1]}'s turn.")
                return

    def check_winner(self):
        # check horizontal lines
        for row in range(6):
            for col in range(4):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3] != 0:
                    self.winner = self.board[row][col]
                    self.log_winner()
                    self.show_winner()
                    return

        # check vertical lines
        for row in range(3):
            for col in range(7):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] != 0:
                    self.winner = self.board[row][col]
                    self.log_winner()
                    self.show_winner()
                    return

        # check diagonal lines (top-left to bottom-right)
        for row in range(3):
            for col in range(4):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != 0:
                    self.winner = self.board[row][col]
                    self.log_winner()
                    self.show_winner()
                    return

        # check diagonal lines (bottom-left to top-right)
        for row in range(3, 6):
            for col in range(4):
                if self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3] != 0:
                    self.winner = self.board[row][col]
                    self.log_winner()
                    self.show_winner()
                    return

        # check if its tie
        if all(self.board[0]):
            self.winner = 0
            self.log_winner()
            self.show_winner()
            return

    def show_winner(self):
        if self.winner == 0:
            tk.messagebox.showinfo("Connect 4", "It's a tie!")
        else:
            tk.messagebox.showinfo("Connect 4", f"Player {self.winner} has won!")
        self.reset_board()

    def reset_board(self):
        for row in range(6):
            for col in range(7):
                self.board[row][col] = 0
                self.buttons[row][col].configure(bg="white", text=" ")
        self.turn = 1
        self.winner = None

    def log_winner(self):
        if self.players:
            winner_name = self.players[self.winner - 1]
            loser_name = self.players[2 - self.winner]
            with open(self.logfile, mode='a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([winner_name, loser_name, self.winner])

    def display_top5(self):
        if not self.players:
            tk.messagebox.showinfo("Connect 4", "Please enter the names of the players first.")
            return

        # read the log file and count the wins for each player
        wins = {}
        with open(self.logfile, mode='r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                winner_name = row[0]
                if winner_name not in wins:
                    wins[winner_name] = 0
                wins[winner_name] += 1

        # sort the players by wins and display the top 5
        top5 = sorted(wins.items(), key=lambda x: x[1], reverse=True)[:5]
        message = "Top 5 Players:\n"
        for i, (name, win_count) in enumerate(top5):
            message += f"{i+1}. {name} - {win_count} wins\n"
        tk.messagebox.showinfo("Connect 4", message)

root = tk.Tk()
Connect4(root)
root.mainloop()
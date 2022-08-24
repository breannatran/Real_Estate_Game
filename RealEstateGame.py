# Author: Breanna Tran
# GitHub username: breannatran
# Date: 6/3/2022
# Description: A Real Estate Game that is a simplified version of the game Monopoly

class Player:
    """
    A class to represent a player by their name, balance, and index on the game board. Used by the RealEstateGame class.
    """
    def __init__(self, name, balance):
        """The constructor for Player class. Takes player's unique name and initial account balance as parameters.
        Initializes private data members representing player's name, balance, and index on the game board. All
        players start at 'GO', which is index 0."""
        self._player_name = name            # represents player's name
        self._player_balance = balance      # represents player's balance
        self._space_index = 0               # represents index of where the player is on the game board

    def get_player_name(self):
        """Returns player name."""
        return self._player_name

    def get_player_balance(self):
        """Returns player balance."""
        return self._player_balance

    def get_space_index(self):
        """Returns index of player's location on game board."""
        return self._space_index

    def set_player_balance(self, change):
        """Updates player balance by adding change amount to current balance. Rent and space price have been stored
        as negative values."""
        self._player_balance = self._player_balance + change

    def set_space_index(self, index):
        """Updates player's location to index."""
        self._space_index = index


class Space:
    """
    A class to represent a space on the game board. Used by the RealEstateGame class.
    """
    def __init__(self, rent):
        """The constructor for Space class. Takes cost of rent of that space as a parameter. Initializes private
        data members for the space's price, rent, and owner. When created, the space does not have an owner and owner
        is set to None."""
        self._price = 5 * rent              # represents the price to purchase the space
        self._rent = rent                   # represents the cost of rent
        self._owner = None                  # represents the owner of the space

    def get_price(self):
        """Returns price of space."""
        return self._price

    def get_rent(self):
        """Returns rent for space."""
        return self._rent

    def get_owner(self):
        """Returns owner of space."""
        return self._owner

    def set_owner(self, name):
        """Sets owner of space. Takes player name as a parameter."""
        self._owner = name


class RealEstateGame:
    """
    A class to represent the Real Estate Game, played by two or more players.
    """
    def __init__(self):
        """The constructor for the RealEstateGame class. Takes no parameters. Initializes the board array and
        player dictionary as private data members."""
        self._game_board = []  # game board is represented by an array
        self._players = {}     # players are stored in a dictionary with player name as key and Player object as value

    def create_spaces(self, go_reward, rent_array):
        """Fills game board with a total of 25 spaces. Takes in the amount given when passing 'GO' and the array of
        length 24 with rent values for each space as parameters. Uses Space class."""

        """Create 'GO' space. Sets rent amount to go_reward."""
        self._game_board.append(Space(go_reward))

        """Create game spaces from array of rent amounts by looping through the rent_array and creating a space for
        each item. Rent and price are stored as negative values in the Space object."""
        for amount in rent_array:
            self._game_board.append(Space(-1 * amount))

    def create_player(self, name, balance):
        """Creates player. Takes in player name and starting balance as parameters. Adds player to players dictionary
        with player name as the key and Player object as the value."""
        """Checks if player name is already a key in players dictionary."""
        if name in self._players.keys():
            print("Player name is already taken.")
        else:
            self._players[name] = Player(name, balance)

    def get_player_account_balance(self, name):
        """Returns player's balance by using method from Player class."""
        return self._players[name].get_player_balance()

    def get_player_current_position(self, name):
        """Returns player's current position by using method from Player class."""
        return self._players[name].get_space_index()

    def buy_space(self, name):
        """Method for a player purchasing a space."""
        """Checks if player is at the 'GO' space which can't be purchased."""
        if self._players[name].get_space_index() == 0:
            print(name + " is on the 'GO' space, which cannot be purchased.")
            return False

        """Checks if the player has an account balance greater than the purchase price and the space doesn't
        already have an owner."""
        """Checks if the space already has an owner."""
        if self._game_board[self.get_player_current_position(name)].get_owner() is not None:
            print("This space is already owned by a player.")
            return False

        elif self.get_player_account_balance(name) < self._game_board[self._players[name].get_space_index()] \
                .get_price() * -1:  # Checks if the player has enough money to purchase space.
            print(name + " does not have enough money to purchase this space.")
            return False

        else:  # Case where space is not yet owned and player has enough money to purchase space.
            """Deduct the purchase price of the space from the player's balance."""
            self._players[name].set_player_balance(self._game_board[self.get_player_current_position(name)].get_price())

            """Set the owner of the current space by using method from Space class."""
            self._game_board[self._players[name].get_space_index()].set_owner(name)
            return True

    def move_player(self, name, moves):
        """Method for a player moving along game board."""
        """Check player's balance and return immediately if balance is zero."""
        if self.get_player_account_balance(name) == 0:
            return

        """Check that the number of moves is between 1 and 6 and is an integer"""
        if 1 <= moves <= 6 and isinstance(moves, int):
            new_index = int(self._players[name].get_space_index() + moves)

            """Check if player passes 'GO'"""
            if new_index > 24:  # Case where player passes 'GO'

                """Add amount of reward for passing 'GO' to player's balance"""
                self._players[name].set_player_balance(self._game_board[0].get_rent())

                """Update player's location on the board"""
                new_index -= 25
                self._players[name].set_space_index(new_index)

            else:  # Case where player does not pass 'GO'
                """Update player's location on the board"""
                self._players[name].set_space_index(new_index)

            """Check if player needs to pay rent. First checks if space is owned by another player."""
            if self._game_board[new_index].get_owner() is not None and self._game_board[new_index].get_owner() != name:

                """Checks if player's balance is less than rent."""
                if self.get_player_account_balance(name) <= -1 * self._game_board[new_index].get_rent():

                    """Sets player's balance to zero."""
                    rent_paid = -1 * self._players[name].get_player_balance()

                    """Removes player as the owner of any spaces."""
                    for index in range(1, len(self._game_board)):
                        if self._game_board[index].get_owner() == name:
                            self._game_board[index].set_owner(None)

                    """Displays message that player has been eliminated."""
                    print(name + " has been eliminated from the game.")

                else:
                    """Else occurs when player's balance is greater than rent."""
                    rent_paid = self._game_board[new_index].get_rent()

                """Deducts rent amount from player's balance."""
                self._players[name].set_player_balance(rent_paid)

                """Adds paid rent to owner's balance."""
                self._players[self._game_board[new_index].get_owner()].set_player_balance(-1 * rent_paid)
        else:
            print("Number of moves must be an integer from 1 to 6. " + name + " stayed at current location.")

    def check_game_over(self):
        """Checks if the game is over by checking if there is only one player left with a balance greater than zero"""
        contenders = 0
        return_value = ''
        winner_name = ''

        """Loops through dictionary of players and increments contenders when players have a balance greater than
        zero"""
        for key in self._players:
            if self.get_player_account_balance(key) > 0:
                contenders += 1

                """Reassigns value of local variable winner_name to the name of the last player checked with a 
                balance greater than zero"""
                winner_name = key

        """If contenders equals 1, there is exactly one player that has a balance greater than zero, so the winner_name
        is the name of this person."""
        if contenders == 1:
            return_value = winner_name
            print("Winner: ")

        return return_value

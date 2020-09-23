from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import (ListProperty, NumericProperty)
from kivy.uix.modalview import ModalView


class GridEntry(Button):
	coords = ListProperty([0,0])

class TicTacToeApp(App):
	def build(self):
		return TicTacToeGrid()

class TicTacToeGrid(GridLayout):
	status = ListProperty([0, 0, 0, 
						   0, 0, 0,
						   0, 0, 0])

	current_player = NumericProperty(1)

	def __init__ (self, *args, **kwargs):
		super(TicTacToeGrid, self).__init__(*args,**kwargs)


		for row in range(3):
			for column in range(3):
				grid_entry = GridEntry(
					coords = (row, column))
				grid_entry.bind(on_release = self.button_pressed)
				self.add_widget(grid_entry)

	def button_pressed(self, button):
		#Create player symbol and colour lookups
		player = {1: 'N', -1: 'P'}
		colors = {1: (253, 0, 228, 1 ), -1: (253, 215, 0, 1)} # (r, g, b ,a)

		row, column = button.coords # The pressed button is automatically
									# passed as an argument

		# Convert 2D grid coordinates to 1D status index:
		status_index = 3*row + column
		already_played = self.status[status_index]

		# If nobody has played here yet, make a new move
		if not already_played:
			self.status[status_index] = self.current_player
			button.text = {1: 'N' , -1 : 'P'}[self.current_player]
			button.background_color = colors[self.current_player]
			self.current_player *= -1 # Switch current player

	def on_status(self, instance, new_value):
		status = new_value

		# Sum each row, col and diag
		# Could be shorter, but let's be extra
		# clear what's going on

		sums = [#rows
				sum(status[0:3]),
				#columns
				sum(status[3:6]),
				sum(status[6:9]),
				sum(status[0::3]),
				#diagonals
				sum(status[1::3]), 
				sum(status[2::3]),
				sum(status[::4]),
				sum(status[2:-2:2])]
		# Sums can only be +-3 if one player
		# filled the whole line

		winner = ''
		if 3 in sums:
			winner = '{} win!'.format('Nitya')
		elif -3 in sums:
			winner = '{} win!'.format('Pranav')
		elif 0 not in self.status: #Grid full
			winner = 'Draw...Nobody wins!'

		if winner:
			popup = ModalView(size_hint = (0.75 , 0.5 ))
			victory_label = Label(text = winner, font_size = 50)
			popup.add_widget(victory_label)
			popup.bind(on_dismiss = self.reset)
			popup.open()

	def reset(self, *args):
		self.status = [0 for _ in range(9)]

		#self.children is a list containing all child widgets
		for child in self.children:
			child.text = ''
			child.background_color = (1, 1, 1, 1) # r g b a

		self.current_player = 1



if __name__ == "__main__":
		TicTacToeApp().run()

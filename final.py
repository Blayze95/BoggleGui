"""Michael Chung - mjc13b"""
from PyQt5 import QtWidgets as Wid
from PyQt5 import QtCore as Core
from PyQt5 import QtGui as ui
import sys
import pickle
import string
import time
import boggle3 as Boggle

class GameWindow(Wid.QMainWindow):
	def __init__(self, file = None):
		Wid.QMainWindow.__init__(self)
		self.setup(file)

	def setup(self, file = None):
		self.setWindowTitle("Boggle")
		self.setToolTip("Detective Conan is the best long running anime")
		self.game = BoggleGame(self, file)
		self.setFixedSize(800, 600)
		self.setCentralWidget(self.game)
		start_new = Wid.QAction('Start New Game', self)
		save_game = Wid.QAction("Save Game", self)
		load_game = Wid.QAction("Load Game", self)
		exit_action = Wid.QAction('Exit', self)
		exit_action.triggered.connect(Wid.qApp.quit)
		start_new.triggered.connect(self.restart)
		save_game.triggered.connect(self.savegame)
		load_game.triggered.connect(self.loadgame)

		menubar = self.menuBar()
		menubar.setNativeMenuBar(False)
		file = menubar.addMenu('Game')
		file.addAction(start_new)
		file.addAction(save_game)
		file.addAction(load_game)
		file.addAction(exit_action)



		self.show()

	@Core.pyqtSlot()
	def loadgame(self):
		self.loadmenu = Wid.QDialog()
		scroll = Wid.QScrollArea()
		lay = Wid.QGridLayout()
		select = Wid.QPushButton()
		menulist = Wid.QListWidget()
		select.setText("Select")
		try:
			file = open("save.sav", 'r')
			up = pickle.Unpickler(file)
			s = up.load()
			#print(s.keys())
			file.close()
			for x in s:
			#	print(x)
				item = Wid.QListWidgetItem(x)
				menulist.addItem(item)


		except IOError:
			print("Messed up")

		def selected():
			print(s[menulist.item(menulist.currentRow()).text()])
			self.game.stopgame()
			self.game = BoggleGame(self, s[menulist.item(menulist.currentRow()).text()])
			self.setCentralWidget(self.game)

		select.clicked.connect(selected)
		#self.loadmenu.addWidget(scroll)

		
		#scrollContent = Wid.QWidget(scroll)
		#scrollLayout = Wid.QVBoxLayout(scrollContent)
		self.loadmenu.setLayout(lay)
		lay.addWidget(menulist, 1, 1, 1, 1)
		lay.addWidget(select, 2, 1, 1, 1)

		self.loadmenu.show()
		#How do I create a scrolling menu with clickable elements?

		


	@Core.pyqtSlot()
	def savegame(self):
		self.game.timer.timer.stop()
		savedata = {time.strftime("%c"): {"board": self.game.gameboard.board, "time": self.game.timer.time, "user": self.game.wordlist.toPlainText()}}
		self.game.enterButton.setText("Resume")
		self.game.line.setReadOnly(True)
		self.game.enterButton.clicked.connect(self.game.startgame)
		try:
			file = open("save.sav", 'r')
			up = pickle.Unpickler(file)
			s = up.load()
			print(savedata.keys()[0])
			s[savedata.keys()[0]] = savedata[savedata.keys()[0]]
			file = open("save.sav", 'w')
			p = pickle.Pickler(file, 0)
			p.dump(s)
			for x in s:
				print(x)

		except IOError:
			file = open("save.sav", 'w')
			p = pickle.Pickler(file, 0)
			p.dump(savedata)
			print(savedata)

		#self.savedisplay = Wid.QWidget()
		#savetext = Wid.QLabel()
		#savetext.setText("Your game has been saved.")
		#savetext.setFont(ui.QFont("Times", 24))
		#lab = Wid.QGridLayout()
		#self.savedisplay.setLayout(lab)
		#self.savedisplay.resize
		#lab.addWidget(savetext)

		#self.savedisplay.show()


		#print(self.savedata)
		#print(self.game.wordlist.toPlainText().split())


	@Core.pyqtSlot()
	def restart(self):
		self.game.stopgame()
		self.game = BoggleGame(self)
		self.setCentralWidget(self.game)

class BoggleGame(Wid.QWidget):
	def __init__(self, parent, file = None):
		Wid.QWidget.__init__(self, parent)
		self.parent = parent
		self.setup(file)

	def setup(self, file = None):
		self.gameboard = Boggle.Boggle()
		if file != None:
			self.gameboard.board = file["board"]

		self.board = DiceArrangement(self, self.gameboard)
		self.wordlist = WordDisplay(self)
		if file != None:
			self.wordlist.append(file["user"])

		self.enterButton = EnterButton(self, "Start")
		self.enterButton.setAutoDefault(True)
		self.line = WordInput(self, self.wordlist)
		self.line.setReadOnly(True)
		self.enterButton.clicked.connect(self.startgame)
		self.line.returnPressed.connect(self.enterButton.click)
		if file != None:
			self.timer = Timer(self, file["time"])

		else:
			self.timer = Timer(self)

		self.timer.timer.timeout.connect(self.countdown)

		#self.quitgame3 = QuitButton(self)
		#self.quitgame4 = QuitButton(self)
		self.grid = Wid.QGridLayout()
		self.setLayout(self.grid)

		self.grid.addWidget(self.board, 1, 1, 4, 4)
		self.grid.addWidget(self.wordlist, 1, 5, 1, 1, Core.Qt.AlignRight)
		#self.grid.addWidget(self.quitgame, 2, 2, 1, 1)
		self.grid.addWidget(self.timer, 5, 5, 1, 1, Core.Qt.AlignRight)
		self.grid.addWidget(self.enterButton, 5, 4, 1, 1)
		#self.grid.addWidget(self.quitgame3, 1, 5, 1, 1)
		self.grid.addWidget(self.line, 5, 1, 1, 3)
	#	self.grid.addWidget(self.quitgame4, 1, 5, 1, 1)


	@Core.pyqtSlot()
	def countdown(self):
		if self.line.isReadOnly() == False:
			self.timer.time = self.timer.time - 1
			self.timer.setText("Time Left: {}".format(self.timer.time))

		if self.timer.time <= 0:
			self.timer.timer.stop()
			self.scorewindow = Wid.QWidget()
			self.line.setReadOnly(True)
			score_label = Wid.QLabel()
			score_label.setFont(ui.QFont("Times", 24, ui.QFont.Bold))
			display = Wid.QGridLayout()
			start_new = StartButton(self)
			quit = QuitButton(self)
			start_new.clicked.connect(self.parent.restart)
			quit.clicked.connect(Wid.qApp.quit)

			score_label.setText("Score: {}".format(self.gameboard.score(self.wordlist.toPlainText().split())))
			self.scorewindow.setLayout(display)
			display.addWidget(score_label, 1, 1, 1, 2, Core.Qt.AlignCenter)
			display.addWidget(start_new, 2, 1, 1, 1, Core.Qt.AlignCenter)
			display.addWidget(quit, 2, 2, 1, 1, Core.Qt.AlignCenter)

			self.scorewindow.show()

	@Core.pyqtSlot()
	def startgame(self):
		self.enterButton.setText("Enter")
		self.enterButton.clicked.connect(self.passWord)
		self.timer.timer.start(1000)
		self.line.setReadOnly(False)

	@Core.pyqtSlot()
	def passWord(self):
		if self.line.isReadOnly() == False:
			test = "{}".format(self.line.text())
			if test != "" and test != "\r" and test != "\n":	
				self.wordlist.append(test)
			self.line.setText("")

	def stopgame(self):
		self.timer.timer.stop()
		self.line.setReadOnly(True)


class EnterButton(Wid.QPushButton):
	def __init__(self, parent, text):
		Wid.QPushButton.__init__(self, parent)
		self.setText(text)
		self.resize(self.sizeHint())

class DiceArrangement(Wid.QWidget):
	def __init__(self, parent, gameb):
		Wid.QWidget.__init__(self, parent)
		self.gameboard = gameb
		self.vbox = Wid.QGridLayout()
		self.resize(self.sizeHint())
		self.setLayout(self.vbox)
		self.dice = []
		self.vbox.setProperty("coloredcell", True)
		#self.vbox.setStyleSheet("background-color: white")
		for x in self.gameboard.board:
			self.dice.append(Die(self, x[0]))

		self.place()

	def place(self):
		c = 1
		r = 1
		for x in self.dice:
			if r == 5:
				r = 1
				c += 1
			self.vbox.addWidget(x, c, r, 1, 1, Core.Qt.AlignCenter)
			r += 1



class StartButton(Wid.QPushButton):
	def __init__(self, parent):
		Wid.QPushButton.__init__(self, parent)
		self.setText("New Game")
		
		self.resize(self.sizeHint())

class LoadButton(Wid.QPushButton):
	def __init__(self, parent):
		Wid.QPushButton.__init__(self, parent)
		self.setText("Load Game")
		
		self.resize(self.sizeHint())


class QuitButton(Wid.QPushButton):
	def __init__(self, parent):
		Wid.QPushButton.__init__(self, parent)
		self.setText("Quit")
		self.clicked.connect(Wid.qApp.quit)
		self.setToolTip("Yare Yare")
		self.resize(self.sizeHint())

class WordInput(Wid.QLineEdit):
	def __init__(self, parent, words):
		Wid.QLineEdit.__init__(self, parent)
		self.resize(self.sizeHint())


class Die(Wid.QLabel):
	def __init__(self, parent, lab = "T"):
		Wid.QLabel.__init__(self, parent)
		self.font = ui.QFont("Times", 36, ui.QFont.Bold)
		self.setFont(self.font)
		self.setStyleSheet("color: black")
		self.setText(lab)
		self.resize(self.sizeHint())

class Timer(Wid.QLabel):
	def __init__(self, parent, time = 180):
		Wid.QLabel.__init__(self, parent)
		self.setFont(ui.QFont("Times", 24, ui.QFont.Bold))
		self.time = time
		self.setText("Time Left: {}".format(self.time))
		self.resize(self.sizeHint())
		self.timer = Core.QTimer(self)
		

class WordDisplay(Wid.QTextEdit):
	def __init__(self, parent):
		Wid.QTextEdit.__init__(self, parent)
		self.resize(self.sizeHint())
		self.setReadOnly(True)

class introGameWindow(Wid.QWidget):
	def __init__(self):
		Wid.QWidget.__init__(self)
		self.screen = Wid.QGridLayout()
		self.resize(self.sizeHint())
		self.title = Wid.QLabel()
		self.title.setFont(ui.QFont("Times", 72, ui.QFont.Bold))
		self.title.setText("Boggle")
		self.start = StartButton(self)
		self.loadgame = LoadButton(self)
		self.start.clicked.connect(self.startg)
		self.loadgame.clicked.connect(self.loadgames)
		self.quit = QuitButton(self)
		self.setLayout(self.screen)
		#self.load = 

		self.screen.addWidget(self.title, 1, 1, 1, 3, Core.Qt.AlignCenter)
		self.screen.addWidget(self.start, 2, 1, 1, 1)
		self.screen.addWidget(self.loadgame, 2, 2, 1, 1)
		self.screen.addWidget(self.quit, 2, 3, 1, 1)

		self.show()

	@Core.pyqtSlot()
	def startg(self):
		self.close()
		self.screen = GameWindow()

	@Core.pyqtSlot()
	def loadgames(self):
		self.loadmenu = Wid.QDialog()
		scroll = Wid.QScrollArea()
		lay = Wid.QGridLayout()
		select = Wid.QPushButton()
		menulist = Wid.QListWidget()
		select.setText("Select")
		try:
			file = open("save.sav", 'r')
			up = pickle.Unpickler(file)
			s = up.load()
			#print(s.keys())
			file.close()
			for x in s:
			#	print(x)
				item = Wid.QListWidgetItem(x)
				menulist.addItem(item)


		except IOError:
			print("Messed up")

		def selected():
			print(s[menulist.item(menulist.currentRow()).text()])
			#self.game.stopgame()
			self.close()
			self.screen = GameWindow(s[menulist.item(menulist.currentRow()).text()])
			#self.game = BoggleGame(self, s[menulist.item(menulist.currentRow()).text()])
			#.setCentralWidget(self.game)

		select.clicked.connect(selected)
		#self.loadmenu.addWidget(scroll)

		
		#scrollContent = Wid.QWidget(scroll)
		#scrollLayout = Wid.QVBoxLayout(scrollContent)
		self.loadmenu.setLayout(lay)
		lay.addWidget(menulist, 1, 1, 1, 1)
		lay.addWidget(select, 2, 1, 1, 1)

		self.loadmenu.show()
		
class loadButton(Wid.QWidget):
	def __init__(self, parent):
		wid.QWidget.__init__(self, parent)

if __name__ == "__main__":
	app = Wid.QApplication(sys.argv)
	main_window = introGameWindow()
	app.exec_()

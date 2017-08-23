from __future__ import print_function
"""Michael Chung - mjc13b"""
"""Thank you for being the best teacher I have had while I have been at FSU"""
"""Godd Luck in your studies!"""


import random
import enchant




class Boggle(object):
	def __init__(self):
		self.die1 = tuple([['A'], ['E'], ['A'], ['N'], ['E'], ['G']])
		self.die2 = tuple([['A'], ['H'], ['S'], ['P'], ['C'], ['O']])
		self.die3 = tuple([['A'], ['S'], ['P'], ['F'], ['F'], ['K']])
		self.die4 = tuple([['O'], ['B'], ['J'], ['O'], ['A'], ['B']])
		self.die5 = tuple([['I'], ['O'], ['T'], ['M'], ['U'], ['C']])
		self.die6 = tuple([['R'], ['Y'], ['V'], ['D'], ['E'], ['L']])
		self.die7 = tuple([['L'], ['R'], ['E'], ['I'], ['X'], ['D']])
		self.die8 = tuple([['E'], ['I'], ['U'], ['N'], ['E'], ['S']])
		self.die9 = tuple([['W'], ['N'], ['G'], ['E'], ['R'], ['H']])
		self.die10 = tuple([['L'], ['N'], ['H'], ['N'], ['R'], ['Z']])
		self.die11 = tuple([['T'], ['S'], ['T'], ['I'], ['Y'], ['D']])
		self.die12 = tuple([['O'], ['W'], ['T'], ['I'], ['Y'], ['D']])
		self.die13 = tuple([['E'], ['R'], ['T'], ['T'], ['Y'], ['L']])
		self.die14 = tuple([['T'], ['O'], ['E'], ['S'], ['S'], ['I']])
		self.die15 = tuple([['T'], ['E'], ['R'], ['W'], ['H'], ['V']])
		self.die16 = tuple([['N'], ['U'], ['I'], ['H'], ['M'], ['Qu']])
		self.dieList = [self.die1, self.die2, self.die3, self.die4, self.die5, self.die6, self.die7, self.die8, 
			self.die9, self.die10, self.die11, self.die12, self.die13, self.die14, self.die15, self.die16]
		self.board = []
		self.inEnglish = enchant.Dict("en_us")
		self.user = []
		self.random_die_order()


	def random_die_order(self):
		g_List = []
		for x in self.dieList:
			g_List.append(random.choice(x))
			#print(g_List)
		random.shuffle(g_List)
		self.board = g_List

	def find_word(self, word, diceLoc):
		revWord = list()
		skip = 0
		for i in range(0, len(word)):
			#print(word[i])
			if skip == 1:
				skip = 0
				continue
			
			if word[i] == 'Q' and word[i+1] == 'U':
				skip = 1
				revWord.append(["Qu"])

			else:
				revWord.append([word[i]])

		revWord.reverse()
		#print(revWord)
		restore = list(revWord)
		usedList = set()
		index = 0

		for x in diceLoc:
			#print(x, end=" = ")
			#print(revWord[len(revWord) - 1])
			if revWord[len(revWord) - 1] == x:
				#print("\tMatched")
				usedList.add(index)
				if False == self.find_path(revWord, diceLoc, index, usedList):
					usedList.remove(index)

				else:
					return True
					
			index = index + 1

		return False

	def addword(self, word):
		if word not in self.user:
			self.user.extend(word)

	def find_path(self, word, diceLoc, curIndex, usedIndex):

		keep = list(word)
		keep.pop()

		#print(keep)
		if len(keep) <= 0:
			#("Word was found")
			return True
			

		offset = range(-5, 6)

		for x in offset:

			if (curIndex + x) < 0 or (curIndex + x) > 15:
				continue

			if x == 2 or x == -2 or x == 0:
				continue

			if curIndex == 0:
				if x == 3:
					continue

			elif curIndex == 3 or curIndex == 7 or curIndex == 11:
				if x == -3 or x == 1 or x == 5:
					continue

			elif curIndex == 4 or curIndex == 8 or curIndex == 12:
				if x == -1 or x == 3 or x == -5:
					continue

			elif curIndex == 15:
				if x == -3:
					continue

			if (curIndex + x) in usedIndex:
				continue

			#print("Index: ", end = "")
			#print(curIndex + x, end = ", ")
			#print(diceLoc[curIndex + x])

			if diceLoc[curIndex + x] == keep[len(keep) - 1]:
				usedIndex.add(curIndex + x)
				if False == self.find_path(keep, diceLoc, (curIndex + x), usedIndex):
					usedIndex.remove(curIndex + x)
					#print("Word not found")
				else:
					return True

		return False

	def score(self, userList):
		scored = 0
		scoreds = []
		for ucheck in userList:
			#print(ucheck, end = ": ")

			if self.inEnglish.check(ucheck.upper()) == True:
				
				if len(ucheck) < 3:
					##print("The word ", end = "")
					#print(ucheck, end = "")
					#print("is not long enough.")
					continue

				elif ucheck in scoreds:
					#print("The word ", end = "")
					#print(ucheck, end = " ")
					#print("has already been scored.")
					continue
					
				else:
					if self.find_word(ucheck.upper(), self.board) == True:
						scoreds.append(ucheck)
						#print("The word ", end = "")
						#print(ucheck, end = " ")
						#print("is worth ", end = "")

						if len(ucheck) == 3 or len(ucheck) == 4:
							#print("1", end = "")
							scored += 1

						elif len(ucheck) == 5:
							#print("2", end = "")
							scored += 2

						elif len(ucheck) == 6:
							#print("3", end = "")
							scored += 3

						elif len(ucheck) == 7:
							#print("5", end == "")
							scored += 5

						elif len(ucheck) >= 8:
							#print("11", end = "")
							scored += 11

						#print(" points!")

		return scored

if __name__ == "__main__":
	gameDice = random_die_order(dieList)
	random.shuffle(gameDice)
	random.shuffle(gameDice)
	i = 0
	print("")
	for x in gameDice:
		for y in x:
			print("[", end = "")
			print(y, end = "")
			print("]", end = " ")
		if i == 3:
			i = 0
			print("\n")
			continue
		i = i + 1

	print("Please enter your words! Press 'Enter' between words. Finish by typing 'x':")
	
	userWord = str()
	userList = list()
	scored = set()
	score = 0
	while True:
		userWord = raw_input("> ")
		if userWord.lower() == 'x':
			break

		elif len(userWord) <= 0:
			continue

		else:
			userList.append(userWord)

	#for x in userList:
		#print(x)

	

	

	print("\nYour total score is: ", end = "")
	print(score)
	
	#for x in userList:
		#find_word(x.upper(), gameDice)

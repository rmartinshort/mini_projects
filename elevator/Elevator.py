#!/usr/bin/env python
#RMS 2018

#Simple elevator class 

#The elevator will start at the specified floor, an will go up and down. It lets people 
#off on their desired floor and checks if more want to get on.

#Commands are issued before the elevator starts, they are carried out when the simulate 
#method is called 

import time 
import numpy as np

class Elevator:

	def __init__(self,nfloors,startfloor):

		self.totalfloors = nfloors
		self.onfloor = startfloor
		self.max_capacity = 3

		if 0 <= self.onfloor < nfloors:
			self.direction = 1 #going up
		elif self.onfloor == nfloors:
			self.direction = -1 #going down
		else:
			raise ValueError("startfloor must be within building!")

		self.nextfloor = self.onfloor

		self.embarkdestinations = []
		self.disembarkdestinations = []
		self.inelevator = []
		self.number_in_elevator = 0

	def call(self,floors):

		'''Customer calls elevator to floor x, destination y 
		floors is [x,y]'''

		print("Called to floor %s, destination %s" %(floors[0],floors[1]))

		self.embarkdestinations.append(floors[0])
		self.disembarkdestinations.append(floors[1])
		self.inelevator.append(False)

	def move(self):

		self.onfloor = self.nextfloor
		print("On floor %i" %self.onfloor)

		if self.onfloor in self.embarkdestinations:

			#indices of potentially embarking customers
			embarking = [i for i in range(len(self.embarkdestinations)) if self.embarkdestinations[i] == self.onfloor]

			#these customers are now in the elevator
			for index in embarking:
				if self.inelevator[index] == False:

					overweight = self.check_overweight()

					if overweight == False:
						print("Doors opening: Customer calling to %s embarks" %self.onfloor)
						self.number_in_elevator += 1
						self.inelevator[index] = True

		if self.onfloor in self.disembarkdestinations:

			#indices of potentially disembarking customers
			disembarking = [i for i, e in enumerate(self.disembarkdestinations) if e == self.onfloor]

			#print('Inelevator: %s' %self.inelevator)

			for index in disembarking:

				#Check if customer is in the elevator: If so, disembark
				if self.inelevator[index] == True:
					print("Doors opening: Customer with destination %s disembarks" %self.onfloor)
					self.disembarkdestinations[index] = np.nan
					self.number_in_elevator -= 1 
					self.inelevator[index] = 'Left'

		#update the value of nextfloor and change direction if needed
		self.check_dirchange()

	def check_overweight(self):

		'''Check if the elevator is at maximum capacity'''

		if self.number_in_elevator == self.max_capacity:

			print("At capacity: Need to wait until elevator returns for more space")
			return 1 
		else:
			return 0 

	def check_dirchange(self):

		'''Check if we need to change direction'''

		if self.onfloor == self.totalfloors:

			print('GOING DOWN')

			self.direction = -1

		elif self.onfloor == 0:

			print('GOING UP')

			self.direction = 1

		self.nextfloor = self.onfloor + self.direction

	def simulate(self):

		'''Starts elevator simulation'''

		print("Start on floor %s" %self.onfloor)

		while np.nansum(self.disembarkdestinations) != 0:

			self.move()
			time.sleep(0.5)

		print("Stopped on floor %s" %self.onfloor)


if __name__ == '__main__':

	myElevator = Elevator(10,0)

	print('-----------------------------------')
	myElevator.call([4,1])
	myElevator.call([4,3])
	myElevator.call([4,8])
	myElevator.call([2,9])
	myElevator.call([9,2])
	myElevator.call([9,9])
	myElevator.call([10,1])
	myElevator.call([4,5])
	myElevator.call([0,7])
	print('-----------------------------------')

	myElevator.simulate()

import os
import math
import re as rgx

class DataLoader:
	def __init__(self, directory = os.getcwd()+"\\data\\"):
		self.directory = directory
		self.data = []
		self.refinedData = []
		for file in os.listdir(directory):
			self.loadFile(os.path.join(directory, file))

		self.refinedData = self.data

	def loadFile(self, fileName, hasHeader = True):
		with open(fileName, "r") as file:
			for line in file:
				convertedData = DataItem(line)
				if convertedData.converted:
					self.data.append(convertedData)

	def refineData(self, 	startLocation = "000000", endLocation = "999999", 
							startDay = "Monday", endDay = "Sunday", 
							startTime = 0, endTime = 500340):

		timeRange = range(startTime, endTime + 1)

		days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
		dayRange = []
		removeDay = True
		for day in days:
			if day == startDay:
				removeDay = False
			elif day == endDay:
				dayRange.append(day)
				removeDay = True
			if not removeDay:
				dayRange.append(day)

		locationXRange = range(int(startLocation[0:3]), int(endLocation[0:3]) + 1)
		locationYRange = range(int(startLocation[3:6]), int(endLocation[3:6]) + 1)

		self.refinedData = []

		for item in self.data:
			if item.time not in timeRange:
				continue
			if item.day not in dayRange:
				continue
			if int(item.location[0:3]) not in locationXRange:
				continue
			if int(item.location[3:6]) not in locationYRange:
				continue
			self.refinedData.append(item)


	def outputData(self, fileName):
		with open(fileName+".csv", "w") as file:
			file.write("Day,Time,Temperature (°C),Wind speed (mph),Location (six-figure grid reference),\n")
			for item in self.refinedData:
				file.write(str(item))

	def calculateStats(self):
		stats = {}

		tempTotal = 0
		temperatures = []
		speedTotal = 0
		speeds = []
		for item in self.refinedData:
			tempTotal += item.temperature
			temperatures.append(item.temperature)
			speedTotal += item.windSpeed
			speeds.append(item.windSpeed)
		temperatures.sort()
		speeds.sort()

		stats.update({	"temperatureAverage":(tempTotal/len(self.refinedData)),
						"windSpeedAverage":(speedTotal/len(self.refinedData)),
						"temperatureRange":(temperatures[len(temperatures) - 1] - temperatures[0]),
						"windSpeedRange":(speeds[len(speeds) - 1] - speeds[0])
						})

		return stats
		

class DataItem:
	def __init__(self, data):
		self.converted = True
		#Split the data based on commas
		data = data.split(",")
		#Check that the first item is a day, if it is not. The data is not what we want.
		self.day = self.checkDay(data[0])
		self.time = self.convertTime(data[1])
		self.temperature = self.checkTemperature(data[2])
		self.windSpeed = self.checkWindSpeed(data[3])
		self.location = self.checkLocation(data[4])

	def __str__(self):
		return ("""{},{},{},{},{},\n""".format(	self.day.strip(),
												self.time,
												str(self.temperature),
												str(self.windSpeed),
												self.location))

	def checkDay(self, day):
		days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
		if day.lower() in days:
			return day
		else:
			self.converted = False
			return None

	def convertTime(self, time):
		result = rgx.match("([0-1]?[0-9]|2[0-3]):[0-5][0-9]", time)
		if not result:
			self.converted = False
			return 0
		hours = int(time[0:2])
		minutes = int(time[3:5])
		seconds = (minutes * 60) + (hours * 360)
		return seconds

	def checkTemperature(self, temperature):
		try:
			return float(temperature)
		except ValueError:
			self.converted = False


	def checkWindSpeed(self, windSpeed):
		try:
			return float(windSpeed)
		except ValueError:
			self.converted = False

	def checkLocation(self, location):
		if len(location) != 6:
			self.converted = False
		return location

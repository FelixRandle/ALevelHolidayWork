from datahandler import DataLoader
from os import system
import re as rgx

def pprint(data):
	print("{}".format(data.center(120)), end = "\n")

def clear():
	system("cls")

def locationInput(default):
	while True:
		pprint("Please enter a location. It should appear as a 6 figure grid reference.")
		pprint("If you wish to use default values, please enter nothing")
		userInput = input()
		if userInput == "":
			clear()
			return default
		if len(userInput) != 6:
			clear()
			pprint("The length of your grid reference should be 6 characters")
			continue
		try:
			int(userInput)
			clear()
			return userInput
		except ValueError:
			clear()
			pprint("Please enter integer values. Not characters.")
			continue

def dayInput(default):
	days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	while True:
		pprint("Please enter a day. It should be spelt correctly.")
		pprint("If you wish to use default values, please enter nothing")
		userInput = input().title()
		if userInput == "":
			clear()
			return default
		if userInput in days:
			return userInput
		else:
			clear()
			pprint("Please enter a valid day of the week. E.g. Monday")

def timeInput(default):
	pattern = rgx.compile("([0-1]?[0-9]|2[0-3]):[0-5][0-9]")
	while True:
		pprint("Please enter a time. It should be in 24Hr time format.")
		pprint("If you wish to use default values, please enter nothing")
		userInput = input()
		if userInput == "":
			clear()
			return default
		result = pattern.match(userInput)
		if not result:
			clear()
			pprint("Your input was not in 24Hr time format. E.g. 08:45")
		else:
			clear()
			hours = int(userInput[0:2])
			minutes = int(userInput[3:5])
			seconds = (minutes * 60) + (hours * 360)
			return seconds

def mainloop():
	exit = False
	clear()
	while not exit:
		pprint("Weather Station")
		pprint("Welcome to the weather station data handler.")
		pprint("If you are unsure what commands are available, type 'help'")
		userInput = input().lower()

		if userInput in ("help", "h"):
			printHelp()
		elif userInput in ("output", "o"):
			outputData()
		elif userInput in ("refine", "r"):
			refineData()
		elif userInput in ("stats", "s"):
			showStats()
		elif userInput in ("quit", "q"):
			quit()
		else:
			clear()
			pprint("Sorry, but '{}' is not a recognised command\n".format(userInput))


def printHelp():
	clear()
	pprint("Available Commands:")
	pprint("'Help'/'H' Displays this help menu.")
	pprint("'Output'/'O' Used to output all data to a single file.")
	pprint("'Refine'/'R' Used to refine data based on location or date and time.")
	pprint("'Stats'/'S' Used to give statistics such as median and mean on current data.")
	pprint("'Quit'/'Q' Used to quit the program.\n")
	

def outputData():
	clear()
	pprint("This command will output all currently refined data to a csv file and overwrite any data currently in that file.")
	pprint("Please enter the name you would like the file to take.")
	pprint("If you would no longer like to complete this action. Please type 'cancel'")
	userInput = input()
	if userInput.lower() == "cancel":
		return
	else:
		clear()
		data.outputData(userInput)
		pprint("Successfully wrote data to file {}.csv".format(userInput))
		pprint("\n\n\n")

def refineData():
	clear()
	pprint("START LOCATION:")
	startLocation = locationInput("000000")
	pprint("END LOCATION:")
	endLocation = locationInput("999999")
	pprint("START DAY:")
	startDay = dayInput("Monday")
	pprint("END DAY:")
	endDay = dayInput("Sunday")
	pprint("START TIME:")
	startTime = timeInput("0")
	pprint("END TIME:")
	endTime = timeInput("500340")
	data.refineData(startLocation, endLocation, startDay, endDay, startTime, endTime)

def showStats():
	stats = data.calculateStats()
	clear()
	pprint("Statistics for currently refined data are as follows:")
	pprint("Average Temperature - {:.2f}".format(stats["temperatureAverage"]))
	pprint("Temperature Range - {:.2f}".format(stats["temperatureRange"]))
	pprint("Average Wind Speed - {:.2f}".format(stats["windSpeedAverage"]))
	pprint("Wind Speed Range - {:.2f}".format(stats["windSpeedRange"]))
	print("\n\n\n")


if __name__ == "__main__":
	global data
	data = DataLoader()
	mainloop()
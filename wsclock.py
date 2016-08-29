# Jose Alfredo Valles Salas

# Working Set Clock Page Replacement Algorithm

import sys
import os.path

# A simple class to keep track of the pages
# in memory and their reference / modified bit.
class mempage:
	value = 0 # The page number.
	refer = 1 # Referenced bit.
	modif = 0 # Modified bit.
	time = 0 # Time of last used.

def diskWrite():
	print "Writing to disk."

# Since apparently objects can't be easily found in a list,
# this function does the job. It takes the page and the memory list,
# and checks to see if the page is already in the list.
def exists(page, schedule, instruction):
	for i in range(len(schedule)):
		if page.value == schedule[i].value:
			schedule[i].refer = 1
			if instruction == 'W':
				schedule[i].modif = 1
			return True
	return False

if len(sys.argv) != 4:
	print "Usage: $ python optimal.py <Number of physical memory pages> <tau> <access sequence file>"
	sys.exit()

fname = str(sys.argv[3])

if os.path.isfile(fname) == False:
	print "%s is not a real file, or I can't find it..." % fname
	sys.exit()

numbpages = int(sys.argv[1])
tau = int(sys.argv[2])
schedule = []

pagefault = 0
# We will use the system clock along with the 
# tau value to determine which page to replace.
# The system clock will advance by 1 every time the arrow
# is moved.
sysclock = 0
# This arrow will keep track of which element
# we're looking at in memory at that moment.
arrow = 0 

with open(fname, "r") as f:
	pages = f.read()
	# Make a list of the pages by splitting
	# what was in the file using the spaces.
	pages = pages.split(" ")
	# Now, let's work with each page individually.
	for i in range(len(pages)):
		page = mempage()
		temp = pages.pop(0)
		# This time we care about the instructions,
		# so save them to check if it's read or write later.
		instruction, val = temp.split(":")
		page.value = int(val)
		# If the page isn't in memory, let's see what we
		# can do about it.
		found = exists(page, schedule, instruction)
		if found == False:
			# If we still have space, then just add it.
			if len(schedule) < numbpages:
				# If the instruction is W, then the M bit
				# is set to 1. Save the current system clock time
				# with the page, and advance the arrow and the clock.
				if instruction == 'W':
					page.modif = 1
				page.time = sysclock
				schedule.append(page)
				arrow = (arrow + 1) % numbpages
				sysclock += 1
				
			# Else, let's see what we can replace.
			else:
				# Check each element in memory individually, and
				# decide which one to remove depending on their M bit and
				# R bit values. If we find one that is dirty (M bit set to 1),
				# then write it to disk and move on. If we find one that is
				# referenced (R bit set to 1), then set the current clock time and
				# set the R bit to 0. If neither of these conditions is met, then
				# check the page's age to see if it's older than the tau. If so,
				# remove it. With each condition check, the clock and arrow are
				# advanced.
				while True:
					if schedule[arrow].refer == 1 and schedule[arrow].modif == 1:
						schedule[arrow].refer = 0
						schedule[arrow].modif = 0
						diskWrite()
						schedule[arrow].time = sysclock
					elif schedule[arrow].refer == 1:
						schedule[arrow].refer = 0
						schedule[arrow].time = sysclock
					elif schedule[arrow].modif == 1:
						diskWrite()
						schedule[arrow].modif = 0
						schedule[arrow].time = sysclock
					elif (sysclock - schedule[arrow].time) > tau:
						schedule[arrow].value = page.value
						schedule[arrow].time = sysclock
						sysclock += 1
						arrow = (arrow + 1) % numbpages
						break
					sysclock += 1
					arrow = (arrow + 1) % numbpages					
			pagefault += 1
	print pagefault
	f.close()
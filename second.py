# Jose Alfredo Valles Salas

# Second Chance Page Replacement Algorithm

import sys
import os.path
import collections

# A simple class to keep track of the pages
# in memory and their reference bit.
class mempage:
	value = 0
	refer = 1

# Since apparently objects can't be easily found in a list,
# this function does the job. It takes the page and the memory list,
# and checks to see if the page is already in the list.
def exists(page, schedule):
	for i in range(len(schedule)):
		if page.value == schedule[i].value:
			schedule[i].refer = 1
			return True
	return False

if len(sys.argv) != 3:
	print "Usage: $ python optimal.py <Number of physical memory pages> <access sequence file>"
	sys.exit()

fname = str(sys.argv[2])

if os.path.isfile(fname) == False:
	print "%s is not a real file, or I can't find it..." % fname
	sys.exit()

numbpages = int(sys.argv[1])
schedule = []

pagefault = 0

with open(str(sys.argv[2]), "r") as f:
	pages = f.read()
	# Make a list of the pages by splitting
	# what was in the file using the spaces.
	# Since we don't care about the read or write
	# instructions for this algorithm, we'll
	# just store the value.
	pages = pages.split(" ")
	pages = [int(i.split(":")[1]) for i in pages]
	# Now, let's work with each page individually.
	for i in range(len(pages)):
		page = mempage()
		# print "Pages: %r" % pages
		page.value = int(pages.pop(0))

		# If the page isn't in memory, let's see what we
		# can do about it.
		if exists(page, schedule) == False:
			# If we still have space, then just add it.
			if len(schedule) < numbpages:
				schedule.append(page)
				# print "New schedule: %r" % [j.value for j in schedule]
				# print "Reference bits: %r" % [j.refer for j in schedule]
			# Else, let's see what we can replace.
			else:
				# Check each element in memory individually
				# to see which one has a reference bit set to 0.
				# If it's set to 1, then set the bit to 0,
				# and move it to the end of the list.
				for m in range(len(schedule)):
					if schedule[0].refer == 1:
						schedule[0].refer = 0
						remove = schedule.pop(0)
						# print "What I'm removing: %r" % remove.value
						schedule.append(remove)
						# print "New schedule: %r" % [j.value for j in schedule]
						# print "Reference bits: %r" % [j.refer for j in schedule]
						# If all of the reference bits in the list were set to 1 when we checked,
						# then they are all reset to 0, and we still have to insert the new page,
						# so insert into the end of the list.
						if m == (len(schedule) - 1):
							schedule.pop(0)
							schedule.append(page)
							# print "New schedule: %r" % [j.value for j in schedule]
							# print "Reference bits: %r" % [j.refer for j in schedule]
						continue
					# Else, remove the first page we find with a
					# reference bit set to 0.
					schedule.pop(0)
					schedule.append(page)
					# print "New schedule: %r" % [j.value for j in schedule]
					# print "Reference bits: %r" % [j.refer for j in schedule]
					break
			pagefault += 1
	print pagefault
	f.close()
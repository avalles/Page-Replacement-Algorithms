# Jose Alfredo Valles Salas

# Optimal Page Replacement Algorithm

import sys
import os.path

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
		# print pages
		# Get the next value in the list read from the file.
		value = int(pages.pop(0))

		# If the page isn't in memory, let's see what we
		# can do about it.
		if value not in schedule:
			# If we still have space, then just add it.
			if len(schedule) < numbpages:
				schedule.append(value)
				# print "New schedule: %r" % schedule
			# Else, let's see what we can replace.
			else:
				# We're gonna try to find the page that is referenced the furthest
				# in the list we read from the file in order to determine which to eliminate.
				# If the page is never referenced again, then we remove it. Else, we remove the one
				# who is furthest away.
				farthest = 0
				index = 0

				# Check each element in memory individually
				# to see which one will be referenced in the future,
				# and see which one will be referenced the farthest.
				for i in range(len(schedule)):
					try:
						# Try to find it and get its index. If not, an exception is raised.
						index = pages.index(schedule[i])
					except Exception as e:
						# If it isn't found, then we remove that value
						# and insert the new page into memory since it
						# will never be referenced again. The index in this case will be -1.
						index = -1
						schedule[i] = value
						# print "New schedule: %r" % schedule
						break
					# Now let's check which page is referenced
					# the farthest into the list we read.
					if index >= farthest:
						farthest = index
						remove = i
				# If the pages were all found in the list,
				# then remove the one that will be referenced
				# the furthest into the future, and insert the
				# new page into memory.
				if index != -1:
					schedule[remove] = value
					# print "New schedule: %r" % schedule
			pagefault += 1
	print pagefault
	f.close()
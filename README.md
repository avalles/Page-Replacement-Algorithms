# Page Replacement Algorithms:

The purpose of these three scripts is to simulate the `Optimal`, `Second Chance`, and `Working Set Clock` page replacement algorithms.

---------------------------------------------------------------
### Optimal:

**Usage:**
```
$ python optimal.py <Number of physical memory pages> <access sequence file>
```

The number of physical memory pages corresponds to the amount of pages that can be in memory at any given time.

#### Algorithm:
We have a set of pages that want to use up space in memory. If the page isn't in the current space, then it is a page fault and we must determine which current page to replace. If there is still space in memory, then add it. If not, then we must determine which of the current pages in memory will be referenced furthest in the future, if at all. The page that will never be referenced again or is referenced furthest in the future is replaced by the new page.

---------------------------------------------------------------
### Second Chance:

**Usage:**
```
$ python second.py <Number of physical memory pages> <access sequence file>
```

The number of physical memory pages corresponds to the amount of pages that can be in memory at any given time.

#### Algorithm:
We have a set of pages that want to use up space in memory. If the page isn't in the current space, then it is a page fault and we must determine which current page to replace. We will always verify the first element in memory. If its reference bit is set to 1, then we move it to the end of the list in memory and set the reference bit to 0. Else, we remove it.

---------------------------------------------------------------
### Working Set Clock:

**Usage:**
```
$ python wsclock.py <Number of physical memory pages> <tau> <access sequence file>
```

The number of physical memory pages corresponds to the amount of pages that can be in memory at any given time.

The "tau" value is used to compare the age of the page stored in memory to the current system clock time. If the page is older than the tau value, then it is removed since it is no longer in the working set.

#### Algorithm:
We have a set of pages that want to use up space in memory. If the page isn't in the current space, then it is a page fault and we must determine which current page to replace. A hardware system clock is simulated, as well as an arrow to point to each page in memory we want to check at the current tick of the clock. If the page has its reference bit set to 1, then reset it to 0, set the page's time to the current clock time, and move the arrow to the next page. If the modified bit is set to 1, the page is dirty and we must write it to disk. Then, set the modified bit to 0, set the page's time to the current clock time, and move the arrow to the next page. Continue until the algorithm finds a page that has not been referenced and is not dirty. If so, then check to see if the page's age is greater than the "tau" value. If so, replace it, else, move the arrow and advance the clock until a suitable page is found.

>>> from booking import *
>>> random.seed(137)
>>> system = Booking.load_system()
>>> len(system.hotels)
2
>>> system.hotels[0].name
'The Great Northern Hotel'
>>> system = Booking.load_system()
>>> len(system.hotels)
2
>>> system.hotels[0].name
'The Great Northern Hotel'


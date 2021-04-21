>>> from room import *
>>> my_room = Room('Double', 237, 99.99)
>>> str(my_room)
'Room 237,Double,99.99'
>>> r = Room("Queen", 105, 80.0)
>>> r.set_up_room_availability(['May', 'Jun'], 2021)
>>> r.set_up_room_availability(['Feb'], 2020)
>>> len(r.availability)
3
>>> len(r.availability[(2021, 6)])
31
>>> r.availability[(2021, 5)][5]
True
>>> print(r.availability[(2021, 5)][0])
None
>>> len(r.availability[(2020, 2)])
30


"Room::obj->reserve room"
>>> r = Room("Queen", 105, 80.0)
>>> r.set_up_room_availability(['May', 'Jun'], 2021)
>>> date1 = datetime.date(2021, 6, 20)
>>> r.reserve_room(date1)
>>> r.availability[(2021, 6)][20]
False
>>> r.availability[(2021, 5)][3] = False
>>> date2 = datetime.date(2021, 5, 3)
>>> r.reserve_room(date2)
Traceback (most recent call last):
AssertionError: The room is not available at the given date


"Room::obj->make available"
>>> r = Room("Queen", 105, 80.0)
>>> r.set_up_room_availability(['May', 'Jun'], 2021)
>>> date1 = datetime.date(2021, 6, 20)
>>> r.make_available(date1)
>>> r.availability[(2021, 6)][20]
True
>>> r.availability[(2021, 5)][3] = False
>>> date2 = datetime.date(2021, 5, 3)
>>> r.make_available(date2)
>>> r.availability[(2021, 5)][3]
True


"Room::obj->is_available"
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
>>> date1 = datetime.date(2021, 5, 25)
>>> date2 = datetime.date(2021, 6, 10)
>>> r1.is_available(date1, date2)
True
>>> r1.availability[(2021, 5)][28] = False
>>> r1.is_available(date1, date2)
False


"Room->find_available_room"
>>> r1 = Room("Queen", 105, 80.0)
>>> r2 = Room("Twin", 101, 55.0)
>>> r3 = Room("Queen", 107, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> r2.set_up_room_availability(['May'], 2021)
>>> r3.set_up_room_availability(['May'], 2021)
>>> r1.availability[(2021, 5)][8] = False
>>> r = [r1, r2, r3]
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
>>> my_room == r3
True
>>> r3.availability[(2021, 5)][3] = False
>>> my_room = Room.find_available_room(r, 'Queen', date1, date2)
>>> print(my_room)
None
>>> r = Room("King", 110, 120.0)
>>> r.set_up_room_availability(['Dec'], 2021)
>>> r.set_up_room_availability(['Jan'], 2022)
>>> date1 = datetime.date(2021, 12, 20)
>>> date2 = datetime.date(2022, 1, 8)
>>> my_room = Room.find_available_room([r], 'Queen', date1, date2)
>>> print(my_room)
None
>>> my_room = Room.find_available_room([r], 'King', date1, date2)
>>> my_room == r
True

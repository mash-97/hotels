>>> from hotel import *
>>> from reservation import *
>>> from room import *
>>> random.seed(987)
>>> Reservation.booking_numbers = []
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> h = Hotel("Secret Nugget Hotel", [r1])
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> h.make_reservation("Mrs. Santos", "Queen", date1, date2)
1953400675629
>>> print(h.reservations[1953400675629])
Booking number: 1953400675629
Name: Mrs. Santos
Room reserved: Room 105,Queen,80.0
Check-in date: 2021-05-03
Check-out date: 2021-05-10


"Hotel::object->get_reciept"
>>> r1 = Room("Queen", 105, 80.0)
>>> r2 = Room("Twin", 101, 55.0)
>>> r3 = Room("Queen", 107, 80.0)
>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
>>> r2.set_up_room_availability(['May', 'Jun'], 2021)
>>> r3.set_up_room_availability(['May', 'Jun'], 2021)
>>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
>>> h.get_receipt([num1])
560.0
>>> date3 = datetime.date(2021, 6, 5)
>>> num2 = h.make_reservation("Mrs. Santos", "Twin", date1, date3)
>>> h.get_receipt([num1, num2])
2375.0
>>> h.get_receipt([123])
0.0


"Hotel::object->get_reservation_for_booking_number"
>>> random.seed(137)
>>> Reservation.booking_numbers = []
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> h = Hotel("Secret Nugget Hotel", [r1])
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
>>> rsv = h.get_reservation_for_booking_number(num1)
>>> print(rsv)
Booking number: 4191471513010
Name: Mrs. Santos
Room reserved: Room 105,Queen,80.0
Check-in date: 2021-05-03
Check-out date: 2021-05-10

"Hotel::object->cancel_reservation"
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> h = Hotel("Secret Nugget Hotel", [r1])
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> num1 = h.make_reservation("Mrs. Santos", "Queen", date1, date2)
>>> h.cancel_reservation(num1)
>>> num1 in h.reservations
False
>>> r1.availability[(2021, 5)][4]
True


"Hotel::object->get_available_room_types"
>>> r1 = Room("Queen", 105, 80.0)
>>> r2 = Room("Twin", 101, 55.0)
>>> r3 = Room("Queen", 107, 80.0)
>>> r1.set_up_room_availability(['May', 'Jun'], 2021)
>>> r2.set_up_room_availability(['May', 'Jun'], 2021)
>>> r3.set_up_room_availability(['May', 'Jun'], 2021)
>>> h = Hotel("Secret Nugget Hotel", [r1, r2, r3])
>>> types = h.get_available_room_types()
>>> types.sort()
>>> types
['Queen', 'Twin']


"Hotel->load_hotel_info_file"
>>> hotel_name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
>>> hotel_name
'Overlook Hotel'
>>> print(len(rooms))
500
>>> print(rooms[236])
Room 237,Twin,99.99
>>> type(rooms[499])==Room
True
>>> all(map(lambda r: type(r)==Room, rooms))
True


"Hotel::obj->save_hotel_info_file"
>>> r1 = Room("Double", 101, 99.99)
>>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
>>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
>>> h.save_hotel_info_file()
>>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
>>> fobj.read()
'Queen Elizabeth Hotel\nRoom 101,Double,99.99\n'
>>> fobj.close()


"Hotel::obj->load_reservation_strings_for_month"
>>> name, rooms = Hotel.load_hotel_info_file('hotels/overlook_hotel/hotel_info.txt')
>>> h = Hotel(name, rooms, {})
>>> rsvs = h.load_reservation_strings_for_month('overlook_hotel', 'Oct', 1975)
>>> rsvs[237] == [(1975, 'Oct', 1, ''), (1975, 'Oct', 2, ''), (1975, 'Oct', 3, ''), (1975, 'Oct', 4, ''), (1975, 'Oct', 5, ''), (1975, 'Oct', 6, ''), (1975, 'Oct', 7, ''), (1975, 'Oct', 8, ''), (1975, 'Oct', 9, ''), (1975, 'Oct', 10, ''), (1975, 'Oct', 11, ''), (1975, 'Oct', 12, ''), (1975, 'Oct', 13, ''), (1975, 'Oct', 14, ''), (1975, 'Oct', 15, ''), (1975, 'Oct', 16, ''), (1975, 'Oct', 17, ''), (1975, 'Oct', 18, ''), (1975, 'Oct', 19, ''), (1975, 'Oct', 20, ''), (1975, 'Oct', 21, ''), (1975, 'Oct', 22, ''), (1975, 'Oct', 23, ''), (1975, 'Oct', 24, ''), (1975, 'Oct', 25, ''), (1975, 'Oct', 26, ''), (1975, 'Oct', 27, ''), (1975, 'Oct', 28, ''), (1975, 'Oct', 29, ''), (1975, 'Oct', 30, '9998701091820--Jack'), (1975, 'Oct', 31, '9998701091820--Jack')]
True


"Hotel::obj->save_reservations_for_month"
>>> random.seed(987)
>>> r1 = Room("Double", 237, 99.99)
>>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
>>> Reservation.booking_numbers = []
>>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
>>> date1 = datetime.date(2021, 10, 30)
>>> date2 = datetime.date(2021, 12, 23)
>>> num = h.make_reservation("Jack", "Double", date1, date2)
>>> h.save_reservations_for_month('Oct', 2021)
>>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
>>> fobj.read()
'237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\n'
>>> fobj.close()


"Hotel::obj->save_hotel"
>>> random.seed(987)
>>> Reservation.booking_numbers = []
>>> r1 = Room("Double", 237, 99.99)
>>> r1.set_up_room_availability(['Oct', 'Nov', 'Dec'], 2021)
>>> h = Hotel("Queen Elizabeth Hotel", [r1], {})
>>> date1 = datetime.date(2021, 10, 30)
>>> date2 = datetime.date(2021, 12, 23)
>>> h.make_reservation("Jack", "Double", date1, date2)
1953400675629
>>> h.save_hotel()
>>> fobj = open('hotels/queen_elizabeth_hotel/hotel_info.txt', 'r')
>>> fobj.read()
'Queen Elizabeth Hotel\nRoom 237,Double,99.99\n'
>>> fobj.close()
>>> fobj = open('hotels/queen_elizabeth_hotel/2021_Oct.csv', 'r')
>>> fobj.read()
'237,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,1953400675629--Jack,1953400675629--Jack\n'
>>> fobj.close()


"Hotel->load_hotel"
>>> random.seed(137)
>>> Reservation.booking_numbers = []
>>> hotel = Hotel.load_hotel('overlook_hotel')
>>> hotel.name
'Overlook Hotel'
>>> str(hotel.rooms[236])
'Room 237,Twin,99.99'
>>> print(hotel.reservations[9998701091820])
Booking number: 9998701091820
Name: Jack
Room reserved: Room 237,Twin,99.99
Check-in date: 1975-10-30
Check-out date: 1975-12-24

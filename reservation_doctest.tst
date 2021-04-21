>>> from room import *
>>> from reservation import *
>>> random.seed(987)
>>> Reservation.booking_numbers = []
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
>>> print(my_reservation.check_in)
2021-05-03
>>> print(my_reservation.check_out)
2021-05-10
>>> my_reservation.booking_number
1953400675629
>>> r1.availability[(2021, 5)][9]
False

"Reservation::object->__str__"
>>> random.seed(987)
>>> Reservation.booking_numbers = []
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
>>> print(my_reservation)
Booking number: 1953400675629
Name: Mrs. Santos
Room reserved: Room 105,Queen,80.0
Check-in date: 2021-05-03
Check-out date: 2021-05-10


"Reservation::object->to_short_string"
>>> random.seed(987)
>>> Reservation.booking_numbers = []
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 10)
>>> my_reservation = Reservation('Mrs. Santos', r1, date1, date2)
>>> my_reservation.to_short_string()
'1953400675629--Mrs. Santos'

"Reservation::object->from_short_string"
>>> Reservation.booking_numbers = []
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(['May'], 2021)
>>> date1 = datetime.date(2021, 5, 3)
>>> date2 = datetime.date(2021, 5, 4)
>>> my_reservation = Reservation.from_short_string('1953400675629--Mrs. Santos', date1, date2, r1)
>>> print(my_reservation.check_in)
2021-05-03
>>> print(my_reservation.check_out)
2021-05-04
>>> my_reservation.booking_number
1953400675629
>>> r1.availability[(2021, 5)][3]
False

"Reservation->get_reservations_from_row"
>>> random.seed(987)
>>> Reservation.booking_numbers = [] # needs to be reset for the test below to pass
>>> r1 = Room("Queen", 105, 80.0)
>>> r1.set_up_room_availability(MONTHS, 2021)
>>> rsv_strs = [(2021, 'May', 3, '1953400675629--Jack'), (2021, 'May', 4, '1953400675629--Jack')]
>>> rsv_dict = Reservation.get_reservations_from_row(r1, rsv_strs)
>>> print(rsv_dict[1953400675629])
Booking number: 1953400675629
Name: Jack
Room reserved: Room 105,Queen,80.0
Check-in date: 2021-05-03
Check-out date: 2021-05-05

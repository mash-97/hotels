import datetime
import random 

import room as room_mod


class Reservation:
  booking_numbers = []
  
  def __init__(self, name, room_reserved, check_in_date, check_out_date, booking_number=None):
    if not room_reserved.is_available(check_in_date, check_out_date):
      raise AssertionError("Room not available at the specified dates!")
    if booking_number != None and booking_number in type(self).booking_numbers:
      raise AssertionError("Provided booking number is already in use!")
    if booking_number != None and len(str(booking_number))!=13:
      raise AssertionError("Provided booking number's length not satisfied!")
    
    self.name = name 
    self.room_reserved = room_reserved 
    self.check_in = check_in_date 
    self.check_out = check_out_date 
    self.booking_number = booking_number 
    
    # generate a new 13 digits booking number if not provided
    if self.booking_number == None:
      self.booking_number = type(self).new_booking_number()
      type(self).booking_numbers.append(self.booking_number)

    # update booking number into the class attribute
    
    
    # reserve specified room for all nights from the check_in_date(included) to the 
    # check_out_night(excluded)
    self.room_reserved.reserve_room_for(self.check_in, self.check_out)
  
  def __str__(self):
    _str_ = "Booking number: {0}\nName: {1}\nRoom reserved: {2}\nCheck-in date: {3}\nCheck-out date: {4}"
    return _str_.format(self.booking_number, self.name, self.room_reserved, self.check_in, self.check_out)
  
  
  def to_short_string(self):
    return "{bn}--{name}".format(bn=self.booking_number, name=self.name)
  
  def reservation_price(self):
    days = (self.check_out - self.check_in).days 
    return self.room_reserved.price*days 
  
  # generate new random booking number that don't exist in booking_numbers 
  @staticmethod
  def new_booking_number():
    while True:
      number = random.randrange(10**12, 10**13)
      if not number in Reservation.booking_numbers:
        break
    return number 
  
  # returns a dict mapping booking_number to the associated reservation
  # tuples in the input supposed to be come from Hotel.load_reservation_strings_for_month
  @staticmethod
  def get_reservations_from_row(room, tuples):
    rvs_dict = {}

    for tupl in tuples:
      t_year, t_month, t_day, short_string = tupl 
      if short_string==None or len(short_string)==0: continue
      
      t_month = room_mod.get_month_no(t_month)
      
      bn,name = short_string.split("--")
      bn = int(bn)
      
      date = datetime.date(t_year, t_month, t_day)
      if bn in rvs_dict.keys():
        if rvs_dict[bn]["minimum_date"] > date:
          rvs_dict[bn]["minimum_date"] = date
	  
        elif rvs_dict[bn]["maximum_date"] < date:
          rvs_dict[bn]["maximum_date"] = date 
	
      else: 
        rvs_dict[bn] = {"minimum_date": date, "maximum_date": date, "name": name}
    
    for bn in rvs_dict.keys():
      rvs_dict[bn] = Reservation(
				  rvs_dict[bn]["name"], 
				  room, 
				  rvs_dict[bn]["minimum_date"], 
				  rvs_dict[bn]["maximum_date"]+datetime.timedelta(1),   # seems to have typo in problem example
				  bn
				)
    return rvs_dict
				  
  @classmethod
  def from_short_string(cls, short_string, check_in, check_out, room):
    booking_number_str, name = short_string.split("--")
    return Reservation(name, room, check_in, check_out, int(booking_number_str))
  

if __name__ == "__main__":
  import doctest 
  doctest.testfile("reservation_doctest.tst", verbose=True)
  

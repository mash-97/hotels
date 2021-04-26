import datetime
import random 

from room import *

# ==============================================================================================
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# get month no from month string
def helper_get_month_no(month_s):
  for i,ms in enumerate(MONTHS):
    if ms==month_s:
      return i+1
  return None

# get month str from month not
def helper_get_month_str(month_no):
  return MONTHS[month_no-1]

# check if the year is a leap year
def helper_is_leap(year):
  helper_is_leap_year = False
  if year%400==0: helper_is_leap_year = True
  elif year%100==0: helper_is_leap_year = False
  elif year%4==0: helper_is_leap_year = True
  return helper_is_leap_year

# get days of the month 
def helper_get_days_of_the_month(year, month):
  days = DAYS_PER_MONTH[month-1]
  # check for leap year and if the month is Feb
  if helper_is_leap(year) and month==2:
    days = 29
  return days
  

# get days of all the months of the year
def helper_get_days_of_months(year):
  days = DAYS_PER_MONTH.copy()
  if helper_is_leap(year):
    days[1] = 29
  return days
# ==============================================================================================


class Reservation:
  booking_numbers = []
  
  # Initialize a reservation
  # name:str -> name of the person room reserved for
  # room_reserved:Room -> room that is reserved
  # check_in:date, check_out:date
  # booking_number:int
  def __init__(self, name, room_reserved, check_in, check_out, booking_number=None):
    if not room_reserved.is_available(check_in, check_out):
      raise AssertionError("Room not available at the specified dates!")
    if booking_number != None and booking_number in type(self).booking_numbers:
      raise AssertionError("Provided booking number is already in use!")
    if booking_number != None and len(str(booking_number))!=13:
      raise AssertionError("Provided booking number's length not satisfied!")
    
    self.name = name 
    self.room_reserved = room_reserved 
    self.check_in = check_in
    self.check_out = check_out
    self.booking_number = booking_number 
    
    # generate a new 13 digits booking number if not provided
    if self.booking_number == None:
      self.booking_number = type(self).helper_new_booking_number()
      type(self).booking_numbers.append(self.booking_number)


    # update booking number into the class attribute
    
    
    # reserve specified room for all nights from the check_in_date(included) to the 
    # check_out_night(excluded)
    type(self).helper_reserve_room_for(self.room_reserved, self.check_in, self.check_out)


  """ purpose made """
  # check_in (date), check_out (date)
  @staticmethod
  def helper_reserve_room_for(room, check_in, check_out):
    diff_td = check_out - check_in
    
    for td in range(0, diff_td.days):
      tmp_date = check_in + datetime.timedelta(td)
      room.reserve_room(tmp_date)
  
  
  def __str__(self):
    _str_ = "Booking number: %s\nName: %s\nRoom reserved: %s\nCheck-in date: %s\nCheck-out date: %s"
    return _str_%(self.booking_number, self.name, self.room_reserved, self.check_in, self.check_out)
  
  
  def to_short_string(self):
    return "%s--%s"%(self.booking_number, self.name)
  
  def reservation_price(self):
    days = (self.check_out - self.check_in).days 
    return self.room_reserved.price*days 
  
  """ purpose made """
  # generate new random booking number that don't exist in booking_numbers 
  @staticmethod
  def helper_new_booking_number():
    while True:
      number = random.randrange(10**12, 10**13)
      if not number in Reservation.booking_numbers:
        break
    return number 
  
  # returns a dict mapping booking_number to the associated reservation
  # tuples in the input supposed to be come from Hotel.load_reservation_strings_for_month

  # room (Room::obj)
  # tuples (list of tuples defining tuple(year:int, month:str, short_string:str)
  # short_string that comes from Reservation::obj->to_short_string
  @staticmethod
  def get_reservations_from_row(room, tuples):
    rvs_dict = {}

    for tupl in tuples:
      t_year, t_month, t_day, short_string = tupl 
      if short_string==None or len(short_string)==0: continue
      
      t_month = helper_get_month_no(t_month)
      
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
  # short_string:str
  # check_int:date, check_out:date
  def from_short_string(cls, short_string, check_in, check_out, room):
    booking_number_str, name = short_string.split("--")
    return Reservation(name, room, check_in, check_out, int(booking_number_str))


# ~ if __name__=="__main__":
    # ~ import doctest
    # ~ doctest.testfile("reservation_doctest.tst", verbose=True)


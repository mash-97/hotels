import datetime 

# ==============================================================================================
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
DAYS_PER_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# get month no from month string
def get_month_no(month_s):
  for i,ms in enumerate(MONTHS):
    if ms==month_s:
      return i+1
  return None

# get month str from month not
def get_month_str(month_no):
  return MONTHS[month_no-1]

# check if the year is a leap year
def is_leap(year):
  is_leap_year = False
  if year%400==0: is_leap_year = True
  elif year%100==0: is_leap_year = False
  elif year%4==0: is_leap_year = True
  return is_leap_year

# get days of the month 
def get_days_of_the_month(year, month):
  days = DAYS_PER_MONTH[month-1]
  # check for leap year and if the month is Feb
  if is_leap(year) and month==2:
    days = 29
  return days
  

# get days of all the months of the year
def get_days_of_months(year):
  days = DAYS_PER_MONTH.copy()
  if is_leap(year):
    days[1] = 29
  return days
# ==============================================================================================

class Room:
  # class attributes
  TYPES_OF_ROOMS_AVAILABLE = ['twin', 'double', 'queen', 'king']
  
  # room_type (str)
  # room_num  (int)
  # price (float/int)
  def __init__(self, room_type, room_num, price):
    
    # check if all the arguments are in correct type
    if type(room_type)!=str or type(room_num)!=int or type(price)!=float or room_num<1 or price < 0:
      raise AssertionError("argument(s) not satisfied!")
    
    self.room_type = room_type
    self.room_num = room_num
    self.price = price
    self.availability = {}
  
  def __str__(self):
    return "Room {0},{1},{2}".format(self.room_num, self.room_type, self.price)

  # months_l (list of str defining months)
  # year (int)
  def set_up_room_availability(self, months_l, year):
    for month_s in months_l:
      month = get_month_no(month_s)
      days = get_days_of_the_month(year, month)
      self.availability[(year, month)] = [None]+[True for i in range(days)]
    
  
  def reserve_room(self, date):
    if self.availability[(date.year, date.month)][date.day] == False:
      raise AssertionError("The room is not available at the given date")
    
    self.availability[(date.year, date.month)][date.day] = False
  
  
  def make_available(self, date):
    self.availability[(date.year, date.month)][date.day] = True
  
  
  # checks if the room is available for the given dates
  # check_in (date)
  # check_out (date)
  def is_available(self, check_in, check_out):
    if check_in >= check_out:
      raise AssertionError("Check in date is earlier to the check out date!")
    
    diff_td = check_out - check_in
    
    for td in range(0, diff_td.days):
      tmp_date = check_in + datetime.timedelta(td)
      available = self.availability[(tmp_date.year, tmp_date.month)][tmp_date.day]
      if not available: return False
    return True

  """ purpose made """
  # check_in (date), check_out (date)
  def reserve_room_for(self, check_in, check_out):
    diff_td = check_out - check_in
    
    for td in range(0, diff_td.days):
      tmp_date = check_in + datetime.timedelta(td)
      self.reserve_room(tmp_date)
  
  """ purpose made """
  # check_in (date), check_out (date)
  def make_available_for(self, check_in, check_out):
    diff_td = check_out - check_in
    
    for td in range(0, diff_td.days):
      tmp_date = check_in + datetime.timedelta(td)
      self.make_available(tmp_date)
  
  @staticmethod
  # rooms (Room objects)
  # room_type (str)
  # check_in (date), check_out (date)
  def find_available_room(rooms, room_type, check_in, check_out):
    if check_in >= check_out:
      raise AssertionError("Check in date is earlier to the check out date!")
    
    for room in rooms:
      if room.room_type == room_type and room.is_available(check_in, check_out):
        return room
    return None
  



import datetime 
import random
import os 
import copy
from room import *
from reservation import *



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



WRITE_END = "\n"
HOTELS_FOLDER_PATH = "hotels"
HOTEL_INFO_FILE_NAME = "hotel_info.txt"

class Hotel:

    # name:str (defines hotel name)
    # rooms:list (defines Room objects)
    # reservations:dict (booking number -> reservation)
    def __init__(self, name, rooms=[], reservations={}):
        self.name = name 
        self.rooms = copy.deepcopy(rooms)
        self.reservations = copy.deepcopy(reservations) # booking number => reservation
    
    # makes reservation for the given person_name(str), room_type(str)
    # check_in(date), check_out(date)
    def make_reservation(self, person_name, room_type, check_in, check_out):
        for room in self.rooms:
            if room.room_type==room_type and room.is_available(check_in, check_out):
                reservation = Reservation(person_name, room, check_in, check_out)
                self.reservations[reservation.booking_number] = reservation
                return reservation.booking_number 
        raise AssertionError("Room not found with the given type, check-in and check-out date!")
    
    # get recieption after booking a reservatio
    # booking_numbers(list of booking numbers)
    def get_receipt(self, booking_numbers):
        total_price = 0.0
        for bn in booking_numbers:
            if bn in self.reservations.keys():
                total_price += self.reservations[bn].reservation_price()
        return total_price
    
    def get_reservation_for_booking_number(self, booking_number):
        return self.reservations.get(booking_number, None)
    
    """ purpose made """
    # check_in (date), check_out (date)
    @staticmethod
    def helper_make_available_for(room, check_in, check_out):
        diff_td = check_out - check_in
        
        for td in range(0, diff_td.days):
            tmp_date = check_in + datetime.timedelta(td)
            room.make_available(tmp_date)
  
    # cancels reservation for the booking number
    # doesn't return anything particular
    def cancel_reservation(self, booking_number):
        reservation = self.get_reservation_for_booking_number(booking_number)
        if reservation:
            type(self).helper_make_available_for(reservation.room_reserved, reservation.check_in, reservation.check_out)
            del self.reservations[reservation.booking_number]
    
    def get_available_room_types(self):
        room_types = []
        for room in self.rooms:
            if not room.room_type in room_types:
                room_types.append(room.room_type)
        return room_types
    

    def save_hotel_info_file(self):
        hotel_info_file_path = self.helper_get_hotel_info_file_path()
        hotel_file = open(hotel_info_file_path, "w+", encoding="utf-8")
        hotel_file.write(self.name+WRITE_END)
        for room in self.rooms:
            hotel_file.write(str(room)+WRITE_END)
        hotel_file.close()
    

    # save csv file for the (month, year)
    # hard try
    def save_reservations_for_month(self, month, year):
        csv_file_path = self.helper_get_csv_file_path(month, year)
        month_num = helper_get_month_no(month)
        days = helper_get_days_of_the_month(year, month_num)
        
        csv_file = open(csv_file_path, "w", encoding="utf-8")
        for room in self.rooms:
            # ====================================> skipping rooms logic
            if not room.availability[(year, month_num)]: continue
            # ====================================> skipping rooms logic
            row = [str(room.room_num)]
            for day in range(1, days+1):
                date = datetime.date(year, month_num, day)
                for reservation in self.helper_get_reservations_for_room(room):
                    if reservation.check_in <= date < reservation.check_out:
                        row.append(reservation.to_short_string())
                    else:
                        row.append("")
            row = ",".join(row)
            csv_file.write(row+WRITE_END)
        csv_file.close()
    
    
    def save_hotel(self):
        hotel_folder_path = self.helper_get_hotel_folder_path()
        if not os.path.exists(hotel_folder_path):
            os.makedirs(hotel_folder_path)
        
        # save hotel info into hotel_info
        self.save_hotel_info_file()
        
        # process csv files
        # find unique (year,month) tuples
        year_month_tuples = {}
        for room in self.rooms:
            for ymt in room.availability.keys():
                year_month_tuples[ymt] = True
        
        for ymt in year_month_tuples.keys():
            self.save_reservations_for_month(MONTHS[ymt[1]-1], ymt[0])
        
    
    # returns a dict mapped by room_number to list of tuples of format 
    # (year, month_s, day, reservation:short_format or '')
    @staticmethod
    def load_reservation_strings_for_month(hotel_folder_name, month_s, year):
        csv_file_path = Hotel.helper_get_csv_file_path_from(hotel_folder_name, Hotel.helper_gen_csv_file_name(month_s, year))
        
        r_dict = {}
        csv_file = open(csv_file_path, "r", encoding="utf-8")
        rows = csv_file.read().split("\n")
        for row in rows:
            if len(row)==0: continue     # '' or '' at the EOF
            columns = row.split(",")
            room_number = int(columns[0])
            if not room_number in r_dict:
                r_dict[room_number] = []
            for i in range(1, len(columns)):
                r_dict[room_number].append((year, month_s, i, columns[i]))
                
        csv_file.close()
        
        return r_dict

    @staticmethod
    def load_hotel_info_file(hotel_info_file_path):
        hotel_name = None
        rooms = None
        r_rooms = []
        hotel_file = open(hotel_info_file_path, "r", encoding="utf-8")
        hotel_name, *rooms = hotel_file.read().split("\n")
        for index, room_inf in enumerate(rooms):
            if len(room_inf)==0: 
                continue
            room_inf = room_inf.split(",")
            room_num = int(room_inf[0].split(" ")[1])
            
            room_type = room_inf[1]
            room_price = float(room_inf[2])
            r_rooms.append( Room(room_type, room_num, room_price) )
        hotel_file.close()
        
        return (hotel_name, r_rooms)
    
    
    @classmethod
    def load_hotel(cls, hotel_folder_name):
        reservations = {}
        hotel_name, rooms = cls.load_hotel_info_file(cls.helper_get_hotel_info_file_path_from(hotel_folder_name))
        
        # map a dict room_nums to rooms
        rnr_dict = cls.helper_get_mapped_num_to_room(rooms)
        
        # a dict to strore room number to reservation strings
        rnrsvs_dict = {}
        
        # make a hotel folder path
        hotel_folder_path = cls.helper_get_hotel_folder_path_from(hotel_folder_name)
        
        #ymts dict mapped to csv file name
        ymts_dict = cls.helper_get_ymts_dict_from_ldir(os.listdir(hotel_folder_path))
        
        # create rooms
        for ymt in ymts_dict.keys():
            month_s = helper_get_month_str(ymt[1])
            
            tmp_rnrsvs_dict = cls.load_reservation_strings_for_month(hotel_folder_name, month_s, ymt[0])
            
            for room_num in tmp_rnrsvs_dict.keys():
                rnr_dict[room_num].set_up_room_availability([month_s], ymt[0])
            
            rnrsvs_dict = cls.helper_get_merged_reservation_strings(rnrsvs_dict, tmp_rnrsvs_dict)
            
        for room_num in rnrsvs_dict.keys():
            tmp_rsvs = Reservation.get_reservations_from_row(rnr_dict[room_num], rnrsvs_dict[room_num])
            for key in tmp_rsvs.keys():
                reservations[key] = tmp_rsvs[key]
        
        return cls(hotel_name, rooms, reservations)


    """ purpose made """
    def helper_get_hotel_info_file_path(self):
        return type(self).helper_gen_hotel_info_file_path(self.name)
    
    
    """ purpose made """
    def helper_get_csv_file_path(self, month, year):
       return type(self).helper_gen_csv_file_path(self.name, month, year)
    
    """ purpose made """
    def helper_get_reservations_for_room(self, room):
        reservations = []
        for bn in self.reservations:
            reservation = self.reservations[bn]
            if room == reservation.room_reserved:
                reservations.append(reservation)
        return reservations
    
    """ purpose made """
    def helper_get_hotel_folder_path(self):
        return type(self).helper_gen_hotel_folder_name(self.name)

    """ purpose made """
    def helper_get_hotel_folder_path(self):
        return type(self).helper_gen_hotel_folder_path(self.name)
                 
    """ purpose made """
    @classmethod
    def helper_gen_csv_file_name(cls, month_s, year):
        return "_".join([str(year), month_s])+".csv"
     
    """ purpose made """   
    @classmethod
    def helper_gen_csv_file_path(cls, hotel_name, month_s, year):
        parts = [cls.helper_gen_hotel_folder_path(hotel_name)]
        parts += [cls.helper_gen_csv_file_name(month_s, year)]
        
        return "/".join(parts)
   
    """ purpose made """
    @staticmethod
    def helper_get_merged_dict(dict_1, dict_2):
        tmp_dict = dict_1
        for key in dict_2.keys():
            tmp_dict[key] = dict_2[key]
        return tmp_dict 
    
    """ purpose made """
    @staticmethod
    def helper_get_merged_reservation_strings(dict_1, dict_2):
        tmp_dict = dict_1
        for key in dict_2.keys():
            if not key in tmp_dict.keys():
                tmp_dict[key] = []
            tmp_dict[key] += dict_2[key]
        return tmp_dict
    
    """ purpose made """
    @staticmethod
    def helper_get_mapped_num_to_room(rooms):
        tmp_dict = {}
        for room in rooms:
            tmp_dict[room.room_num] = room
        return tmp_dict
    
    """ purpose made """
    @staticmethod
    def helper_get_hotel_info_file_path_from(hotel_folder_name):
        parts = [HOTELS_FOLDER_PATH, hotel_folder_name, HOTEL_INFO_FILE_NAME]
        return "/".join(parts)
    
    """ purpose made """
    @staticmethod
    def helper_get_hotel_folder_path_from(hotel_folder_name):
        parts = [HOTELS_FOLDER_PATH, hotel_folder_name]
        return "/".join(parts)
    
    """ purpose made """
    @staticmethod
    def helper_get_ymts_dict_from_ldir(ls):
        ymt = {}
        for l in ls:
            ym, ext = l.split(".")
            try:
                if ext=="csv":
                    y,m = ym.split("_")
                    y = int(y)
                    m = helper_get_month_no(m)
                    ymt[(y,m)] = l
            except: 
                continue
        return ymt
    
    """ purpose made """
    @staticmethod
    def helper_get_csv_file_path_from(hotel_folder_name, csv_file_name):
        return "/".join([HOTELS_FOLDER_PATH, hotel_folder_name, csv_file_name])
    """ purpose made """
    @classmethod
    def helper_gen_hotel_folder_name(cls, hotel_name):
        return "_".join(hotel_name.lower().split(" "))
    

    """ purpose made """
    @classmethod
    def helper_gen_hotel_folder_path(cls, hotel_name):
        parts = [HOTELS_FOLDER_PATH, cls.helper_gen_hotel_folder_name(hotel_name)]
        return "/".join(parts)
    

    """ purpose made """
    @classmethod
    def helper_gen_hotel_info_file_path(cls, hotel_name):
        parts = [cls.helper_gen_hotel_folder_path(hotel_name), HOTEL_INFO_FILE_NAME]
        return "/".join(parts)
    


# ~ if __name__=="__main__":
    # ~ import doctest
    # ~ doctest.testfile("hotel_doctest.tst", verbose=True)

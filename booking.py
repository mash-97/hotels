import datetime
import random
import matplotlib 
import os
from hotel import *




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




class Booking:
    def __init__(self, hotels):
        self.hotels = hotels 
    
    
    def menu(self):
        print("Welcome to Booking System")
        print("What would you like to do?")
        print("1    Make a reservation")
        print("2    Cancel a reservation")
        print("3    Look up a reservation")
        
        choice = input("> ")
        if choice=="1":
            self.create_reservation()
            
        elif choice=="2":
            self.cancel_reservation()
            
        elif choice=="3":
            self.lookup_reservation()
        
        elif choice=="xyzzy":
            print("you said the magic word!")
            input("YOHYOYOYOY")
            self.delete_reservations_at_random()
        
        type(self).helper_save_all_the_hotels(self.hotels)
    
    
    """ purpose made """
    @staticmethod
    def helper_save_all_the_hotels(hotels):
        for hotel in hotels:
            hotel.save_hotel()
    
    # prompts user to give input on choice to create a reservation
    def create_reservation(self):
        person_name = input("Please enter your name: ")
        
        print("Hi {customer}! Which hotel would you like to book?".format(customer=person_name))
        for index, hotel in enumerate(self.hotels):
            print("{0} {1}".format(index+1, hotel.name))
        hotel_choice = int(input("> "))
        
        hotel = self.hotels[hotel_choice-1]
        room_types = hotel.get_available_room_types()
        
        print("Which type of room would you like?")
        for index, room_type in enumerate(room_types):
            print("{0} {1}".format(index+1, room_type))
        
        room_type_choice = int(input("> "))
        room_type = room_types[room_type_choice-1]
        
        cid_s = input("Enter check-in date (YYYY-MM-DD): ").split("-")
        cod_s = input("Enter check-out date (YYYY-MM-DD): ").split("-")
        
        check_in = datetime.date(int(cid_s[0]), int(cid_s[1]), int(cid_s[2]))
        check_out = datetime.date(int(cod_s[0]), int(cod_s[1]), int(cod_s[2]))
        
        print("Ok. Making your reservation for a Double room.")
        booking_number = hotel.make_reservation(person_name, room_type, check_in, check_out)
        
        print("Your reservation number is:", booking_number)
        print("Your total amount due is: $%.2f."%(hotel.get_receipt([booking_number])))
        print("Thank you!")
    
    
    """ purpose made """
    # find hotel for the booking_number
    # booking_number:int
    def helper_find_hotel(self, booking_number):
        for hotel in self.hotels:
            if booking_number in hotel.reservations:
                return hotel
        return False
    
    # prompts user to cancel the reservation
    def cancel_reservation(self):
        booking_number = int(input("Please enter your booking number: "))
        
        hotel = self.helper_find_hotel(booking_number)
        
        if hotel:
            hotel.cancel_reservation(booking_number)
            print("Cancelled successfully.")
        
        else:
            print("Could not find a reservation with that booking number.")
    
    
    # lookup reservation: prompts user to input booking number 
    # or person name, room reserved, check in date, check out date 
    def lookup_reservation(self):
        have_bn = input("Do you have your booking number(s)? ")
        if have_bn=="yes":
            bns = []
            while True:
                bn = input("Please enter a booking number (or 'end'): ")
                if bn=="end":
                    break
                bns.append(int(bn))
            
            for bn in bns:
                hotel = self.helper_find_hotel(bn)
                if not hotel:
                    print("Could not find a reservation with the booking number: ", bn)
                    continue
                
                reservation = hotel.reservations[bn]
                
                print("Reservation found at hotel %s:"%(hotel.name))
                print(reservation)
                # ~ print("Booking number: ", reservation.booking_number)
                # ~ print("Name: ", reservation.name)
                # ~ print("Room reserved: ", reservation.room_reserved)
                # ~ print("Check-in date: ", reservation.check_in)
                # ~ print("Check-out date: ", reservation.check_out)
                # ~ print("Total amount due: $%.2f"%(hotel.get_receipt([bn])))
                print()
        
        elif have_bn=="no":
            person_name = input("Please enter your name: ")
            hotel_name = input("Please enter the hotel you are booked at: ")
            room_number = int(input("Enter the reserved room number: "))
            cid_s = input("Enter the check-in date (YYYY-MM-DD): ").split("-")
            cod_s = input("Enter the check-out date (YYYY-MM-DD): ").split("-")
            
            check_in = datetime.date(int(cid_s[0]), int(cid_s[1]), int(cid_s[2]))
            check_out = datetime.date(int(cod_s[0]), int(cod_s[1]), int(cod_s[2]))
            
            # define for check
            hotel = None
            room = None
            reservation = None
            
            # find hotel with the hotel_name
            for h in self.hotels:
                if h.name == hotel_name:
                    hotel = h
                    break
            
            # ~ # find room with the room_number
            # ~ if hotel: 
                # ~ for r in hotel.rooms:
                    # ~ if r.room_num == room_number:
                        # ~ room = r
                        # ~ break
            
            # find reservation with above data
            if hotel:
                reservation = None
                for bn in hotel.reservations.keys():
                    rv = hotel.reservations[bn]
                    
                    found = True
                    found &= (hotel!=None)
                    # ~ if found: print("Hotel Passed!")
                    # ~ if found: print("Room Passed!")
                    found &= (rv.name==person_name)
                    # ~ if found: print("Name Passed!")
                    found &= (rv.room_reserved.room_num==room_number)
                    # ~ if found: print("Reserved Room Passed!")
                    found &= (rv.check_in==check_in)
                    # ~ if found: print("Check-in Passed!")
                    found &= (rv.check_out==check_out)
                    # ~ if found: print("Check-out Passed1")
                    
                    if found:
                        reservation = rv
                        break
            
            if reservation:
                print("Reservation found under booking number %s."%(reservation.booking_number))
                print("Here are the details:")
                print(reservation)
                # ~ print("Booking number: ", reservation.booking_number)
                # ~ print("Name: ", reservation.name)
                # ~ print("Room reserved: ", reservation.room_reserved)
                # ~ print("Check-in date: ", reservation.check_in)
                # ~ print("Check-out date: ", reservation.check_out)
                # ~ print("Total amount due: $%.2f"%(hotel.get_receipt([reservation.booking_number])))
            
            else:
                print("Could not find a reservation with the above information.")
        
            
    def delete_reservations_at_random(self):    
        print("You said the magic word!")
        random_index = random.randint(0, len(self.hotels)-1)
        hotel = self.hotels[random_index]
        
        hotel.reservations = {}
    
    
    """ purpose made """
    # month:int -> Month No
    # returns a dict mapping days to total reservations
    def helper_get_total_reservations(self, hotel, month):
       
        days = DAYS_PER_MONTH.copy()
        days[1] = 29            # ignore if not leap year
        days = days[month-1]    # assign only days of the 'month'
        
        # initialize d_to_rn dict with 0 values
        rpd = {}
        for i in range(days):
            rpd[i] = 0
        
        for bn in hotel.reservations.keys():
            reservation = hotel.reservations[bn]
            cid = reservation.check_in 
            cod = reservation.check_out 
            years = cod.year - cid.year
            
            for y in range(years+1):
                if month==2 and helper_is_leap(cid.year+y):
                    days = 29
                elif month==2:
                    days = 28
                
                for d in range(days):
                    date = datetime.date(cid.year+y, month, d+1)
                    if cid <= date < cod:
                        rpd[d] += 1
        return rpd
    
    
    """ purpose made """
    # returns a tuple of two lists respectively
    # one for keys and second for values
    # dictt:dict
    @staticmethod
    def helper_tup_kvl_dict(dictt):
        keys = []
        vals = []
        for key in dictt.keys():
            keys.append(key)
            vals.append(dictt[key])
        return (keys, vals)
    
    """ purpose made """
    # month:int -> Month No
    # returns a dict mapping hotel into a tupled-key-values-dict ( reservations per days )
    # get reservations per day for all the hotels
    def helper_get_rnpd_model_for_hotels(self, month):
        htd = {}
        for hotel in self.hotels:
            htd[hotel] = type(self).helper_tup_kvl_dict(self.helper_get_total_reservations(hotel, month))
        return htd
    
    # month:str -> MONTHs
    def plot_occupancies(self, month_s):
        month = helper_get_month_no(month_s) # month:int
        htd = self.helper_get_rnpd_model_for_hotels(month)
        """
            htd contains a dict like below:
            hotel_1: ([days], [reservation numbers per day])
        """
        
        # initialize result list
        rl = []
        
        # Now the ploting part
        import matplotlib.pyplot
        plt = matplotlib.pyplot
        
        plt.title("Occupancies for month "+month_s)
        plt.xlabel("Day of month")
        plt.ylabel("Number of reservations")
        
        for h in htd.keys():
            # lay to the plot
            plt.plot(htd[h][0], htd[h][1], label=h.name)
            # add to the result list
            rl.append(htd[h])
        
        plt.legend()
        plt.savefig("hotel_occupancies_"+month_s+".png")
        
        return rl
    
    
    @classmethod
    def load_system(cls):
        hotel_folder_names = os.listdir(HOTELS_FOLDER_PATH)
        hotel_folder_names.sort(reverse=True)
        hotels = []
        
        for hotel_folder_name in hotel_folder_names:
            hotels.append(Hotel.load_hotel(hotel_folder_name))
        return cls(hotels)



# ~ if __name__=="__main__":
    # ~ import doctest
    # ~ doctest.testfile("booking_doctest.tst", verbose=True)
    # ~ booking = Booking.load_system()
    # ~ booking.menu()
    

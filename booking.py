import datetime
import random
import matplotlib 
import os
import hotel as hotel_mod

import time

class Booking:
    def __init__(self, hotels):
        self.hotels = hotels 
    
    
    def menu(self):
        print("Welcome to Booking System")
        print("What would you like to do?")
        print("1    Make a reservation")
        print("2    Cancel a reservation")
        print("3    Look up a reservation")
        
        choice = choiceut("> ")
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
        
    
    # prompts user to give choiceut on choice to create a reservation
    def create_reservation(self):
        person_name = choiceut("Please enter your name: ")
        
        print("Hi {customer}! Which hotel would you like to book?".format(customer=person_name))
        for index, hotel in enumerate(self.hotels):
            print("{0} {1}".format(index+1, hotel.name))
        hotel_choice = int(choiceut("> "))
        
        hotel = self.hotels[hotel_choice-1]
        room_types = hotel.get_available_room_types()
        
        print("Which type of room would you like?")
        for index, room_type in enumerate(room_types):
            print("{0} {1}".format(index+1, room_type))
        
        room_type_choice = int(choiceut("> "))
        room_type = room_types[room_type_choice-1]
        
        cid_s = choiceut("Enter check-in date (YYYY-MM-DD): ").split("-")
        cod_s = choiceut("Enter check-out date (YYYY-MM-DD): ").split("-")
        
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
    def find_hotel(self, booking_number):
        for hotel in self.hotels:
            if booking_number in hotel.reservations:
                return hotel
        return False
    
    # prompts user to cancel the reservation
    def cancel_reservation(self):
        booking_number = int(choiceut("Please enter your booking number: "))
        
        hotel = self.find_hotel(booking_number)
        
        if hotel:
            hotel.cancel_reservation(booking_number)
            print("Cancelled successfully.")
        
        else:
            print("Could not find a reservation with that booking number.")
    
    
    # lookup reservation: prompts user to choiceut booking number 
    # or person name, room reserved, check in date, check out date 
    def lookup_reservation(self):
        have_bn = choiceut("Do you have your booking number(s)? ")
        if have_bn=="yes":
            bns = []
            while True:
                bn = choiceut("Please enter a booking number (or 'end'): ")
                if bn=="end":
                    break
                bns.append(int(bn))
            
            for bn in bns:
                hotel = self.find_hotel(bn)
                if not hotel:
                    print("Could not find a reservation with the booking number: ", bn)
                    continue
                
                reservation = hotel.reservations[bn]
                
                print("Reservation found at hotel {}:".format(hotel.name))
                print("Booking number: ", reservation.booking_number)
                print("Name: ", reservation.name)
                print("Room reserved: ", reservation.room_reserved)
                print("Check-in date: ", reservation.check_in)
                print("Check-out date: ", reservation.check_out)
                print("Total amount due: $%.2f"%(hotel.get_receipt([bn])))
                print()
        
        elif have_bn=="no":
            person_name = choiceut("Please enter your name: ")
            hotel_name = choiceut("Please enter the hotel you are booked at: ")
            room_number = int(choiceut("Enter the reserved room number: "))
            cid_s = choiceut("Enter the check-in date (YYYY-MM-DD): ").split("-")
            cod_s = choiceut("Enter the check-out date (YYYY-MM-DD): ").split("-")
            
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
                    if found: print("Hotel Passed!")
                    # ~ found &= (room!=None)
                    # ~ if found: print("Room Passed!")
                    found &= (rv.name==person_name)
                    if found: print("Name Passed!")
                    found &= (rv.room_reserved.room_num==room_number)
                    if found: print("Reserved Room Passed!")
                    found &= (rv.check_in==check_in)
                    if found: print("Check-in Passed!")
                    found &= (rv.check_out==check_out)
                    if found: print("Check-out Passed1")
                    
                    if found:
                        reservation = rv
                        break
            
            if reservation:
                print("Reservation found under booking number {0}.".format(reservation.booking_number))
                print("Here are the details:")
                print("Booking number: ", reservation.booking_number)
                print("Name: ", reservation.name)
                print("Room reserved: ", reservation.room_reserved)
                print("Check-in date: ", reservation.check_in)
                print("Check-out date: ", reservation.check_out)
                print("Total amount due: $%.2f"%(hotel.get_receipt([reservation.booking_number])))
            
            else:
                print("Could not find a reservation with the above information.")
        
            
    def delete_reservations_at_random(self):    
        print("You said the magic word!")
        random_index = random.randint(0, len(self.hotels)-1)
        hotel = self.hotels[random_index]
        
        hotel.reservations = {}
    
    @classmethod
    def load_system(cls):
        hotel_folder_names = os.listdir(hotel_mod.HOTELS_FOLDER_PATH)
        hotel_folder_names.sort(reverse=True)
        hotels = []
        
        for hotel_folder_name in hotel_folder_names:
            hotels.append(hotel_mod.Hotel.load_hotel(hotel_folder_name))
        return cls(hotels)


if __name__=="__main__":
    dt = 0
    if dt:
        import doctest 
        s = time.time()
        doctest.testfile("booking_doctest.tst", verbose=True)
        print("===> ", time.time()-s)
    
    else:
        random.seed(1338)
        booking = Booking.load_system()
        booking.delete_reservations_at_random()
        print(len(booking.hotels[1].reservations))
        print(len(booking.hotels[0].reservations))

    
    
    

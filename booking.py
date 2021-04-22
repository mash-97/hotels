import datetime
import random
import matplotlib 
import os
import hotel as hotel_mod


class Booking:
    def __init__(self, hotels):
        self.hotels = hotels 
    
    
    @classmethod
    def load_system(cls):
        hotel_folder_names = os.listdir(hotel_mod.HOTELS_FOLDER_PATH)
        hotel_folder_names.sort(reverse=True)
        hotels = []
        for hotel_folder_name in hotel_folder_names:
            hotels.append(hotel_mod.Hotel.load_hotel(hotel_folder_name))
        return cls(hotels)


if __name__=="__main__":
    import doctest 
    doctest.testfile("booking_doctest.tst", verbose=True)


from abc import ABC, abstractmethod
from datetime import datetime
# VEHICLE CLASSES 
class Vehicle(ABC):
    def __init__(self, plate_number):
        self.plate_number = plate_number
    @abstractmethod
    def get_rate(self):
        pass
class Car(Vehicle):
    def get_rate(self):
        return 7
class Bike(Vehicle):
    def get_rate(self):
        return 3
class Truck(Vehicle):
    def get_rate(self):
        return 10
#  PRICING STRATEGY
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, hours, rate):
        pass
class PeakPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate * 1.5
class OffPeakPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate
class WeekendPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate * 1.2
# PARKING TICKET

class ParkingTicket:
    def __init__(self, vehicle):
        self.vehicle = vehicle
        self.entry_time = datetime.now()
        self.exit_time = None
        self.duration = 0
        self.fee = 0
    def close_ticket(self, pricing_strategy):
        self.exit_time = datetime.now()
        time_diff = self.exit_time - self.entry_time
        self.duration = max(1, round(time_diff.total_seconds() / 3600))
        rate = self.vehicle.get_rate()
        self.fee = pricing_strategy.calculate_fee(self.duration, rate)
# PARKING LOT 

class ParkingLot:
    def __init__(self, total_spaces, pricing_strategy):
        self.total_spaces = total_spaces
        self.available_spaces = total_spaces
        self.active_tickets = {}
        self.pricing_strategy = pricing_strategy
    def park_vehicle(self, vehicle):
        if self.available_spaces <= 0:
            print(" Parking Full!")
            return
        if vehicle.plate_number in self.active_tickets:
            print("⚠ Vehicle already inside!")
            return
        ticket = ParkingTicket(vehicle)
        self.active_tickets[vehicle.plate_number] = ticket
        self.available_spaces -= 1
        print(f" Vehicle {vehicle.plate_number} parked. Spaces left: {self.available_spaces}")

    def exit_vehicle(self, plate_number):
        if plate_number not in self.active_tickets:
            print(" Vehicle not found!")
            return
        ticket = self.active_tickets.pop(plate_number)
        ticket.close_ticket(self.pricing_strategy)
        self.available_spaces += 1

        print("\n----- Parking Bill -----")
        print("Plate:", plate_number)
        print("Hours:", ticket.duration)
        print("Total Fee: $", ticket.fee)
        print("Spaces left:", self.available_spaces)
        print("------------------------")
# HELPER FUNCTION

def create_vehicle():
    v_type = input("Enter vehicle type (car/bike/truck): ").lower()
    plate = input("Enter plate number: ")

    if v_type == "car":
        return Car(plate)
    elif v_type == "bike":
        return Bike(plate)
    elif v_type == "truck":
        return Truck(plate)
    else:
        print("Invalid vehicle type!")
        return None
def choose_pricing():
    print("Select Pricing Strategy:")
    print("1. Peak")
    print("2. Off-Peak")
    print("3. Weekend")
    choice = input("Choice: ")
    if choice == "1":
        return PeakPricing()
    elif choice == "2":
        return OffPeakPricing()
    elif choice == "3":
        return WeekendPricing()
    else:
        print("Invalid choice! Defaulting to Off-Peak.")
        return OffPeakPricing()
    
#  MAIN SYSTEM 

def main():
    strategy = choose_pricing()
    parking_lot = ParkingLot(300, strategy)
    while True:
        print("\n===== Parking System =====")
        print("1. Park Vehicle")
        print("2. Exit Vehicle")
        print("3. Show Available Spaces")
        print("4. Exit Program")
        option = input("Select option: ")
        if option == "1":
            vehicle = create_vehicle()
            if vehicle:
                parking_lot.park_vehicle(vehicle)
        elif option == "2":
            plate = input("Enter plate number to exit: ")
            parking_lot.exit_vehicle(plate)
        elif option == "3":
            print("Available Spaces:", parking_lot.available_spaces)
        elif option == "4":
            print("Exiting system...")
            break
        else:
            print("Invalid option!")
if __name__ == "__main__":
    main()

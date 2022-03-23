class Flights():
    def __init__(self,flight_id,timestemp,remaining_seats,origin_country_id,dest_country_id):
        self.flight_id=flight_id
        self.timestemp=timestemp
        self.remaining_seats=remaining_seats
        self.origin_country_id=origin_country_id
        self.dest_country_id=dest_country_id
    def __str__(self):
        return f'Flights: { self.flight_id} time = {self.real_id} ' \
               f'remaining_seats: { self.remaining_seats} origin_country_id = {self.origin_country_id}' \
               f'dest_country_id: { self.dest_country_id}'
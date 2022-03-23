class Tickets():
    def __init__(self,ticket_id,user_id,flight_id):
        self.ticket_id=ticket_id
        self.user_id=user_id
        self.flight_id=flight_id
    def __str__(self):
        return f'Ticket: { self.ticket_id}  user_id = {self.user_id} flight_id={self.flight_id}'
import sqlite3

myroute = r'C:\Users\Benas\Desktop\projectDB.db'  # the route of the db

def GetUsersToDict():
    '''
    A function that displays all users from the database using a SELECT query
    :return: list Of all Users in DB
    '''
    conn = sqlite3.connect(myroute)
    listOfUsers = []
    crusr = conn.execute('SELECT * FROM users')
    for record in crusr:
        user = {"id_AI": record[0], "full_name": record[1], "password": record[2],
                "real_id": record[3]}
        listOfUsers.append(user)
    conn.close()
    return listOfUsers

def GetFlightsToDict():
    '''
     A function that displays all Flights from the database using a SELECT query
    :return: list Of all Flights in DB
    '''
    conn = sqlite3.connect(myroute)
    listOFFlights = []
    crusr = conn.execute('SELECT * FROM Flights')
    for record in crusr:
        flight = {"flight_id": record[0], "timestamp": record[1], "remaining_seats": record[2],
                  "origin_country_id": record[3], "dest_country_id": record[4]}
        listOFFlights.append(flight)
    conn.close()
    return listOFFlights

def GetTicketsToDict(): 
    '''
     A function that displays all Tickets from the database using a SELECT query
    :return: list Of all Tickets in DB
    '''
    conn = sqlite3.connect(myroute)
    listOFTickets = []
    crusr = conn.execute('SELECT * FROM Tickets')
    for record in crusr:
        ticket = {"ticket_id": record[0], "user_id": record[1], "flight_id": record[2]}
        listOFTickets.append(ticket)
    conn.close()
    return listOFTickets

def GetCountriesToDict():
    '''
     A function that displays all Countries from the database using a SELECT query
    :return: list Of all Countries in DB
    '''
    conn = sqlite3.connect(myroute)
    listOFCountries = []
    crusr = conn.execute('SELECT * FROM Countries')
    for record in crusr:
        country = {"code_AI": record[0], "name": record[1]}
        listOFCountries.append(country)
    conn.close()
    return listOFCountries

def Postuser(name, pwd, id):
    '''
    A function that post user into the database using a INSERT query
    :param user name:
    :param user pwd :
    :param user id_AI:
    :return: new update list of users
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"INSERT INTO users (full_name,password,real_id) VALUES('{name}','{pwd}','{id}')")
    conn.commit()
    conn.close()
    return f'{GetUsersToDict()}'

def Putuser(id_AI, name, pwd, id): 
    '''
    A function that update user from the database using a UPDATE query
    :param user id_AI:
    :param user name:
    :param user pwd:
    :param user id:
    :return: new update list of users
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"UPDATE users SET full_name = '{name}',password = '{pwd}',real_id = '{id}' WHERE id_AI = {id_AI}")
    conn.commit()
    conn.close()
    return f'{GetUsersToDict()}'

def Deleteuser(id_AI):
    '''
    A function that delete user from the database using a DELETE query
    :param user id_AI:
    :return: new update list of users
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"DELETE FROM users WHERE id_AI = {id_AI}")
    conn.commit()
    conn.close()
    return f'{GetUsersToDict()}'

def Postflight(timestamp, remaining_seats, origin_country_id,dest_country_id):
    '''
    A function that post flight into the database using a INSERT query
    :param flight timestamp:
    :param flight remaining_seats:
    :param flight origin_country_id:
    :param flight dest_country_id:
    :return: new update list of flights
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"INSERT INTO Flights (timestamp,remaining_seats,origin_country_id,dest_country_id)"
                 f" VALUES('{timestamp}',{remaining_seats},{origin_country_id},{dest_country_id})")
    conn.commit()
    conn.close()
    return f'{GetFlightsToDict()}'

def Putflight(flight_id, timestamp, remaining_seats, origin_country_id,dest_country_id):
    '''
    A function that update flight from the database using a UPDATE query
    :param flight_id:
    :param flight timestamp:
    :param flight remaining_seats:
    :param flight origin_country_id:
    :param flight dest_country_id:
    :return: new update list of flights
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"UPDATE Flights SET timestamp = '{timestamp}',remaining_seats = {remaining_seats},"
                 f"origin_country_id = {origin_country_id},dest_country_id = {dest_country_id} WHERE flight_id = {flight_id}")
    conn.commit()
    conn.close()
    return f'{GetFlightsToDict()}'

def Deleteflight(flight_id):
    '''
    A function that delete flight from the database using a DELETE query
    :param flight_id:
    :return: new update list of flights
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"DELETE FROM Flights WHERE flight_id = {flight_id}")
    conn.commit()
    conn.close()
    return f'{GetFlightsToDict()}'

def Postticket(user_id, flight_id):
    '''
    A function that post ticket into the database using a INSERT query
    :param user_id:
    :param flight_id:
    :return: new update list of Tickets
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"INSERT INTO Tickets(user_id,flight_id) VALUES({user_id},{flight_id})")
    conn.commit()
    conn.close()
    return f'{GetTicketsToDict()}'

def Deleteticket(ticket_id):
    '''
    A function that delete ticket from the database using a DELETE query
    :param ticket_id:
    :return: new update list of Tickets
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"DELETE FROM Tickets WHERE ticket_id = {ticket_id}")
    conn.commit()
    conn.close()
    return f'{GetTicketsToDict()}'

def Postcountry(name):
    '''
    A function that post country into the database using a INSERT query
    :param country name:
    :return: new update list of Countries
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"INSERT INTO Countries (name) VALUES('{name}')")
    conn.commit()
    conn.close()
    return f'{GetCountriesToDict()}'

def Putcountry(code_AI, name):
    '''
    A function that update country from the database using a UPDATE query
    :param country code_AI:
    :param country name:
    :return: new update list of Countries
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"UPDATE Countries SET name = '{name}' WHERE code_AI = {code_AI}")
    conn.commit()
    conn.close()
    return f'{GetCountriesToDict()}'

def Deletecountry(code_AI):
    '''
    A function that delete country from the database using a DELETE query
    :param country code_AI:
    :return: new update list of Countries
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"DELETE FROM Countries WHERE code_AI = {code_AI}")
    conn.commit()
    conn.close()
    return f'{GetCountriesToDict()}'

def TicketIdToFlightID(ticket_id):
    '''
    A function that receives a ticket ID and checks if it exists or not, if yes returns his flight id
    :param ticket_id:
    :return: if this ticket exist return the flight id of the ticket else return false
    '''
    for ticket in GetTicketsToDict():
        if ticket.get("ticket_id") == ticket_id:
            return int(ticket.get("flight_id"))
    else:
        return False

def DeleteticketAndRemainingSeats(ticket_id):
    '''
    A function that deletes a ticket with DELETE query from DB
    and adds a remainig seat on the flight with UPDATE query to DB
    :param ticket_id
    '''
    conn = sqlite3.connect(myroute)
    flight_id = TicketIdToFlightID(ticket_id)
    conn.execute(f"DELETE FROM Tickets WHERE ticket_id = {ticket_id}")
    conn.commit()
    conn.execute(f"UPDATE Flights SET remaining_seats = remaining_seats+1 WHERE flight_id= {flight_id}")
    conn.commit()
    conn.close()

def ReturnUserDictBYidAi(id):
    '''
    a function which brings all the user's details according to his ID_AI number
    :param user id_AI:
    :return: user dictionary
    '''
    for i in GetUsersToDict():
        if id == i.get("id_AI"):
            return i

def ReturnUserIDbyTicket(ticket_id): 
    '''
    a function that take ticket id and return the user id that owner the ticket
    :param ticket_id:
    :return: user id who own the ticket
    '''
    for ticket in GetTicketsToDict():
        if ticket.get("ticket_id") == ticket_id:
            return ticket.get("user_id")
    else:
        return False

def ListOFTickets(id_AI):
    '''
    A function that returns a list of all tickets that the user purchased by user ID_ai
    :param user id_AI:
    :return: list of all tickets owned by the user
    '''
    listoftickets = []
    for ticket in GetTicketsToDict():
        if ticket.get("user_id") == id_AI: 
            listoftickets.append(ticket)
    return listoftickets

def IfFlightExist(flight_id): 
    '''
    A function that took flight id and returns if there left remaining seats of the fligt or not
    :param flight_id:
    :return: if there left remaining seats of the fligt return True if not False
    '''
    for i in GetFlightsToDict():
        if i.get("flight_id") == flight_id and i.get("remaining_seats") > 0:  # בדיקה האם הid ברשימה
            return True
    return False

def BuyTicketAndRemainingSeats(user_id, flight_id):
    '''
    A function that insert ticket to DB with INSERT query
    and Missing a seat from the flight in DB with UPDATE query
    :param user_id - who want to buy the ticket:
    :param flight_id taht the user want to buy:
    '''
    conn = sqlite3.connect(myroute)
    conn.execute(f"INSERT INTO Tickets(user_id,flight_id) VALUES({user_id},{flight_id})")
    conn.commit()
    conn.execute(f"UPDATE Flights SET remaining_seats = remaining_seats-1 WHERE flight_id= {flight_id}")
    conn.commit()
    conn.close()

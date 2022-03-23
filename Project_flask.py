import json
import requests
from flask import Flask
from flask import url_for, redirect, request, render_template
import sqlite3
from MyFunctions import *
import logging
# from users import *
# from tickets import *
# from flights import *
# from countries import *
app = Flask(__name__)
logging.basicConfig(filename="ProjectLog.log", level=10, format='%(asctime)s ==> %(levelname)s: %(message)s')


# Home page
@app.route('/')
def homepage():
    logging.info("User was enter to the home page")
    return render_template('homepage.html')


# login page
@app.route('/login')
@app.route('/Login')
def login():
    logging.info("User was enter to the login page")
    return render_template('Login.html')


# register page
@app.route('/register')
@app.route('/Register')
def register():
    logging.info("User was enter to the register page")
    return render_template('Register.html')


# user website page
@app.route('/Website', methods=['POST'])
@app.route('/website', methods=['POST'])
def website():
    logging.debug(f'User with real id "{request.form["realid"]}" was try to enter in the website page with SELECT Query')
    for i in GetUsersToDict():
        if request.form['pwd'] == i.get("password") and request.form['realid'] == i.get("real_id"):  # check users details for login
            logging.info(f'User "{i.get("full_name")}" was enter to the website page with SELECT Query')
            listoftickets = [] #list of all the user tickets
            for ticket in GetTicketsToDict():
                if ticket.get("user_id") == i.get("id_AI"):  # Check which of the cards are of the user mentioned above
                    listoftickets.append(ticket)
            return render_template('UserWebsite.html', i=i, lst=listoftickets, flights=GetFlightsToDict())
            # i=user dictionary details,lst= list of user tickets,flights= list of all flights
    else:
        logging.error(f"User was enter wrong details in the login page")
        return f'<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />' \
               f'<body style="text-align:center" BGCOLOR="Gainsboro"> <font Size="7">EROR please try again <br /> ' \
               f'<br /><a href="http://127.0.0.1:5000/Login">' \
               f'<button style="width: 100px; height: 50px">Login</button></a>'


@app.route('/Delete', methods=['POST'])
@app.route('/delete', methods=['POST'])
def DeleteTickets():
    id = int(request.form['id_ai'])
    ticket_id = int(request.form['ticket'])
    logging.debug(f'User "{ReturnUserDictBYidAi(id).get("full_name")}" was try to delete ticket id: "{ticket_id}"')
    if id == ReturnUserIDbyTicket(ticket_id):  # check if the ticket that the user sent is really his
        DeleteticketAndRemainingSeats(ticket_id)  # delete the ticket from the user and add 1 seat to the remainig seats
        logging.info(f'User "{ReturnUserDictBYidAi(id).get("full_name")}" was delete with DELETE Query ticket id: "{ticket_id}"')
        return render_template('UserWebsite.html', i=ReturnUserDictBYidAi(id), lst=ListOFTickets(id),flights=GetFlightsToDict())
    else:  # eror if the ticket id not match to the user id - alert and return to login
        logging.error(f"User {ReturnUserDictBYidAi(id).get('full_name')} was enter wrong ticket id in the delete box")
        return f'<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />' \
               f'<body style="text-align:center" BGCOLOR="Gainsboro"> <font Size="7">EROR!!!!!<br /> ' \
               f'YOUR TICKET ID YOU INSERT NOT YOURS!!!! <br /> please LOGIN and try again <br /> ' \
               f'<br /><a href="http://127.0.0.1:5000/Login">' \
               f'<button style="width: 100px; height: 50px">Login</button></a>'


@app.route('/buy', methods=['POST'])
def BuyTicket():
    id = int(request.form["id_ai"])
    flight_id = int(request.form['flight'])
    logging.debug(f'User "{ReturnUserDictBYidAi(id).get("full_name")}" was try to buy ticket in flight: "{flight_id}"')
    if IfFlightExist(flight_id):  # check if the flight even exist
        BuyTicketAndRemainingSeats(id, flight_id)  # add ticket to the user and delete 1 seat from the remaining seats
        logging.info(f'User "{ReturnUserDictBYidAi(id).get("full_name")}" was buy ticket with INSERT and UPDATE Query in flight: {flight_id}')
        return render_template('UserWebsite.html', i=ReturnUserDictBYidAi(id), lst=ListOFTickets(id),flights=GetFlightsToDict())
    else:  # eror if the flight is dont exist or was no left remaining seat on the flight - alert and return to login
        logging.error(f'User "{ReturnUserDictBYidAi(id).get("full_name")}" was enter wrong flight id in the buy box or not left remaining seats')
        return f'<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />' \
               f'<body style="text-align:center" BGCOLOR="Gainsboro"> <font Size="7">EROR!!!!!<br /> ' \
               f'YOUR FLIGHT ID YOU INSERT NOT EXIST OR THERE WERE NO SEATS LEFT ON THE FLIGHT!!!! <br /> please LOGIN and try again <br /> ' \
               f'<br /><a href="http://127.0.0.1:5000/Login">' \
               f'<button style="width: 100px; height: 50px">Login</button></a>'


@app.route('/users', methods=['GET', 'POST', 'PUT'])
@app.route('/Users', methods=['GET', 'POST', 'PUT'])
def Users():
    if request.method == 'GET':
        logging.info(f'Get request sent to users by Postman with SELECT Query')
        return f'{GetUsersToDict()}'  # getUsers - all the users from DB
    elif request.method == 'POST':  # PostUsers - add user to DB
        if request.get_json() != None:  # check if the details of the user sent from the postman or by form in html
            user = request.get_json()  # it sent by postman
            Postuser(user.get('full_name'), user.get('password'), user.get('real_id'))
            logging.info(
                f'POST request sent to users by postman and insert to DB user:"{user.get("full_name")}" with real id:{user.get("real_id")}')
            return f'{GetUsersToDict()}'
        else:  # it sent by form html, Execution of the information that sent from the register and publication in the DB by INSERT query
            Postuser(request.form['name'], request.form['pwd'], request.form['realid'])
            logging.info(f'POST request sent from users by Register and insert to DB user:"{request.form["name"]}" with real id:{request.form["realid"]}')
            #Go to page where says about successful registration and go to the main menu
            return f'<br /><br /><br /><br /><br /><br /><br /><br /><br /><br /><br />'  \
               f'<body style="text-align:center" BGCOLOR="Gainsboro"> <font Size="7"> ' \
               f' You have successfully registered <br /> and press the button to redirected to the main menu site. <br /> please LOGIN now<br /> ' \
               f'<br /><a href="http://127.0.0.1:5000/">' \
               f'<button style="width: 100px; height: 50px">Home page</button></a>'
            #render_template('Login.html')
    elif request.method == 'PUT':  # put user in DB by his id_AI
        user = request.get_json()
        logging.debug(f'Postman try to sent PUT request to users')
        for temp in GetUsersToDict():
            if temp.get("id_AI") == user.get("id_AI"):  # cheak if id in the list
                Putuser(user.get('id_AI'), user.get('full_name'), user.get('password'), user.get('real_id'))
                logging.info(f'Postman change user from users with UPDATE Query in id_ai: {user.get("id_AI")} ')
                return f'{GetUsersToDict()}'
        logging.error(f'Postman try to PUT request with User id_AI that not exist in users')
        return 'we dont have this user'


# getUserByID / deleteUserByID
@app.route('/users/<int:id>', methods=['GET', 'DELETE'])
@app.route('/Users/<int:id>', methods=['GET', 'DELETE'])
def getUser(id):
    if request.method == 'GET':  # get user by id_AI
        logging.debug(f'Postman try to sent GET request to users with id_AI = {id}')
        for temp in GetUsersToDict():
            if temp.get("id_AI") == id:  # cheak if id in the users table
                logging.info(f'Postman send GET request to users with SELECT Query in id_ai: {id} ')
                return temp
        logging.error(f'Postman try to GET request with User id_AI = {id} that not exist in users')
        return 'we dont have this user'
    elif request.method == 'DELETE':  # delete user by id_AI
        logging.debug(f'Postman try to sent DELETE request to users with id_AI = {id}')
        for temp in GetUsersToDict():
            if temp.get("id_AI") == id:  # cheak if id in the users table
                Deleteuser(id)
                logging.info(f'Postman send DELETE request to users with DELETE Query in id_ai: {id} ')
                return f'{GetUsersToDict()}'
        logging.error(f'Postman try to DELETE request with User id_AI = {id} that not exist in users')
        return 'we dont have this user'


@app.route('/flights', methods=['GET', 'POST', 'PUT'])
@app.route('/Flights', methods=['GET', 'POST', 'PUT'])
def Flights():
    if request.method == 'GET':  # SELECT flights from DB
        logging.info(f'GET request sent to flights by Postman with SELECT Query')
        return f'{GetFlightsToDict()}'
    elif request.method == 'POST':  # INSERT flight to the DB
        logging.debug(f'Postman try to send POST request to flights ')
        flight = request.get_json()
        Postflight(flight.get('timestamp'), flight.get('remaining_seats'), flight.get('origin_country_id'),flight.get('dest_country_id'))
        logging.info(f'POST request sent to flights by postman and insert to DB flight with INSERT Query in time:"{flight.get("timestamp")}"')
        return f'{GetFlightsToDict()}'
    elif request.method == 'PUT':  # UPDATE flight from the DB
        logging.debug(f'Postman try to send PUT request to flights ')
        flight = request.get_json()
        for temp in GetFlightsToDict():
            if temp.get("flight_id") == flight.get("flight_id"):  # cheak if id in the list
                Putflight(flight.get('flight_id'), flight.get('timestamp'), flight.get('remaining_seats'),
                          flight.get('origin_country_id'), flight.get('dest_country_id'))
                logging.info(
                    f'put request sent to flights by postman and edit details in DB flight with UPDATE Query in flight_id:"{flight.get("flight_id")}"')
                return f'{GetFlightsToDict()}'
        logging.error(f'Postman try to send PUT request with flight id = {flight.get("flight_id")} that not exist or'
                      f'something goes wrong with the details')
        return 'we dont have this flight'


# FlightByID
@app.route('/flights/<int:id>', methods=['GET', 'DELETE'])
@app.route('/Flights/<int:id>', methods=['GET', 'DELETE'])
def GetFlight(id):
    if request.method == 'GET':  # get flight by id
        logging.debug(f'Postman try to sent GET request to flights with flight_id = {id}')
        for js in GetFlightsToDict():
            if js.get("flight_id") == id:  # cheak if id in the flights table
                logging.info(f'Postman send GET request to flights with SELECT Query in flight_id: {id} ')
                return js
        logging.error(f'Postman try to GET request with flight_id = {id} that not exist in flights')
        return 'we dont have this flight'
    elif request.method == 'DELETE':  # delete flight by id from DB
        logging.debug(f'Postman try to sent DELETE request to flights with flight_id = {id}')
        for temp in GetFlightsToDict():
            if temp.get("flight_id") == id:  # cheak if id in the flights table
                Deleteflight(id)
                logging.info(f'Postman send DELETE request to flights with DELETE Query in flight_id: {id} ')
                return f'{GetFlightsToDict()}'
        logging.error(f'Postman try to DELETE request with flight_id = {id} that not exist in flights')
        return 'we dont have this flight'


# Tickets
@app.route('/tickets', methods=['GET', 'POST'])
@app.route('/Tickets', methods=['GET', 'POST'])
def Tickets():
    if request.method == 'GET':  # SELECT Tickets from DB
        logging.info(f'GET request sent to Tickets by Postman with SELECT Query')
        return f'{GetTicketsToDict()}'
    elif request.method == 'POST':  # INSERT ticket to DB
        logging.debug(f'Postman try to send POST request to Tickets')
        ticket = request.get_json()
        Postticket(ticket.get('user_id'), ticket.get('flight_id'))
        logging.info(
            f'POST request sent to Tickets by Postman and insert to DB ticket with INSERT Query in user_id:"{ticket.get("user_id")}"')
        return f'{GetTicketsToDict()}'


# TicketByID
@app.route('/Tickets/<int:id>', methods=['GET', 'DELETE'])
@app.route('/tickets/<int:id>', methods=['GET', 'DELETE'])
def getTicket(id):
    if request.method == 'GET':  # get Ticket By id
        logging.debug(f'Postman try to sent GET request to Tickets with Ticket_id = {id}')
        for js in GetTicketsToDict():
            if js.get("ticket_id") == id:  # cheak if id in the tickets table
                logging.info(f'Postman send GET request to tickets with SELECT Query in ticket_id: {id} ')
                return js
        logging.error(f'Postman try to GET request with ticket_id = {id} that not exist in tickets')
        return 'we dont have this ticket'
    elif request.method == 'DELETE':  # Delete ticket by id
        logging.debug(f'Postman try to sent DELETE request to tickets with ticket_id = {id}')
        for temp in GetTicketsToDict():
            if temp.get("ticket_id") == id:  # cheak if id in the tickets table
                Deleteticket(id)
                logging.info(f'Postman send DELETE request to tickets with DELETE Query in ticket_id: {id} ')
                return f'{GetTicketsToDict()}'
        logging.error(f'Postman try to DELETE request with ticket_id = {id} that not exist in tickets')
        return 'we dont have this ticket'


# Countries
@app.route('/Countries', methods=['GET', 'POST', 'PUT'])
@app.route('/countries', methods=['GET', 'POST', 'PUT'])
def Countries():
    if request.method == 'GET':  # SELECT countries from DB
        logging.info(f'GET request sent to Countries by Postman with SELECT Query')
        return f'{GetCountriesToDict()}'  # GetCountries
    elif request.method == 'POST':  # INSERT country to DB
        logging.debug(f'Postman try to send POST request to Countries')
        country = request.get_json()
        Postcountry(country.get('name'))
        logging.info(
            f'POST request sent to Countries by postman and insert to DB Country with INSERT Query with name:"{country.get("name")}"')
        return f'{GetCountriesToDict()}'
    elif request.method == 'PUT':  # UPDATE country from DB
        logging.debug(f'Postman try to send PUT request to Countries')
        country = request.get_json()
        for temp in GetCountriesToDict():
            if temp.get("code_AI") == country.get("code_AI"):  # cheak if id in the list
                Putcountry(country.get('code_AI'), country.get('name'))
                logging.info(
                    f'put request sent to Countries by postman and edit details in DB Country with UPDATE Query with name:"{country.get("name")}"')
                return f'{GetCountriesToDict()}'
        logging.error(
            f'Postman try to send PUT request to countries with code_AI = {country.get("code_AI")} that not exist or'
            f'something goes wrong with the details')
        return 'we dont have this country'


@app.route('/countries/<int:id>', methods=['GET', 'DELETE'])
@app.route('/Countries/<int:id>', methods=['GET', 'DELETE'])
def getCountry(id):
    if request.method == 'GET':  # get country by id
        logging.debug(f'Postman try to send GET request to Countries with code_AI = {id}')
        for js in GetCountriesToDict():
            if js.get("code_AI") == id:  #  cheak if id in the list
                logging.info(f'Postman send GET request to Countries with SELECT Query in code_AI: {id} ')
                return js
        logging.error(f'Postman try to GET request with code_AI = {id} that not exist in Countries')
        return 'we dont have this country'
    elif request.method == 'DELETE':  # delete country by id
        logging.debug(f'Postman try to sent DELETE request to Countries with code_AI = {id}')
        for temp in GetCountriesToDict():
            if temp.get("code_AI") == id:  #  cheak if id in the list
                Deletecountry(id)
                logging.info(f'Postman send DELETE request to Countries with DELETE Query in code_AI: {id} ')
                return f'{GetCountriesToDict()}'
        logging.error(f'Postman try to DELETE request with code_AI = {id} that not exist in Countries')
        return 'we dont have this country'


if __name__ == '__main__':
    app.run()

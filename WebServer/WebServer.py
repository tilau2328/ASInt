 #!/usr/bin/env python

import json
import webapp2
from webapp2_extras import routes
from DataBase import DataBase

DEBUG = True

#################### WebAppServer ####################

database = DataBase()

if DEBUG:
    database.reset()

class MainPage(webapp2.RequestHandler):
    def get(self):

        s = ""
        s += '<h4>Messages:  </h4>'
        s += '<p>'
        s += '<a href="html/messages/count">Number of messages </a> &nbsp '
        s += '<a href="html/messages">List of messages </a> &nbsp '
        s += '</p>'

        try:
            users = database.users.get()

            if users:
                s += '<h3>Users:</h3>'
                for user in users:
                    s += '<p>'
                    s += '<h4>User: ' + user["Username"] + ' </h4>'
                    s += '<a href="html/users/' + user["Username"] + '/messages/count">Number of messages of user: ' + user["Username"] + ' </a> &nbsp '
                    s += '<a href="html/users/' + user["Username"] +'/messages">List of messages of user: ' + user["Username"] + ' </a> &nbsp '
                    s += '</p>'
            else:
                s += '<h3>No User Exist, Yet</h3>'
        except Exception as e:
            if DEBUG:
                print e
            pass

        try:
            rooms = database.rooms.get()
            if rooms:
                s += '<h3>Rooms:</h3>'
                for room in rooms:
                    s += '<p>'
                    s += '<h4>Room: ' + room["RoomID"] + ' </h4>'
                    s += '<a href="html/' + room["RoomID"] + '/users/count">Number of users in room: ' + room["RoomID"] + ' </a> &nbsp '
                    s += '<a href="html/' + room["RoomID"] + '/users">List of users in room: ' + room["RoomID"] + ' </a> &nbsp '
                    s += '<a href="html/' + room["RoomID"] + '/messages/count">Number of messages in room: ' + room["RoomID"] + ' </a> &nbsp '
                    s += '<a href="html/' + room["RoomID"] + '/messages">List of messages in room: ' + room["RoomID"] + ' </a> &nbsp '
                    s += '</p>'
            else:
                s += '<h3>No Room Exist, Yet</h3>'
        except Exception as e:
            if DEBUG:
                print e

        self.response.write(s)

###################### WebClient #####################

class UsersCount(webapp2.RequestHandler):
    def get(self, RoomID = None):
        if RoomID:
            users_in_room = database.users.count(RoomID = RoomID)
            if users_in_room:
                self.response.write('There are ' + str(users_in_room) + ' users in room: ' + str(RoomID))
            else:
                self.response.write('There is no user in this room, yet')
        else:
            number_of_users = database.users.count()
            if number_of_users:
                self.response.write('There are ' + str(number_of_users) + ' connected')
            else:
                self.response.write('There are no users, yet')

class UsersList(webapp2.RequestHandler):
    def get(self, RoomID = None):
        if RoomID:
            users = database.users.get(RoomID = RoomID)
            print users
            if users:
                self.response.write('Users in room ' + str(RoomID) + ': ')
                self.response.write(users)
            else:
                self.response.write('There is no user in this room, yet')
        else:
            users = database.users.get()
            print users
            if users:
                self.response.write('Active Users: ')
                self.response.write(users)
            else:
                self.response.write('There is no user connected, yet')

class MessagesCount(webapp2.RequestHandler):
    def get(self, RoomID = None, Username = None):
        if RoomID:
            try:
                number_of_messages = database.messages.count(RoomID = RoomID)
                print "#" + str(number_of_messages)
                if number_of_messages:
                    self.response.write('Number of messages sent: ' + str(number_of_messages))
                else:
                    self.response.write('No message has been sent in this room, yet')
            except Exception as e:
                if DEBUG:
                    print e
                self.response.write("This group doesn't exist, yet")
        elif Username:
            try:
                number_of_messages = database.messages.count(Username = Username)
                print "#" + str(number_of_messages)
                if number_of_messages:
                    self.response.write('Number of messages sent: ' + str(number_of_messages))
                else:
                    self.response.write('No message has been sent by this user, yet')
            except Exception as e:
                print e
                self.response.write("User doesn't exist, yet")
        else:
            number_of_messages = database.messages.count()
            print "#" + str(number_of_messages)
            if number_of_messages:
                self.response.write('Number of messages sent: ' + str(number_of_messages))
            else:
                self.response.write('No message has been sent, yet')

class MessagesList(webapp2.RequestHandler):
    def get(self, RoomID = None, Username = None):
        if RoomID:
            try:
                message_list = database.messages.get(RoomID = RoomID)
                print message_list
                if message_list:
                    self.response.write('List of messages of room: ' + str(RoomID))
                    self.response.write(message_list)
                else:
                    self.response.write('No message has been sent in this room, yet')
            except Exception as e:
                if DEBUG:
                    print e
                self.response.write("Room doesn't exist, yet")
        elif Username:
            try:
                message_list = database.messages.get(Username = Username)
                print message_list
                if message_list:
                    self.response.write('List of messages of user: ' + str(Username))
                    self.response.write(message_list)
                else:
                    self.response.write('No message has been sent by this user, yet')
            except Exception as e:
                print e
                self.response.write("User doesn't exist, yet")
        else:
            message_list = database.messages.get()
            print message_list
            if message_list:
                self.response.write('List of messages: ')
                self.response.write(message_list)
            else:
                self.response.write('No message has been sent, yet')

####################### Servers ########################

class Servers(webapp2.RequestHandler):
    def get(self, ServerID = None):
        try:
            data = database.servers.get(ServerID)
            self.response.write(json.dumps(data))
        except Exception as e:
            if DEBUG:
                print "GET Server"
                print e
            self.response.write(json.dumps({}))

    def post(self, ServerID = None):
        try:
            data = json.loads(self.request.body)
            new_server = {}
            new_server["ServerID"] = data["ServerID"]
            new_server["host"] = data["host"]
            new_server["pub_port"] = data["pub_port"]
            new_server["pull_port"] = data["pull_port"]
            if database.servers.insert(new_server):
                self.response.write('OK')
            else:
                self.response.write('FAIL')
        except Exception as e:
            if DEBUG:
                print "POST Server"
                print e
            self.response.write('FAIL')

    def delete(self, ServerID):
        try:
            database.servers.remove(str(ServerID))
            self.response.write('OK')
        except Exception as e:
            if DEBUG:
                print "Delete Server"
                print e
            self.response.write('FAIL')

class BestServer(webapp2.RequestHandler):
    def get(self):
        best_server = {}
        best = -1
        servers = database.servers.get()
        try:
            if servers:
                for server in servers:
                    rooms = database.rooms.get(ServerID = server["ServerID"])
                    n_users = 0
                    if rooms:
                        for room in rooms:
                            n_users += database.users.count(RoomID = room["RoomID"])
                        print n_users
                        if best == -1 or best > n_users:
                            best = n_users
                            best_server = server
                    else:
                        best = 0
                        best_server = server
                self.response.write(json.dumps(best_server))
            else:
                self.response.write(json.dumps({}))
        except Exception as e:
            if DEBUG:
                print "Best server"
            	print e
            self.response.write(json.dumps({}))

####################### Rooms ##########################

class Rooms(webapp2.RequestHandler):
    def get(self, RoomID = None):
        try:
            if RoomID:
                room = database.rooms.get(RoomID = RoomID)
                print room
                self.response.write(json.dumps(room))
            else:
                rooms = database.rooms.get()
                self.response.write(json.dumps(rooms))
        except Exception as e:
            if DEBUG:
                print "GET Rooms"
                print e
            self.response.write(json.dumps({}))

    def post(self, RoomID = None):
        try:
            data = json.loads(self.request.body)
            RoomID = str(data["RoomID"])
            new_room = {}
            new_room["RoomID"] = RoomID
            new_room["messages"] = []
            new_room["server"] = data["server"]
            first_user_name = data["first_user"]
            database.rooms.insert(new_room)
            data = {"current_room": RoomID}
            if database.users.update(first_user_name, data):
                self.response.write('OK')
            else:
                self.response.write('FAIL')
        except Exception as e:
            if DEBUG:
                print "POST Rooms"
                print e
            self.response.write('FAIL')

    def put(self, RoomID):
        try:
            data = json.loads(self.request.body)
            room = database.rooms.get(str(RoomID))
            data = {"server": data.get("server")}
            if database.rooms.update(RoomID, data):
                self.response.write('OK')
            else:
                self.response.write('FAIL')
        except Exception as e:
            if DEBUG:
                print "PUT Rooms"
                print e
            self.response.write('FAIL')

####################### Users ###########################

class Users(webapp2.RequestHandler):
    def get(self, UserName = None):
        try:
            if UserName:
                user = database.users.get(Username = UserName)
                self.response.write(json.dumps(user))
            else:
                users = database.users.get()
                self.response.write(json.dumps(users))
        except Exception as e:
            if DEBUG:
                print "GET Users"
                print e
            self.response.write(json.dumps({}))

    def post(self, UserName = None):
        try:
            data = json.loads(self.request.body)
            username = str(data["username"])
            new_user = {}
            new_user["username"] = username
            new_user["current_room"] = None
            new_user["status"] = "ON"
            if database.users.insert(new_user):
                self.response.write('OK')
            else:
                self.response.write('FAIL')
        except Exception as e:
            if DEBUG:
                print "POST Users"
                print e
            self.response.write('FAIL')

    def put(self, UserName):
        try:
            print "PASCOA"
            data = json.loads(self.request.body)
            command = data["command"]
            print command
            if command == "login":
                data = {"status": "ON"}
                if database.users.update(UserName, data):
                    self.response.write('OK')
                else:
                    self.response.write('FAIL')
            elif command == "logout":
                data = {"status": "OFF"}
                if database.users.update(UserName, data):
                    self.response.write('OK')
                else:
                    self.response.write('FAIL')
            elif command == "enter":
                RoomID = data["RoomID"]
                data = {"current_room": RoomID}
                if database.users.update(UserName, data):
                    self.response.write('OK')
                else:
                    self.response.write('FAIL')
            elif command == "exit":
                data = {"current_room": None}
                if database.users.update(UserName, data):
                    self.response.write('OK')
                else:
                    self.response.write('FAIL')
        except Exception as e:
            if DEBUG:
                print "PUT Users"
                print e
            self.response.write('FAIL')

################## Mensages #######################

class Messages(webapp2.RequestHandler):
    def get(self):
        try:
            messages = database.messages.get()
            self.response.write(messages)
        except Exception as e:
            if DEBUG:
                print "GET Message"
                print e
            self.response.write([])

    def post(self):
        try:
            new_message = {}
            data = json.loads(self.request.body)
            new_message["from"] = data["from"]
            new_message["message"] = data["message"]
            RoomID = data["RoomID"]
            new_message["RoomID"] = RoomID
            InnerID = database.messages.count(RoomID = RoomID)
            OuterID =  database.messages.count()
            new_message["InnerID"] = InnerID
            new_message["OuterID"] = OuterID
            if database.messages.insert(new_message):
                self.response.write('OK')
            else:
                self.response.write('FAIL')
        except Exception as e:
            if DEBUG:
                print "POST Messages"
                print e
            self.response.write('FAIL')

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', MainPage),

    webapp2.Route(r'/html/users/', UsersList),
    webapp2.Route(r'/html/users/count', UsersCount),
    webapp2.Route(r'/html/<RoomID:\w+>/users/count', UsersCount),
    webapp2.Route(r'/html/<RoomID:\w+>/users', UsersList),

    webapp2.Route(r'/html/messages', MessagesList),
    webapp2.Route(r'/html/messages/count', MessagesCount),
    webapp2.Route(r'/html/users/<Username:\w+>/messages', MessagesList),
    webapp2.Route(r'/html/users/<Username:\w+>/messages/count', MessagesCount),
    webapp2.Route(r'/html/<RoomID:\w+>/messages/count', MessagesCount),
    webapp2.Route(r'/html/<RoomID:\w+>/messages', MessagesList),

    webapp2.Route(r'/nameserver/servers/<ServerID:[\w-]*>', Servers),
    webapp2.Route(r'/nameserver/bestserver', BestServer),
    webapp2.Route(r'/nameserver/rooms/<RoomID:\w*>', Rooms),
    webapp2.Route(r'/nameserver/users/<UserName:\w*>', Users),

    webapp2.Route(r'/server/messages', Messages),

], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='7000')

if __name__ == '__main__':
    main()

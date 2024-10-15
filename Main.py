# This is the file that runs the Flask service

# Import the managers
from AccountManager import AccountManager
from DatabaseManager import DatabaseManager
from TransactionManager import TransactionManager
from LogManager import LogManager
from BlockManager import BlockManager

# Import Libraries
import sqlite3 #Enables database functions
import re #Regular Expressions for password validation

from flask import Flask, render_template, request, redirect, make_response, url_for #Flask for web service

#Initialise Managers and Flask app
am = AccountManager()
dm = DatabaseManager()
tm = TransactionManager()
lm = LogManager()
bm = BlockManager()

app = Flask(__name__)


# Check if the user is blocked, before loading any page
@app.before_request
def checkBlock():
    ip_address = request.remote_addr

    dm.Manager_Start()
    block = dm.Get_Block_Entry_IPAddress(ip_address)
    dm.Manager_Stop()

    if block:
        if bm.Block_Expired(block) == False:
            return render_template('blocked.html')
        else:
            dm.Manager_Start()
            dm.Remove_Block(block)
            dm.Manager_Stop()
            
# Main page
@app.route("/")
def index():
    if "UserId" in request.cookies:
        # If the user is already logged in, redirect to the dashboard
        return redirect('/dashboard')
    else:
        # Otherwise, show the index page
        return render_template('index.html')

# Login page
@app.route("/login", methods=['GET', 'POST'])
def login(): 
    ip_address = request.remote_addr # Get the IP address of the user
    if request.method == 'GET':
        # If the user loads this page using a GET request, show the login page

        if "LoginCounter" in request.cookies:

            # If the user has tried to login more than 3 times, block the user
            if int(request.cookies.get("LoginCounter")) >= 3:
                try:
                    dm.Manager_Start() # Start the database manager
                    logEntry = lm.Create_Log(None, None, "User Blocked", ip_address) # Create a log entry
                    block = bm.Create_Block(ip_address) # Create a block entry in the database
                    dm.Add_Log_Entry(logEntry)
                    dm.Add_Block(block)

                finally:
                    # Stop the database manager, even if there is an error
                    dm.Manager_Stop()

                return render_template('blocked.html') # Redirect the user to the blocked page
            else:
                return render_template('login.html', error_message="Incorrect Username or Password") # Show the login page with an error message
            
        return render_template('login.html') # Show the login page
    
    if request.method == 'POST':
        # If the user submits the form, check the username and password

        # Get the username and password from the form
        username = request.form['username']
        password = request.form['password']

        if am.Login(username, password) == False: # If the login is incorrect
            response = make_response(redirect('/login')) # Redirect the user to the login page, using a GET request
            
            if "LoginCounter" in request.cookies: # If the user has tried to login before

                loginCounter = int(request.cookies.get("LoginCounter")) + 1 # Increment the login counter
            else:
                loginCounter = 1 # Otherwise, set the login counter to 1
                
            # Give the User a cooke with the login counter, set to expire in 24 hours
            response.set_cookie("LoginCounter", str(loginCounter), max_age=86400)

            try:
                # Generate a log entry for the failed login
                # If the username is incorrect, getting the account will fail, and the except block will run

                dm.Manager_Start() # Start the database manager
                user = dm.Get_Account_Username(username)
                logEntry = lm.Create_Log(user.Get_UUID(), None, "Failed Login - Password incorrect", ip_address)
            except:
                logEntry = lm.Create_Log(None, None, "Failed Login - Username incorrect", ip_address)
            finally:
                dm.Add_Log_Entry(logEntry) # Adds the Log Entry to the database
                dm.Manager_Stop() # Stop the database manager, even if there is an error

            return response
            
        #Sets the current user to the account object returned by the login function
        user = am.Login(username, password)

        # Redirect the user to their dashboard
        response = make_response(redirect('/dashboard'))

        # Set a cookie with the user's UUID, set to expire in 1 hour
        # This is used to keep the user logged in, and help the program identify the user
        response.set_cookie('UserId', user.Get_UUID(), max_age=3600) 

        # Reset the Login Counter
        if "LoginCounter" in request.cookies:
            response.delete_cookie('LoginCounter')

        try:
            dm.Manager_Start() # Start the database manager
            logEntry = lm.Create_Log(user.Get_UUID(), None, "Successful Login", ip_address) # Create + add a log entry
            dm.Add_Log_Entry(logEntry)
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        return response

# Signup page
@app.route("/signup", methods=['GET', 'POST'])
def Signup():
    ip_address = request.remote_addr # Get the IP address of the user

    if request.method == 'GET': # If the user loads the page using a GET request, load the page
        return render_template('signup.html')
    
    if request.method == 'POST':
        # If the user submits the form, create a new account

        username = request.form['username']
        password = request.form['password']
        fName = request.form['fName']
        lName = request.form['lName']


        # If the password does not match the regex, show an error message
        # The regex checks for the following:
        # - 8-16 characters
        # - At least one number
        # - At least one uppercase/lowercase letter
        # - At least one special character

        if re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[A-Z])(?=.*[-\#\$\.\%\&\*\@\^\(\)\+\-\_\=\{\}\[\]\|\?\,\.\<\>\;\:\'\!\"\&])(?=.*[a-zA-Z]).{8,16}$', password) == None:

            errorMessage = "Password must contain:_8-16 characters_At least one number_At least one uppercase / lowercase letter_At least one special character".split("_") 
            return render_template('signup.html', error_message=errorMessage) # Show the signup page with an error message

        else:
            # If the password is valid, create a new account
            user = am.Create_User(username, fName, lName, "user", password) 

        try:
            dm.Manager_Start() # Start the database manager
            dm.Add_Account(user) # Attempts to add the account to the database
        except sqlite3.IntegrityError: # Error is thrown when a unique field collides
            dm.Manager_Stop()
            return render_template('signup.html', error_message="Username Taken, try again.") # Show the signup page with an error message
        else:
            logEntry = lm.Create_Log(user.Get_UUID(), None, "User Successfully signed up", ip_address) # Create a log entry
            dm.Add_Log_Entry(logEntry)
            dm.Manager_Stop() # Stop the database manager
            return redirect('/login') # Redirect the user to the login page, to login with their new account
    
# Dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    ip_address = request.remote_addr # Get the IP address of the user
    isAdmin = Check_Admin(ip_address, "User accessed dashboard") # Check if the user is an admin

    if isAdmin == None:
        return redirect("/login") # If the user is not logged in, redirect to the login page

    if request.method == 'GET': # If the user loads the page using a GET request

        if "UserId" in request.cookies:
            try:
                dm.Manager_Start() # Start the database manager
                user = dm.Get_Account_UUID(request.cookies.get("UserId")) # Get the user object from the database
            finally:
                dm.Manager_Stop() # Stop the database manager, even if there is an error
        
        # If the user is an admin, show the admin dashboard
        if isAdmin:
            try:
                dm.Manager_Start() # Start the database manager
                logEntry = lm.Create_Log(user.Get_UUID(), None, "Admin Dashboard Accessed", ip_address) # Create a log entry
                allLogs = dm.Get_All_Logs() # Get the most recent log entries from the database
                dm.Add_Log_Entry(logEntry)  # Add the log entry to the database
            finally:
                dm.Manager_Stop() # Stop the database manager, even if there is an error

            recentLogs = []
            logCounter = 0

            for log in allLogs:
                recentLogs.append({
                    "Username1":log.Get_User1_ID(),
                    "Username2":log.Get_User2_ID(),
                    "EventType":log.Get_Event_Type(), 
                    "IPAddress":log.Get_IP_Address(), 
                    "DateTime":log.Get_Date_Time()})
                
                logCounter += 1

                if logCounter == 15:
                    break

            return render_template('adminDashboard.html', fName=user.Get_fName(), lName=user.Get_lName(), admin = True, logs=recentLogs) # Show the admin dashboard
        else:
            # If the user is not an admin, show the user dashboard
            try:
                dm.Manager_Start() # Start the database manager
                transList = dm.Get_Transaction_UserID(user.Get_UUID()) # Loads the transactions associated with the user
                logEntry = lm.Create_Log(user.Get_UUID(), None, "User Dashboard Accessed", ip_address) # Create a log entry
                dm.Add_Log_Entry(logEntry) # Add the log entry to the database
            finally:
                dm.Manager_Stop() # Stop the database manager, even if there is an error

            return render_template('userDashboard.html', fName=user.Get_fName(), lName=user.Get_lName(), balance="{:.2f}".format(float(user.Get_Balance())), transactions=transList) # Show the user dashboard
        
    if request.method == 'POST': # If the user attempts to make a transaction

        if "UserId" in request.cookies:
            try:
                dm.Manager_Start() # Start the database manager
                user = dm.Get_Account_UUID(request.cookies.get("UserId")) # Get the user object from the database
            finally:
                dm.Manager_Stop() # Stop the database manager, even if there is an error

        amount = request.form['amount'] # Get the amount from the form

        if request.form['button'] == 'deposit': # If the user is depositing money
            user.Set_Balance(user.Get_Balance() + float(amount))  # Add the amount to the user's balance

        elif request.form['button'] == 'withdraw': # If the user is withdrawing money
            if user.Get_Balance() - float(amount) > 0.01:
                user.Set_Balance(user.Get_Balance() - float(amount)) # Subtract the amount from the user's balance
            else:
                return redirect(url_for('dashboard', alert="Withdraw Error")) # If the user does not have enough money, redirect to the dashboard with an alert

        # Create a log entry and a transaction entry
        logEntry = lm.Create_Log(user.Get_UUID(), None, "User " + request.form['button'] + " " + str(amount), ip_address)
        transaction = tm.Create_Transaction(user.Get_UUID(), request.form['button'], amount)

        try:
            dm.Manager_Start() # Start the database manager
            dm.Edit_Balance(user, user.Get_Balance()) # Edit the user's balance in the database
            dm.Add_Transaction(transaction) # Applies the transaction and adds a log entry
            dm.Add_Log_Entry(logEntry)
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        return redirect('/dashboard') # Reload the dashboard, to show the updated balance and transaction history

# Signout page
@app.route('/signout')
def signout():
    ip_address = request.remote_addr # Get the IP address of the user
    response = make_response(redirect('/')) # Redirect the user to the main page, afer loading the page

    if "UserId" in request.cookies: # If the user is logged in
        try:
            dm.Manager_Start() # Start the database manager
            user = dm.Get_Account_UUID(request.cookies.get("UserId"))
            logEntry = lm.Create_Log(user.Get_UUID(), None, "User successfully signed out", ip_address) # Create a log entry
            dm.Add_Log_Entry(logEntry) # Add the log entry to the database
        finally:
            dm.Manager_Stop()

        response.delete_cookie('UserId') # Delete the cookie with the user's UUID, effectively logging the user out

    return response

# THE FOLLOWING PAGES ARE ACCESSIBLE BY ONLY THE ADMIN
# ENSURE TO CHECK THAT THE USER IS AN ADMIN BEFORE LOADING THE PAGE

# Logs page
@app.route('/logs', methods=['GET', 'POST'])
def viewLogs():
    if request.method == 'GET': # If the user loads the page using a GET request
        ip_address = request.remote_addr # Get the IP address of the user

        isAdmin = Check_Admin(ip_address, "User accessed logs page") # Check if the user is an admin


        if isAdmin == None:    
            return redirect('/login') # If the user is not logged in, redirect to the login page
        if isAdmin == False:    
            return redirect('/dashboard') # If the user is not an admin, redirect to the user dashboard
        
        try:
            dm.Manager_Start() # Start the database manager
            logList = dm.Get_All_Logs() # Get all log entries and usernamea from the database
            usernameList = dm.Get_All_Usernames()
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        # Create a list of log entries to display

        logLists = [""]
        for log in logList:
            if log.Get_User1_ID() == None:

                logLists.append({
                    "EventType":log.Get_Event_Type(), 
                    "IPAddress":log.Get_IP_Address(), 
                    "DateTime":log.Get_Date_Time()})

        return render_template('logs.html', usernames=usernameList, genericLogs=logLists, admin=True) # Show the logs page
        
    if request.method == 'POST': # If the user attempts to search for a specific user's logs

        # Check if the user is an admin
        if "UserId" in request.cookies:
            try:
                dm.Manager_Start() # Start the database manager
                user = dm.Get_Account_UUID(request.cookies.get("UserId"))
            finally:
                dm.Manager_Stop() # Stop the database manager, even if there is an error

            if user.Get_Role() != 'admin':
                logEntry = lm.Create_Log(user.Get_UUID(), None, "Unauthorized User attempted to access logs", ip_address) # Report the attempted unauthorized access
                
                try:
                    dm.Manager_Start() # Start the database manager
                    dm.Add_Log_Entry(logEntry) # Add the log entry to the database
                finally:
                    dm.Manager_Stop() # Stop the database manager, even if there is an error
                    return redirect('/dashboard') # If the user is not an admin, redirect to the user dashboard
            else: 
                return redirect('/login') # If the user is not logged in, redirect to the login page
        
        username = request.form['username'] # Get the username from the form

        try:
            dm.Manager_Start() # Start the database manager
            user = dm.Get_Account_Username(username) # Get the user object as well as all of the user's logs from the database
            logList = dm.Get_Log_Entry_User1ID(user.Get_UUID())
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error
        
        # Create a list of log entries to display

        logLists = [""]

        for log in logList:
            try:
                dm.Manager_Start() # Start the database manager
                user2 = dm.Get_Account_UUID(log.Get_User2_ID()) # Get the user object of the second user in the log entry
            finally:
                dm.Manager_Stop()  # Stop the database manager, even if there is an error

            if user2 == False:
                user2Username = "None" # If user2 does not exist, set the username to "None"
            else:
                user2Username = user2.Get_Username() # Otherwise, display the username of user2

            logLists.append({
                "Username1":user.Get_Username(), 
                "Username2":user2Username,
                "EventType":log.Get_Event_Type(), 
                "IPAddress":log.Get_IP_Address(), 
                "DateTime":log.Get_Date_Time()})
        try:
            dm.Manager_Start() # Start the database manager
            usernameList = dm.Get_All_Usernames() # Get all usernames from the database
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        return render_template('logs.html', userLogs=logLists, usernames=usernameList, fName=user.Get_fName(), lName=user.Get_lName(), admin=True) # Show the logs page

# Manage Users Page
@app.route("/manage-users", methods=['GET', 'POST'])
def Manage_Users():
    if request.method == 'GET': # If the user loads the page using a GET request
        ip_address = request.remote_addr # Get the IP address of the user

        # Check if the user is an admin
        isAdmin = Check_Admin(ip_address, "Admin accessed manage users page")
        
        if isAdmin == None:
            return redirect('/login') # If the user is not logged in, redirect to the login page
        elif isAdmin == False:
            return redirect('/dashboard') # If the user is logged in, redirect to their dashboard
        
        # Create a list of users to display

        userList = []

        try:
            dm.Manager_Start() # Start the database manager
            usernameList = dm.Get_All_Usernames() # Get all usernames from the database

            for username in usernameList:

                user = dm.Get_Account_Username(username)
                
                userList.append({
                    "uuid":user.Get_UUID(),
                    "username":user.Get_Username(), 
                    "fName":user.Get_fName(), 
                    "lName":user.Get_lName(),
                    "role":user.Get_Role()})
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error
            
        return render_template('manageUsers.html', userList=userList, admin=True) # Show the manage users page
    
    if request.method == 'POST': # If the user loads the page using a GET request
        ip_address = request.remote_addr # Get the IP address of the user

        # Check if the user is an admin
        isAdmin = Check_Admin(ip_address, "Admin accessed manage users page")
        
        if isAdmin == None:
            return redirect('/login') # If the user is not logged in, redirect to the login page
        elif isAdmin == False:
            return redirect('/dashboard') # If the user is logged in, redirect to their dashboard
        
        manageType = request.form['manageButton'] # Get the type of management request from the form

        if manageType == "delete":
            return redirect('/delete-user') # If the user wants to delete a user, redirect to the delete user page

        elif manageType == "add":
            return redirect('/add-user') # If the user wants to add a user, redirect to the add user page
        else:
            return render_template('addUser.html', admin=True) # Something has went wrong, reload the page

# Add User Page
@app.route("/delete-user", methods=['GET', 'POST'])
def Delete_User():
    if request.method == 'GET' or request.method == 'POST':
        ip_address = request.remote_addr # Get the IP address of the user

        # Check if the user is an admin
        isAdmin = Check_Admin(ip_address, "Admin Accessed add user page")

        if isAdmin == None:
            return redirect('/login') # If the user is not logged in, redirect to the login page
        elif isAdmin == False:
            return redirect('/dashboard') # If the user is not an admin, redirect to the user dashboard

        try:
            dm.Manager_Start() # Start the database manager
            usernameList = dm.Get_All_Usernames() # Get all usernames from the database
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        try:
            request.form['username']
        except:
            return render_template('deleteUser.html', usernames=usernameList, admin=True) # Show the delete user page

        username = request.form['username'] # Get the username from the form

        dm.Manager_Start() # Start the database manager
        user = dm.Get_Account_Username(username) # Get the user object from the database
        logEntry = lm.Create_Log(user.Get_UUID(), None, "Admin Successfully deleted user " + username, ip_address) # Create a log entry
        dm.Add_Log_Entry(logEntry)
        dm.Remove_Account(user) # Remove the user from the database
        dm.Manager_Stop() # Stop the database manager

        return redirect('/manage-users') # Redirect the user to the manage users page

# Add User Page
@app.route("/add-user", methods=['GET', 'POST'])
def Add_User():
    if request.method == 'GET':
        ip_address = request.remote_addr # Get the IP address of the user

        # Check if the user is an admin
        isAdmin = Check_Admin(ip_address, "Admin Accessed add user page")

        if isAdmin == None:
            return redirect('/login') # If the user is not logged in, redirect to the login page
        elif isAdmin == False:
            return redirect('/dashboard') # If the user is not an admin, redirect to the user dashboard

        return render_template('addUser.html', admin=True) # Show the add user page
    
    if request.method == 'POST':
        try:
            request.form['username']
        except:
            return render_template('addUser.html', admin=True) # Show the add user page
        
        ip_address = request.remote_addr # Get the IP address of the user

        # Get deatils of new user from the form
        username = request.form['username']
        password = request.form['password']
        fName = request.form['fName']
        lName = request.form['lName']
        role = request.form['role']

        # If the password does not match the regex, show an error message
        # The regex checks for the following:
        # - 8-16 characters
        # - At least one number
        # - At least one uppercase/lowercase letter
        # - At least one special character

        if re.match(r'^(?=.*\d)(?=.*[a-zA-Z])(?=.*[A-Z])(?=.*[-\#\$\.\%\&\*\@\^\(\)\+\-\_\=\{\}\[\]\|\?\,\.\<\>\;\:\'\!\"\&])(?=.*[a-zA-Z]).{8,16}$', password) == None:

            errorMessage = "Password must contain:_8-16 characters_At least one number_At least one uppercase / lowercase letter_At least one special character".split("_") 
            return render_template('addUser.html', error_message=errorMessage, admin=True) # Show the Add User page with an error message

        else:
            # If the password is valid, create a new account
            user = am.Create_User(username, fName, lName, role, password) 

        try:
            dm.Manager_Start() # Start the database manager
            dm.Add_Account(user) # Attempts to add the account to the database
        except sqlite3.IntegrityError: # Error is thrown when a unique field collides
            dm.Manager_Stop()
            return render_template('signup.html', error_message="Username Taken, try again.", admin=True) # Show the Add User page with an error message
        else:
            logEntry = lm.Create_Log(user.Get_UUID(), None, "Admin Successfully created user " + username, ip_address) # Create a log entry
            dm.Add_Log_Entry(logEntry)
            dm.Manager_Stop() # Stop the database manager
            return redirect('/manage-users') # Redirect the user to the manage users page, to view the new user


def Check_Admin(ipAddress, logText):
    if "UserId" in request.cookies:
        try:
            dm.Manager_Start() # Start the database manager
            user = dm.Get_Account_UUID(request.cookies.get("UserId"))
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        if user.Get_Role() == 'admin':
            logEntry = lm.Create_Log(user.Get_UUID(), None, logText, ipAddress) # Create a log entry
            admin = True
        else:
            logEntry = lm.Create_Log(user.Get_UUID(), None, "Unauthorized User attempted to perform an admin action", ipAddress) # Report the attempted unauthorized access
            admin = False

        try:
            dm.Manager_Start() # Start the database manager
            dm.Add_Log_Entry(logEntry) # Add the log entry to the database
        finally:
            dm.Manager_Stop() # Stop the database manager, even if there is an error

        return admin

    else:
        return None

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
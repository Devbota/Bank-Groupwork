Overview
This repository contains the code for the NeXTSafe Bank web-based banking application developed using Python's Flask framework. It implements secure user and admin functionality for online banking operations, including account management, transactions, and secure authentication.

Code Overview
Main.py:
Runs the Flask app, handling user routes, login, transactions, and account management.

AccountClass.py & AccountManager.py:
Define and manage user accounts, including balance updates and encrypted data handling.

BlockClass.py & BlockManager.py:
Implement blockchain-based security for tamper-proof transaction logs.

DatabaseManager.py:
Manages interactions with the SQLite database (SDSDB.db), handling user, transaction, and log data.

LogClass.py & LogManager.py:
Handle logging of user activities such as login attempts and transactions.

TransactionClass.py & TransactionManager.py:
Define and manage user transactions like withdrawals and deposits, with encryption.

Database (SDSDB.db)
User Table: Stores user credentials and account information.
Transaction Table: Logs user transactions (withdrawals, deposits).
Log Table: Tracks user activity such as logins and transactions.
Blockchain: Provides immutable transaction history for security.
Security Features
Password Hashing & Salting: Protects stored passwords.
Encryption: Secures user transaction data.
Blockchain: Ensures integrity of transaction history.

How to Run:
Run the application:
python Main.py
Access via browser:
http://localhost:5000
This banking app emphasizes security through encryption, password hashing, and blockchain logging. It is modular and designed for scalability.

import psycopg2
import datetime

class Andhra_Bank:
    def __init__(self):
        self.user = 'gowtham@inf'
        self.password = '130713'

    def connect_db(self):
        return psycopg2.connect(
            dbname="ANDHRA_BANK",
            user="postgres",
            password="root",
            host="localhost",
            port=5432
        )

    def deposit_amount(self, conn, cursor, table_name, result):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM {} 
            WHERE AADHAR_NO = {}
            ORDER BY ctid DESC LIMIT 1
        """.format(table_name, result[0]))
    
        result = cursor.fetchone()
        new_deposit = int(input("Enter Deposit Amount: "))
        new_balance = result[5] + new_deposit

        cursor.execute("""
            INSERT INTO {} (
                AADHAR_NO, FULL_NAME, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {})
        """.format(table_name, result[0], result[1], result[2], result[3],
                   result[4], new_balance, 0, new_deposit))

        conn.commit()
        cursor.close()

        print("\nTransaction:")
        print("Aadhar:", result[0])
        print("Name:", result[1])
        print("Deposited Amount:", new_deposit)
        print("New Balance:", new_balance)
        print("New deposit recorded.")

    def withdraw_amount(self, conn, cursor, table_name, result):
        conn = self.connect_db()        
        cursor = conn.cursor()  
        cursor.execute("""  
            SELECT * FROM {} 
            WHERE AADHAR_NO = {}
            ORDER BY ctid DESC LIMIT 1
        """.format(table_name, result[0]))
    
        result = cursor.fetchone()

        print("\nUser found. Last transaction:")
        print("Aadhar:", result[0])
        print("Name:", result[1])
        print("Balance:", result[5])

        withdraw_amount = int(input("Enter Withdraw Amount: "))

        if withdraw_amount > result[5]:
            print("Insufficient balance.")
            return
        if withdraw_amount < 0 or withdraw_amount > 100000:
            print("Withdraw amount must not exceed 100000.")
            return

        new_balance = result[5] - withdraw_amount
        print("New Balance after withdrawal:", new_balance)

        cursor.execute("""
            INSERT INTO {} (
                AADHAR_NO, FULL_NAME, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {})
        """.format(table_name, result[0], result[1], result[2], result[3],
                   result[4], new_balance, withdraw_amount, 0))

        conn.commit()
        cursor.close()
        print("New withdrawal recorded.")

    def mini_statement(self, conn, cursor, table_name, result):
        print("----SOLUTION_BANK----")
        print("Aadhar : ", result[0])
        print("Name :", result[1])
        print("phone_no :", result[3])
        print("Time :", datetime.datetime.now())
        print("Current Balance :", result[5])

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM {} WHERE AADHAR_NO = {}
        """.format(table_name, result[0]))
        transactions = cursor.fetchall()
        print("\n----TRANSACTION HISTORY----")
        print("Withdraw Amount | Deposit Amount | Balance")
        for transaction in transactions: 
            if transaction[6] != 0:
                withdraw = transaction[6]
            else:
                withdraw = 0 
            if transaction[7] != 0:
                deposit = transaction[7]
            else:
                deposit = 0 
            if transaction[5] != 0:
                balance = transaction[5]
            else:
                balance = 0
            print(" {}\t\t|{}\t\t\t|{}".format(withdraw, deposit, balance))
        cursor.close()

    def balance_enquiry(self, conn, cursor, table_name, result):
        conn = self.connect_db()    
        cursor = conn.cursor()  
        cursor.execute("""  
            SELECT * FROM {} 
            WHERE AADHAR_NO = {}
            ORDER BY ctid DESC LIMIT 1
        """.format(table_name, result[0]))
        result = cursor.fetchone()  
        cursor.close()
        print("\n----BALANCE ENQUIRY----")
        print("Time:", datetime.datetime.now())
        print("Name:", result[1])
        print("Current Balance:", result[5])

    def create_user(self, conn, cursor, table_name, aadhar_no):
        full_name = input("Enter Full Name: ")
        address = input("Enter Address: ")
        phone_no = int(input("Enter Phone Number: "))
        nominee_aadhar = int(input("Enter Nominee Aadhar Number: "))
        balance = int(input("Enter Initial Balance: "))
        withdraw = int(input("Enter Withdraw Amount: "))
        deposit = int(input("Enter Deposit Amount: "))

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO {} (
                AADHAR_NO, FULL_NAME, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR, BALANCE, WITHDRAW, DEPOSIT
            ) VALUES ({}, '{}', '{}', {}, {}, {}, {}, {})
        """.format(table_name, aadhar_no, full_name, address, phone_no,
                   nominee_aadhar, balance, withdraw, deposit))
        conn.commit()
        print("New user created.")

    def login(self):
        entered_user = input("Please enter the username: ")
        if entered_user == self.user:
            entered_password = input("Please enter the password: ")
            if entered_password == self.password:
                print("Login successful!")

                try:
                    conn = self.connect_db()
                    print("Database connected")
                    cursor = conn.cursor()

                    table_name = input("Enter Account Holder Name: ").strip()

                    try:
                        cursor.execute("""
                            CREATE TABLE {} (
                                AADHAR_NO BIGINT,
                                FULL_NAME VARCHAR(50),
                                ADDRESS VARCHAR(50),
                                PHONE_NO BIGINT,
                                NOMINEE_AADHAR BIGINT,
                                BALANCE BIGINT,
                                WITHDRAW INT,
                                DEPOSIT BIGINT
                            );
                        """.format(table_name))
                        conn.commit()
                        print("Acccount '{}' created.".format(table_name))
                    except psycopg2.errors.DuplicateTable:
                        conn.rollback()
                        print("Account '{}' already exists.".format(table_name))

                    aadhar_no = int(input("Enter Aadhar Number: "))
                    cursor.execute("""
                        SELECT * FROM {} 
                        WHERE AADHAR_NO = {}
                        ORDER BY ctid DESC LIMIT 1  
                    """.format(table_name, aadhar_no))
                    result = cursor.fetchone()

                    if result:
                        while True:
                            print("\nUser already exists.")
                            print("1. Deposit")
                            print("2. Withdraw")
                            print("3. Mini_statement")
                            print("4. Balance Enquiry")
                            print("5. Cancel")
                            choice = input("Choose option (1/2/3/4): ")

                            if choice == '1':
                                self.deposit_amount(conn, cursor, table_name, result)
                            elif choice == '2':
                                self.withdraw_amount(conn, cursor, table_name, result)
                            elif choice == '3':
                                self.mini_statement(conn, cursor, table_name, result)
                            elif choice == '4':
                                self.balance_enquiry(conn, cursor, table_name, result)
                            elif choice == '5':
                                print("\n----------------------------------------------")
                                print("     Thank you for using our Bank!")
                                print("             Visit again!")
                                return False
                            else:
                                print("Invalid choice.")
                    else:
                        print("User not found. Creating new user.")
                        self.create_user(conn, cursor, table_name, aadhar_no)

                except Exception as e:
                    print("ERROR:", e)

            else:
                print("Incorrect password.")
        else:
            print("Incorrect username.")

Andhra_Bank().login()

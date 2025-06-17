import psycopg2

class Andhra_Bank:
    def __init__(self):         
        self.user = 'Gowtham'
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
        print("\nUser found. Last transaction:")
        print("Aadhar:", result[0])
        print("Name:", result[1])
        print("Balance:", result[5])
        print("Withdraw:", result[6])
        print("Deposit:", result[7])

        new_deposit = int(input("Enter Deposit Amount: "))
        new_balance = result[5] + new_deposit

        cursor.execute(f"""
            INSERT INTO {table_name} (
                AADHAR_NO, FULL_NAME, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({result[0]}, '{result[1]}', '{result[2]}', {result[3]}, {result[4]}, {new_balance}, 0, {new_deposit})
        """)
        conn.commit()
        print("New deposit recorded.")

    def withdraw_amount(self, conn, cursor, table_name, result):
        print("\nUser found. Last transaction:")
        print("Aadhar:", result[0])
        print("Name:", result[1])
        print("Balance:", result[5])

        withdraw_amount = int(input("Enter Withdraw Amount: "))

        if withdraw_amount > result[5]:
            print("Insufficient balance.")
            return

        new_balance = result[5] - withdraw_amount

        cursor.execute(f"""
            INSERT INTO {table_name} (
                AADHAR_NO, FULL_NAME, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR, BALANCE, WITHDRAWL, DEPOSIT
            ) VALUES ({result[0]}, '{result[1]}', '{result[2]}', {result[3]}, {result[4]}, {new_balance}, {withdraw_amount}, 0)
        """)
        conn.commit()
        print("New withdrawal recorded.")

    def create_user(self, conn, cursor, table_name, aadhar_no):
        full_name = input("Enter Full Name: ")
        address = input("Enter Address: ")
        phone_no = int(input("Enter Phone Number: "))
        nominee_aadhar = int(input("Enter Nominee Aadhar Number: "))
        balance = int(input("Enter Initial Balance: "))
        withdraw = int(input("Enter Withdraw Amount: "))
        deposit = int(input("Enter Deposit Amount: "))

        cursor.execute(f"""
            INSERT INTO {table_name} (
                AADHAR_NO, FULL_NAME, ADDRESS, PHONE_NO,
                NOMINEE_AADHAR, BALANCE, WITHDRAW, DEPOSIT
            ) VALUES ({aadhar_no}, '{full_name}', '{address}', {phone_no}, {nominee_aadhar}, {balance}, {withdraw}, {deposit})
        """)
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

                    table_name = input("Enter Table Name: ").strip()

                    try:
                        cursor.execute(f"""
                            CREATE TABLE {table_name} (
                                AADHAR_NO BIGINT,
                                FULL_NAME VARCHAR(50),
                                ADDRESS VARCHAR(50),
                                PHONE_NO BIGINT,
                                NOMINEE_AADHAR BIGINT,
                                BALANCE BIGINT,
                                WITHDRAW INT,
                                DEPOSIT BIGINT
                            );
                        """)
                        conn.commit()
                        print(f"Table '{table_name}' created.")
                    except psycopg2.errors.DuplicateTable:
                        conn.rollback()
                        print(f"Table '{table_name}' already exists.")

                    aadhar_no = int(input("Enter Aadhar Number: "))
                    cursor.execute(f"""
                        SELECT * FROM {table_name} 
                        WHERE AADHAR_NO = %s
                        ORDER BY ctid DESC LIMIT 1
                    """, (aadhar_no,))
                    result = cursor.fetchone()

                    if result:
                        print("\nUser already exists.")
                        print("1. Deposit")
                        print("2. Withdraw")
                        choice = input("Choose option (1/2): ")

                        if choice == '1':
                            self.deposit_amount(conn, cursor, table_name, result)
                        elif choice == '2':
                            self.withdraw_amount(conn, cursor, table_name, result)
                        else:
                            print("Invalid choice.")
                    else:
                        print("User not found. Creating new user.")
                        self.create_user(conn, cursor, table_name, aadhar_no)

                    conn.close()

                except Exception as e:
                    print("ERROR:", e)

            else:
                print("Incorrect password.")
        else:
            print("Incorrect username.")

bank = Andhra_Bank()
bank.login()

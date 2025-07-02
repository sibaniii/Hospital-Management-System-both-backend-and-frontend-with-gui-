from prettytable import PrettyTable
from colorama import init, Fore, Style
import mysql.connector
import time
import csv

init(autoreset=True)

def show_dashboard(mycursor):
    print(Fore.BLUE + Style.BRIGHT + "\n======= DASHBOARD SUMMARY =======")
    mycursor.execute("SELECT COUNT(*) FROM patient_detail")
    total_patients = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM doctor_details")
    total_doctors = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM nurse_details")
    total_nurses = mycursor.fetchone()[0]
    mycursor.execute("SELECT COUNT(*) FROM other_workers_details")
    total_others = mycursor.fetchone()[0]
    total_employees = total_doctors + total_nurses + total_others

    print(f"🧍 Total Patients       : {total_patients}")
    print(f"🩺 Doctors              : {total_doctors}")
    print(f"👩‍⚕️ Nurses              : {total_nurses}")
    print(f"🧹 Other Staff          : {total_others}")
    print(f"👥 Total Employees      : {total_employees}")

def export_table_to_csv(mycursor, table_name):
    filename = table_name + ".csv"
    mycursor.execute(f"SELECT * FROM {table_name}")
    rows = mycursor.fetchall()
    headers = [i[0] for i in mycursor.description]

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(Fore.GREEN + f"✅ Exported '{table_name}' to '{filename}'")

while True:
    print(Fore.CYAN + Style.BRIGHT + """
    ===========================================
           Welcome To RUBY GROUP OF HOSPITALS
    ===========================================
    """)
    passwd = str(input("Enter the Password Please!!:"))

    mysql = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Sarvesh123!"
    )
    mycursor = mysql.cursor()
    mycursor.execute("create database if not exists ruby")
    mycursor.execute("use ruby")

    mycursor.execute("create table if not exists patient_detail(name varchar(30) primary key, sex varchar(15), age int(3), address varchar(50), contact varchar(15))")
    mycursor.execute("create table if not exists doctor_details(name varchar(30) primary key, specialisation varchar(40), age int(2), address varchar(30), contact varchar(15), fees int(10), monthly_salary int(10))")
    mycursor.execute("create table if not exists nurse_details(name varchar(30) primary key, age int(2), address varchar(30), contact varchar(15), monthly_salary int(10))")
    mycursor.execute("create table if not exists other_workers_details(name varchar(30) primary key, age int(2), address varchar(30), contact varchar(15), monthly_salary int(10))")
    mycursor.execute("create table if not exists user_data(username varchar(30) primary key, password varchar(30) default '000')")
    mycursor.execute("create table if not exists appointments(id int primary key auto_increment,patient_name varchar(100),doctor_name varchar(100),appointment_date date,appointment_time time,notes text)""")
    while True:
        print(Fore.YELLOW + """
                        1. Sign In
                        2. Registration
        """)
        r = int(input("Enter your choice:"))
        if r == 2:
            print(Fore.GREEN + """
                =======================================
                !!!!!!!!!! REGISTER YOURSELF !!!!!!!!!!
                =======================================
            """)
            u = input("Input your username!!:")
            p = input("Input the password (Password must be strong!!!):")
            mycursor.execute("insert into user_data values(%s, %s)", (u, p))
            mysql.commit()
            print(Fore.GREEN + "✅ Registration Done Successfully!\n")
            input("Enter any key to continue:")

        elif r == 1:
            print(Fore.GREEN + """
                    ==================================
                       !!!!!!!! SIGN IN !!!!!!!!!!
                    ==================================
            """)
            un = input("Enter Username!!:")
            ps = input("Enter Password!!:")
            mycursor.execute("select password from user_data where username=%s", (un,))
            row = mycursor.fetchall()
            for i in row:
                if i[0] == ps:
                    while True:
                        print(Fore.MAGENTA + """
                                1. Administration
                                2. Patient (Details)
                                3. Sign Out
                                4. View Dashboard
                                5. Export Data
                        """)
                        a = int(input("ENTER YOUR CHOICE:"))
                        if a == 1:
                            print("""
                                    1. Display the details
                                    2. Add a new member
                                    3. Delete a member
                                    4. Make an exit
                            """)
                            b = int(input("Enter your Choice:"))
                            if b == 1:
                                print("""
                                        1. Doctors Details
                                        2. Nurse Details
                                        3. Others
                                """)
                                c = int(input("Enter your Choice:"))
                                tables = ["doctor_details", "nurse_details", "other_workers_details"]
                                columns = [
                                    ["NAME", "SPECIALISATION", "AGE", "ADDRESS", "CONTACT", "FEES", "MONTHLY SALARY"],
                                    ["NAME", "AGE", "ADDRESS", "CONTACT", "MONTHLY SALARY"],
                                    ["NAME", "AGE", "ADDRESS", "CONTACT", "MONTHLY SALARY"]
                                ]
                                mycursor.execute(f"select * from {tables[c-1]}")
                                rows = mycursor.fetchall()
                                table = PrettyTable(columns[c-1])
                                for row in rows:
                                    table.add_row(row)
                                print(table)

                            elif b == 2:
                                print("""
                                        1. Doctor Details
                                        2. Nurse Details
                                        3. Others
                                """)
                                c = int(input("ENTER YOUR CHOICE:"))
                                if c == 1:
                                    data = [input(f"{field}: ") for field in ["Name", "Specialization", "Age", "Address", "Contact", "Fees", "Monthly Salary"]]
                                    mycursor.execute("insert into doctor_details values(%s,%s,%s,%s,%s,%s,%s)", tuple(data))
                                elif c == 2:
                                    data = [input(f"{field}: ") for field in ["Name", "Age", "Address", "Contact", "Monthly Salary"]]
                                    mycursor.execute("insert into nurse_details values(%s,%s,%s,%s,%s)", tuple(data))
                                elif c == 3:
                                    data = [input(f"{field}: ") for field in ["Name", "Age", "Address", "Contact", "Monthly Salary"]]
                                    mycursor.execute("insert into other_workers_details values(%s,%s,%s,%s,%s)", tuple(data))
                                mysql.commit()
                                print(Fore.GREEN + "SUCCESSFULLY ADDED")

                            elif b == 3:
                                print("""
                                        1. Doctor Details
                                        2. Nurse Details
                                        3. Others
                                """)
                                c = int(input("Enter your Choice:"))
                                tbl = ["doctor_details", "nurse_details", "other_workers_details"][c - 1]
                                name = input("Enter Name:")
                                mycursor.execute(f"select * from {tbl} where name=%s", (name,))
                                row = mycursor.fetchall()
                                print(row)
                                p = input("You really wanna delete this data? (y/n):")
                                if p.lower() == "y":
                                    mycursor.execute(f"delete from {tbl} where name=%s", (name,))
                                    mysql.commit()
                                    print(Fore.RED + "SUCCESSFULLY DELETED!!")
                                else:
                                    print("NOT DELETED")

                            elif b == 4:
                                break

                        elif a == 2:
                            print("""
                                        1. Show Patients Info
                                        2. Add New Patient
                                        3. Discharge Summary
                                        4. Exit
                            """)
                            b = int(input("Enter your Choice:"))
                            if b == 1:
                                mycursor.execute("select * from patient_detail")
                                rows = mycursor.fetchall()
                                table = PrettyTable(["NAME", "SEX", "AGE", "ADDRESS", "CONTACT"])
                                for row in rows:
                                    table.add_row(row)
                                print(table)

                            elif b == 2:
                                data = [input(prompt) for prompt in ["Name", "Gender", "Age", "Address", "Contact"]]
                                mycursor.execute("insert into patient_detail values(%s,%s,%s,%s,%s)", tuple(data))
                                mysql.commit()
                                print(Fore.GREEN + "Registered Successfully!")

                            elif b == 3:
                                name = input("Enter the Patient Name:")
                                mycursor.execute("select * from patient_detail where name=%s", (name,))
                                row = mycursor.fetchall()
                                print(row)
                                bill = input("Has the patient paid all the bills? (y/n):")
                                if bill.lower() == "y":
                                    mycursor.execute("delete from patient_detail where name=%s", (name,))
                                    mysql.commit()
                                    print(Fore.GREEN + "Patient discharged and deleted.")
                                else:
                                    print("Bills yet to be paid.")

                            elif b == 4:
                                break

                        elif a == 3:
                            break

                        elif a == 4:
                            show_dashboard(mycursor)
                            input("\nPress Enter to return to menu...")

                        elif a == 5:
                            print("""
                                    Which data do you want to export?
                                    1. Patient Details
                                    2. Doctor Details
                                    3. Nurse Details
                                    4. Other Workers
                                    5. Back
                            """)
                            c = int(input("Enter your choice:"))
                            table_map = {
                                1: "patient_detail",
                                2: "doctor_details",
                                3: "nurse_details",
                                4: "other_workers_details"
                            }
                            if c in table_map:
                                export_table_to_csv(mycursor, table_map[c])
                                input("\nPress Enter to return to menu...")
                            elif c == 5:
                                continue
                            else:
                                print("Invalid choice. Try again.")

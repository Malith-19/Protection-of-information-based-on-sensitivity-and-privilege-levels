import csv
import hashlib

# mapping of privileges to privilege levels

read_privileges = {
    'patient' : ['record_id','user_name','personal_details','sickeness_details','drug_prescriptions','lab_test_prescriptions'], 
    'lab staff' : ['record_id','user_name','personal_details','lab_test_prescriptions'], 
    'pharmacy staff' : ['record_id','user_name','personal_details','drug_prescriptions'], 
    'nurse' : ['record_id','user_name','personal_details','sickeness_details','drug_prescriptions','lab_test_prescriptions'], 
    'doctor' : ['record_id','user_name','personal_details','sickeness_details','drug_prescriptions','lab_test_prescriptions']
}

allowed_actions = {
    'patient' : ['view my records'], 
    'lab staff' : ['view all records', 'view all records by user name', 'view record by id'], 
    'pharmacy staff' : ['view all records', 'view all records by user name', 'view record by id'], 
    'nurse' : ['view all records', 'view all records by user name', 'view record by id'], 
    'doctor' : ['view all records', 'view all records by user name', 'view record by id', 'add new record']
}



# hashing the given string using md5
def hash(str_to_hash):
    return hashlib.md5(str_to_hash.encode()).hexdigest()

# reading the config csv and store the data in the 2d array
def read_csv(filename):
    data= []
    with open(filename,"r") as file:
        csvreader = csv.reader(file,delimiter=",")
        
        for row in csvreader:
            if row:
                data.append(row)
            
    return data

# writing a one row data to csv
def write_csv(filename,data):
    with open(filename,"a+",newline="") as file:
        csvwritter = csv.writer(file)
        csvwritter.writerow(data)
    
# validating if a given user exists already
def validate_user_exists(user_details,username):
    for user_data in user_details:
        if user_data[0] == username:
            return True,user_data
    return False,[]


    
# function to handle login
def login():
    username = input("Enter your username: ")
    
    is_username_valid, user_data = validate_user_exists(user_details,username)
    
    if not is_username_valid:
        while True:
            choice = input("Entered username is invalid!\nPlease select a choice to continue: \n1 - Re-enter the login details\n2 - Go to main menu\n")
            if choice == "1":
                return login()
            elif choice == "2":
                return False,[]
            else:
                print("Incorrect input. Please try again!\n")
    
    password = input("Enter your password: ") 
    
    if not user_data[1] == hash(password):
        while True:
            choice = input("Entered username is invalid!\nPlease select a choice to continue: \n1 - Re-enter the login details\n2 - Go to main menu\n")
            if choice == "1":
                login()
            elif choice == "2":
                return False,[]
            else:
                print("Incorrect input. Please try again!\n")
    
    print("Login successfull!")
    return True,user_data
                

# function to handle registeration
def register():
    global user_details
    
    username = input("Enter a username: ")
    is_user_valid,_ =  validate_user_exists(user_details,username)
    if is_user_valid:
        print("This username already exists. Please try a different one.")
        return register()
    
    password = input("Enter a password: ")
    hashed_password = hash(password)
    
    
    valid_user_type = False
    
    while not valid_user_type:
        user_type_choice = input("Enter the user type:\n1 - Patient\n2 - Hospital staff\n")
        valid_user_type = True
        if user_type_choice == "1":
            user_type = "patient"
            
        elif user_type_choice == "2":
            user_type = "hospital staff"
        else:
            print("Invalid input! Please try again.")
            
    if user_type == "patient":
        privilege_level = "patient"
    else:
        valid_privilege_level = False
        while not valid_privilege_level:
            privilege_level_choice = input("Enter your privilege level:\n1 - Lab staff\n2 - Pharmacy staff\n3 - Nurse\n4 - Doctor\n")
            valid_privilege_level = True
            
            if privilege_level_choice == "1":
                privilege_level = "lab staff"
            elif privilege_level_choice == "2":
                privilege_level = "pharmacy staff"
            elif privilege_level_choice == "3":
                privilege_level = "nurse"
            elif privilege_level_choice == "4":
                privilege_level = "doctor"
            else:
                print("Invalid input! Please try again.")
    
    user_data = [username,hashed_password,user_type,privilege_level]
    user_details.append(user_data)          
    
    write_csv("config.csv",user_data)
    print("Registration successfull!")
    return True

# adding a new record
def add_record():
    record_id = str(len(record_details)+1)
    
    username = input("Enter the patient username: ")
    is_user_valid,_ =  validate_user_exists(user_details,username)
    
    if not is_user_valid:
        print("This patient is not exist! please re-enter")
        return add_record()
    
    patient_details = input("Enter the patient details: ")
    sickness_details = input("Enter the sickness details: ")
    drug_description = input("Enter the drug description: ")
    lab_test_prescriptions = input("Enter the lab test prescriptions: ")
    
    record = [record_id,username,patient_details,sickness_details,drug_description,lab_test_prescriptions]
    write_csv("record.csv",record)
    record_details.append(record)

# getting records using record id
def get_record_by_id(id):
    if len(record_details)<id:
        return []
    
    return record_details[id-1]

# getting records using patient username
def get_records_by_username(username):
    output = []
    for record in record_details:
        if record[1] == username:
            output.append(record)
            
    return output

# helper function to show records to filter the fields in the records.
def filter_record(records,user_privilege):
    if user_privilege == "lab staff":
        for record in records:
            record.pop(4)
    elif user_privilege == "pharmacy staff":
        for record in records:
            record.pop(3)
    return records
        
# function to print the records with the filtering.        
def show_records(records,user_privilege):
    if records:
        print("Here the medical records!")
        filtered_records = filter_record(records,user_privilege)
        for record in filtered_records:
            print(" ".join(record))
        return
    else:
        print("No records found!")      
# generating action menu for given actions.
def generate_menu(actions):
    menu ="select a choice from below options.\n"

    i = 0
    for action in actions:
        i += 1
        menu += str(i)+" - "+action+"\n"
        
    return menu


# this will run given command with username and user privilege. This where user's actions running after login and they selects a action.
def do_action(action,username,user_privilege):
    if action == "view my records":
        records = get_records_by_username(username)
        show_records(records,user_privilege)
    elif action == "view all records":
        
        show_records(record_details,user_privilege)
    elif action == "view all records by user name":
        req_username = input("Enter the username of the patient: ")
        records = get_records_by_username(req_username)
        show_records(records,user_privilege)
        
    elif action == "view record by id":
        id = int(input("Enter the record ID: "))
        record = get_record_by_id(id)
        if record:
            show_records([record],user_privilege)
        else:
            show_records(record,user_privilege)
        
    elif action == "add new record":
        add_record()


# loading neccessary data
user_details = read_csv("config.csv")
record_details = read_csv("record.csv")


# Here the main function
def main():
    is_validate_option = False
    user_data = []

    while(not (is_validate_option and user_data )):
        option = input("Select a relevent number for login or register\n1 - Login\n2 - Register\n")
        if option == "1":
            is_validate_option,user_data=login()
            
        elif option == "2":
            is_validate_option= register()
        else:
            print("Invalid input. Please enter again choice 1 or 2.\n")
            
    username,user_type,user_privilege = user_data[0],user_data[2],user_data[3]
    
    actions = allowed_actions[user_privilege]
    menu = generate_menu(actions)
    
    while True:
        print(menu)
        choice = int(input("Enter your choice: "))
        if 1<=choice<=len(actions):
            do_action(actions[choice-1],username,user_privilege)
        else:
            print("Invalid input")
    
        
        
        
         
    
# running the main function.
main()
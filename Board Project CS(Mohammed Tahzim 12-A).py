import random
import mysql.connector as con
from prettytable import PrettyTable, from_db_cursor
def Table():
    x = PrettyTable()
    x.field_names = ["Name", "Wins", "Loses", "Tie", "Win Rate(%)"]
    x.add_row([Name, user_wins, computer_wins, Tie, win_rate])
    print(x)

db = con.connect(host = "localhost", user = "root", password = "#tahzim12")
mycursor = db.cursor()

#mycursor.execute("Create Database RPSGameData")
mycursor.execute("Use RPSGameData")
'''
mycursor.execute("Create Table Players (Name varchar(20) primary key, Phone int(20), Gender varchar(20), Age int(100))")
mycursor.execute("Create Table Results(Name varchar(20) primary key, Wins int(255), Losses int(255), Tie int(255))")
mycursor.execute("Create Table ScoreBoard( Name varchar (20) primary key, WinRatePercentage int(100))") 
mycursor.execute("Create Table StoreData(Name varchar (20), ItemPurchased varchar(20))")
'''
user_wins = 0
computer_wins = 0
Tie = 0
Players = []

rps = ["rock", "paper", "scissors"]

while True:
    print('''
    MAIN MENU
    1.Start Game
    2.Options
    3.Store
    4.Quit
    ''')
    n = int(input("Enter choice (1/2/3/4): "))
    if n==1:
        num=int(input("Enter number of players: "))
        for i in range (num):
            Name = input("Enter name: ")
            Phone = int(input("Enter Phone Number: "))
            Sex = input("Enter Gender(M/F): ").upper()
            Age = int(input("Enter age: "))
            if Age < 7:
                print("Players Under the age of 7 are not allowed to play")
                break
            else:
                mycursor.execute(f"Insert into Players values('{Name}',{Phone},'{Sex}',{Age})")
                db.commit()
            play = int(input("Number of times you want to play: "))
            

            for i in range (play):
                user = input("Type Rock/Paper/Scissors: ").lower()
                if user == "q":
                    break
                if user not in rps:
                    continue 
                num = random.randint(0,2)
                comp = rps[num]
                print("Computer: ",comp)
            
                if user == "rock" and comp =="scissors":
                    print("You won!")
                    user_wins +=1
                elif user == "paper" and comp =="rock":
                    print("You won!")
                    user_wins +=1
                elif user == "scissors" and comp =="paper":
                    print("You won!")
                    user_wins +=1
                elif user == "scissors" and comp =="scissors":
                    print("Tie")
                    Tie +=1
                elif user == "paper" and comp =="paper":
                    print("Tie")
                    Tie +=1    
                elif user == "rock" and comp =="rock":
                    print("Tie")
                    Tie +=1
                else:
                    print("You lost!")
                    computer_wins +=1
            win_rate = (user_wins/play)*100
            mycursor.execute(f"Insert into Results values('{Name}',{user_wins},{computer_wins},{Tie})")
            mycursor.execute(f"Insert into Scoreboard values('{Name}', {win_rate})")
            db.commit()
            print("Your Score")
            Table()
            user_wins = 0
            computer_wins = computer_wins - computer_wins
            print("Scoreboard")
            mycursor.execute("Select Results.Name, Results.Wins, Results.Losses, ScoreBoard.WinRatePercentage from Results,ScoreBoard where Results.Name=ScoreBoard.Name ")
            x = from_db_cursor(mycursor)
            print(x)
                
    if n==2:
        while True:
            print('''
            --------------------------------
            Options
            A. Display Scoreboard
            B. Display Details of Players
            C. Check Your Score
            D. Edit Your Profile
            E. Back To Main Menu
            --------------------------------
            ''')

            opt = input("Enter Choice (A/B/C/D/E): ").lower()
            if opt=="a":
                print("HIGHEST SCORE (WinRate)")
                mycursor.execute("Select*from ScoreBoard where WinRatePercentage = (Select max(WinRatePercentage) from ScoreBoard)")
                x = from_db_cursor(mycursor)
                print(x)
                

                print("------------------------------------------------------")

                print("SCORE BOARD")
                mycursor.execute("Select Results.Name, Results.Wins, Results.Losses, ScoreBoard.WinRatePercentage from Results, ScoreBoard where Results.Name = ScoreBoard.Name ")
                x = from_db_cursor(mycursor)
                print(x)

            if opt=="b":
                print("All PLayers")
                mycursor.execute("Select*from Players")
                x = from_db_cursor(mycursor)
                print(x)
                print("--------------")
                Search = input("Search Name: ")
                print("--------------")
                mycursor.execute(f"select*from ScoreBoard where Name = '{Search}'")
                x = from_db_cursor(mycursor)
                print(x)
                
            if opt=='c':
                Search = input("Enter Player Name: ")
                print("--------------")
                mycursor.execute(f"Select*from Results where Name = '{Search}'")
                x = from_db_cursor(mycursor)
                print(x)
            
            if opt=="d":
                while True:
                    print('''
                    --------------------
                    EDIT PROFILE
                    A. Edit Name
                    B. Edit Phone
                    C. Edit Gender
                    D. Edit Age
                    E. Back to Options
                    --------------------
                    ''')
                    
                    Edi = input("Enter Choice (A/B/C/D/E): ").lower()
                    if Edi=="a":
                        Oldname = input("Enter Current Name: ")
                        Newname = input("Enter New Name: ")
                        mycursor.execute(f"Update Players Set Name = '{Newname}' where Name = '{Oldname}'")
                        mycursor.execute(f"Update Results Set Name = '{Newname}' where Name = '{Oldname}'")
                        mycursor.execute(f"Update ScoreBoard Set Name = '{Newname}' where Name = '{Oldname}'")
                        db.commit()
                        print("Name Succesfully Updated")

                        mycursor.execute(f"Select*from Players where Name = '{Newname}'")
                        all = mycursor.fetchall()
                        for x in all:
                            print(x)
                    
                    if Edi=="b":
                        oldph = int(input("Enter Old Phone Number: "))
                        newph = int(input("Enter New Phone Number: "))
                        mycursor.execute(f"Update Players Set Phone = {newph} where Phone = {oldph}")
                        db.commit()
                        print("Phone Number Succesfully Updated")

                        mycursor.execute(f"Select*from Players where Phone = {newph}")
                        all = mycursor.fetchall()
                        for x in all:
                            print(x)
                    
                    if Edi=="c":
                        Name = input("Enter Name: ")
                        newg = input("Enter New Gender: ")
                        mycursor.execute(f"Update Players Set Gender = '{newg}' where Name = '{Name}'")
                        db.commit()
                        print("Gender Succesfully Updated")

                        mycursor.execute(f"Select*from Players where Name = '{Name}'")
                        all = mycursor.fetchall()
                        for x in all:
                            print(x)
                    
                    if Edi=="d":
                        Name = input("Enter Name: ")
                        newage = input("Enter New Age: ")
                        mycursor.execute(f"Update Players Set Age = '{newage}' where Name = '{Name}'")
                        db.commit()
                        print("Age Succesfully Updated")

                        mycursor.execute(f"Select*from Players where Name = '{Name}'")
                        all = mycursor.fetchall()
                        for x in all:
                            print(x)
                    if Edi=="e":
                        break

            if opt=="e":
                break

    if n==3:
        items = {"nike hoodie": 50, "casio watch": 20,"kitkat": 7, "chips": 2, "pencils": 3, "snickers": 7, "adidas shoes": 70, "logitech mouse": 40, "logitech keyboard": 46,
        "iphone 14": 100, "samsung s20 ultra": 100, "ring:": 10}
        print("WELCOME TO THE STORE")
        
        Search = input("Search Name: ")
        print("--------------------")        
        mycursor.execute(f"select Name, Wins from Results where Name = '{Search}'")
        x = from_db_cursor(mycursor)
        print(x)
        print("------------------------")

        x = PrettyTable()
        x.field_names = ["Items", "WinsRequired"]
        x.add_row(["Nike Hoodie", "27"])
        x.add_row(["Casio Watch", "15"])
        x.add_row(["Kitkat", "4"])
        x.add_row(["Chips", "2"])
        x.add_row(["Pencils", "3"])
        x.add_row(["Snickers", "4"])
        x.add_row(["Adidas Shoes", "30"])
        x.add_row(["logitech mouse", "11"])
        x.add_row(["logitech Keyboard", "15"])
        x.add_row(["Iphone 14", "100"])
        x.add_row(["Samsung S20 Ultra", "100"])
        x.add_row(["Ring", "10"])
        print(x)
        print("--------------------")
        buy = input("Enter Item Name: ").lower()

        mycursor.execute(f"select*from Results where Name = '{Search}'")
        all = mycursor.fetchall()
        for i in all:
            W = i[1]
        if items[buy] <= W:
            mycursor.execute(f"Insert into StoreData values('{Search}', '{buy}')")
            mycursor.execute(f"Update Results Set Wins = Wins - {items[buy]} where Name ='{Search}'")
            db.commit()
            print(buy, "Purchased")
            mycursor.execute(f"select Name, Wins from Results where Name = '{Search}'")
            x = from_db_cursor(mycursor)
            print(x)
        else:
            print("You dont have enough Wins to purchase this item")
            continue

    if n==4:
         break            
                




        


            

    
    


    







    

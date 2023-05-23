#Import modules
import json
import discord
import os
from pathlib import Path

#Functions

def reloadVars(): #Reload the values of all variables after a transaction
    print("Variables reloaded successfully")


def buy(symbol,buying,cost,onMarket,transact,formerOnMarket, b, W): #Buy function
    print(f"Buying {transact} shares from company {symbol}, which will now have {onMarket} shares available for purchase on the market (formerly {formerOnMarket} shares were available), with a total cost of ${cost}.")

    # Just in case the program throws a tantrum
    tempPth=Path(f"Temp\\{UID}.json")
    tempDct= {
        "symbol": symbol,
        "transaction": "buying",
        "buying": buying,
        "cost": cost,
        "onMarket": onMarket,
        "transact": transact,
        "formerOnMarket": formerOnMarket
    }
    j=json.dumps(tempDct, indent=4)
    with open(tempPth, "w") as outfile2:
        outfile2.write(j)
        print("Created a temporary JSON file to store information during transaction in case of unexpected behaviour.")

    uB=b-cost #New user value
    w=W+cost #New company value

    v=w/onMarket

    cDct = json.load(open(cPth, "r"))  # Load company JSON dictionary
    name = cDct['name']  # Save name of company
    sTtl = cDct['sTtl']  # Save total shares of company
    cDctApp = {
        "name": name,
        "smbl": smbl,
        "val": w,
        "sV": v,
        "sTtl": sTtl,
        "sAvl": onMarket
    }
    j = json.dumps(cDctApp, indent=4)
    with open(cPth, "w") as outfile3:
        outfile3.write(j)


def sell(symbol,selling,cost,onMarket,transact,formerOnMarket, b, W): #Selling function
    print(f"Selling {transact} shares back to company {symbol}, which will now have {onMarket} shares available for purchase on the market (formerly {formerOnMarket} shares were available), with a total income of ${cost}")
    # Just in case the program throws a tantrum
    tempPth = Path(f"Temp\\{UID}.json")
    tempDct = {
        "symbol": symbol,
        "transaction": "selling",
        "selling": selling,
        "cost": cost,
        "onMarket": onMarket,
        "transact": transact,
        "formerOnMarket": formerOnMarket
    }
    j = json.dumps(tempDct, indent=4)
    with open(tempPth, "w") as outfile2:
        outfile2.write(j)
        print("Created a temporary JSON file to store information during transaction in case of unexpected behaviour.")

    uB=b+cost #New user value
    w=W-cost #New company value

    v=w/onMarket
    cDct = json.load(open(cPth, "r"))  # Load company JSON dictionary
    name = cDct['name']  # Save name of company
    sTtl = cDct['sTtl']  # Save total shares of company
    cDctApp = {
        "name": name,
        "smbl": smbl,
        "val": w,
        "sV": v,
        "sTtl": sTtl,
        "sAvl": onMarket
    }
    j = json.dumps(cDctApp, indent=4)
    with open(cPth, "w") as outfile3:
        outfile3.write(j)

    uDctApp= {
        "UID": UID,
        "bal": uB
    }
    j = json.dumps(uDctApp, indent=4)
    with open(uPth, "w") as outfile3:
        outfile3.write(j)


def parseCmd(X, Q, N, T, P, B, nW): #This function had no reason to exist other than because Python was shitting itself processing the code without it
    if uIn == "sell":  # Selling shares
        if X < T or X == T:  # Total number of shares is greater than or equal to number of shares on the market (good)
            bQ = q
            nN = N + bQ  # Re-evaluate the number of shares on the market
            sell(smbl, bQ, P, nN, Q, N, B, nW)  # Sell function
        elif X > T:  # Total number of shares is less than the number of shares on the market (bad)
            print("The number of shares being sold exceeds the quantity of shares currently not on the market.")
    else:
        if uIn == "buy":  # Buying shares
            if P > uB:  # If the cost of the transaction is higher than the user's balance
                print("You cannot afford this transaction!")
            else:
                if X > 0 or X == 0:
                    bQ = (Q - (2 * Q))  # Convert q's value from positive to negative
                    nN = N + bQ  # Re-evaluate the number of shares on the market
                    buy(smbl, bQ, P, nN, Q, N, B, nW)  # Buy function
                else:
                    print("The number of shares being bought exceeds the number of shares available.") #Wh


UID=input("Enter UID: ") #Obtain UID. Do automatically when integrated with Discord API

#On user input
while True:
    uIn=input("Enter command: ").lower() #Command, save as var uIn

    #Check if "Usrs/[UID].json" is a valid filepath
    uPth=Path(f"Usrs\\{UID}.json")
    if uPth.is_file(): #Yes
        uDct=json.load(open(uPth, "r"))
        uB=uDct["bal"]
        print(f"Welcome back {UID}. Your balance is ${uB}.")
    else: #No
        uB=10000
        uDct= {
            "UID": UID,
            "bal": uB
        }
        uDctJ_O=json.dumps(uDct, indent=4)
        with open(uPth, "w") as outfile:
            outfile.write(uDctJ_O)
        print(f"Your profile has now been created. You have ${uB}. Have fun, and spend wisely.")

    #Check that var "uIn" is a valid command
    if uIn== "sell" or uIn == "buy": #Valid command
        print("Command valid")

        q=input("How many shares do you want to transact? ") #Determine "q"
        try:
            q=int(q)#Convert "q" to an integer

            smbl = input("What is the symbol of the company whos shares you want to transact? ")  # Determine "smbl"
            cPth = Path(f"Comps\\{smbl}.json")  # File path to the company with the shares that are being transacted

            # Check that the company with the given symbol exists in the directory
            if cPth.is_file():  # Company exists

                cDct = json.load(open(cPth, "r"))  # Load company JSON dictionary
                t = cDct['sTtl']  # Save total share number of company from dictionary as variable "t"
                n = cDct['sAvl']  # Save number of shares in company on market as variable "n"
                v = cDct['sV']  # Save cost of one share in the company
                w = cDct['val']

                p = v * q  # Determine the total cost of the transaction

                if uIn == "sell":
                    x = n + q  # Determine how many shares in company would hypothetically be on the market after the transaction (selling)
                if uIn == "buy":
                    x = n - q  # Determine how many shares in company would hypothetically be on the market after the transaction (buying)

                parseCmd(x, q, n, t, p, uB, w) #I really need to start coding my bots in a language other than Python

            else:  # Company does not exist
                print("No company with that symbol exists!")

        except ValueError:
            print("Invalid number of shares")

    else:  # Invalid command
        print("Command invalid")
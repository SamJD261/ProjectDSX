import json
import os
from pathlib import Path

type = input("Company or user file? ").lower()
if type=="company" or type=="user":
    print("Command valid")
    if type=="company":
        name=input("Name? ")
        smbl=input("Symbol? ")
        val=input("Net worth? ")
        val=int(val)
        shrNumT=input("Number of shares in total? ")
        shrNumT=int(shrNumT)

        shrVal= val/shrNumT
        pth = Path(f"Comps\\{smbl}.json")

        cDct = {
            "name": name,
            "smbl": smbl,
            "val": val,
            "sV": shrVal,
            "sTtl": shrNumT,
            "sAvl": shrNumT,
        }
        j = json.dumps(cDct, indent=4)
        with open(pth, "w") as outfile:
            outfile.write(j)
    if type=="user":
        UID=input("UID? ")
        bal=input("Balance? ")

        pth=Path(f"Usrs\\{UID}.json")

        uDct = {
            "bal": bal,
            "UID": UID
        }
        j = json.dumps(uDct, indent=4)
        with open(pth, "w") as outfile:
            outfile.write(j)


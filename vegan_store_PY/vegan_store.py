import csv
from veg_store_modules.store import VeganStore
from veg_store_modules.commands_help import help1,help2
commands=["aggiungi","elenca","vendita","profitti","aiuto","chiudi"]
VeganStore.initial_store_check()

promt=""
while promt!="chiudi":
    cost=[]
    sales=[]

    promt=input("Inserisci un comando:")

    if promt not in commands:
      help1()

    elif promt=="aiuto":
      help2()

    elif promt =="aggiungi":
        VeganStore.add_product()

    elif promt=="vendita":
        VeganStore.sell_product()

    elif promt=="elenca":
        VeganStore.show()

    elif promt=="profitti":
        VeganStore.profit_calculator()

else:
    print("bye bye")
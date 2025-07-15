import csv
commands=["aggiungi","elenca","vendita","profitti","aiuto","chiudi"]
columns = ["prodotto","quantità","prezzo di acquisto","prezzo di vendita"]
columns_costs=["prodotto","quantità","prezzo di acquisto", "prezzo di vendita", "costi"]
columns_sales =["prodotto","quantità","fatturato"]

class VeganStore:
    """
    The VeganStore class consists of the following methods:
    - initial_store_check()
    - add_product()
    - sell_product()
    - show()
    - _opencost()
    - _cost_calculator()
    - _opensales()
    - _sales_calculator()
    - profit_calculator()
    - instruction()
    """

    def initial_store_check():
        """
        Verify the existence of the "store.csv" file and, if such a file does not exist, 
        create it in append mode to host the warehouse data.
        """  
        try:
            with open("store.csv", "r") as store_csv:
                store_reader=csv.reader(store_csv)
        except FileNotFoundError:
            with open("store.csv", "a+",newline="") as store_csv:
                store_writer=csv.writer(store_csv)
                store_writer.writerow(columns)    

    def add_product():
        """1. Allows adding products to the warehouse by entering quantities, purchase prices, 
            and selling prices in append mode to the store.csv file created by the initial_store_check() function. Additionally, 
            if a product already present in the warehouse is added, the new quantity is added to the previous one, 
            rewriting the store.csv file with the correct final quantity;

            2. When the add_product() method is initiated, in parallel to adding product references to the store.csv file, a parallel file "cost.csv" is 
            created to track the costs related to the purchase of raw materials for the activities of the vegan market store."""
        try:
            product=(input("Inserisci nuovo prodotto: ")).upper()
            quantity=abs(int(input("Inserisci la quantità: ")))

            with open ("store.csv", "r") as csv_file: 
                reader=csv.DictReader(csv_file)
                reader_list=list(reader)
                list_check=[]
                for entry in reader_list:
                    list_check.append(entry["prodotto"])


                if product not in list_check:
                    purchase_price=abs(float(input("Inserisci prezzo di acquisto: ")))
                    sell_price=abs(float(input("Inserisci il prezzo vendita: ")))

                    with open("store.csv", "a+", newline="") as file:
                        writer=csv.DictWriter(file, fieldnames=columns)
                        writer.writerow({"prodotto":product, "quantità":quantity, "prezzo di acquisto":purchase_price, "prezzo di vendita":sell_price})
                else:
                    with open("store.csv", "w+", newline="") as file:

                        writer=csv.DictWriter(file, fieldnames=columns)
                        writer.writeheader()
                        for entry in reader_list:

                            if product==entry["prodotto"]:
                                entry["quantità"]=int(entry["quantità"])+quantity
                                new_quantity=entry["quantità"]
                                writer.writerow({"prodotto":product, "quantità":new_quantity, "prezzo di acquisto": entry["prezzo di acquisto"], "prezzo di vendita": entry["prezzo di vendita"] })
                                purchase_price=float(entry["prezzo di acquisto"])
                                sell_price=float(entry["prezzo di vendita"])

                            else:
                                writer.writerow(entry)
            print(f"AGGIUNTO {product} X {quantity} in magazzino")

            with open("costs.csv", "a+",newline="") as csv_cost_file:
                costs=int(quantity)*(purchase_price)
                cost_dict=csv.DictWriter(csv_cost_file, fieldnames=columns_costs)
                cost_dict.writerow({"prodotto": product,"quantità":quantity,
                                    "prezzo di acquisto":purchase_price,"prezzo di vendita": sell_price,"costi":costs})
        except ValueError:
                print("Errore di inserimento: il prodotto non è stato aggiunto perché non c'è stato un problema in fase di inserimento dati")
                print("N.B = per inserire in magazzino il prodotto è necessario esplicitare la quantità, prezzo di acquisto, prezzo di vendita utilizzando solamente numeri")
                print("L'operazione di aggiunta è stata interrota, si prega di riprovare!")         
        finally:
            pass    
    
    def sell_product():
        """
        This method allows recording warehouse sales through a text interface that prompts the user to enter the name of the sold product 
        and its quantity. The sale will then be recorded in the "store.csv" file, which keeps track of the updated warehouse balance. 
        If the number of products (per type) sold matches the available warehouse stock, the sell_product() function removes that 
        reference from the warehouse, rewriting the store.csv file without that reference. In parallel, the sell_product() function 
        generates a file (if it does not already exist) called sales.csv, which tracks the revenue from sales.
        """
        try:
            registered_product=[]
            n_product=[]
            product_price=[]
            promt_sold=None
            
            while promt_sold!="":
                sold_product=(input("Nome del prodotto:")).upper() 
                with open("store.csv", "r") as store_csv:
                    store_reader=csv.DictReader(store_csv)
                    store_list=list(store_reader)
                    store_check=[]
                    for entry in store_list:
                        store_check.append(entry["prodotto"])
                        if entry["prodotto"]==sold_product:
                            product_price.append(entry["prezzo di vendita"] )                    
                        else:
                            None
    
                if sold_product not in store_check:
                    print("il prodotto NON è presente in magazzino")
                    break
                    
                else:
                    sold_quantity=int(input("Quantita: "))

                    with open("store.csv", "w+", newline="") as new_csv:
                        new_writer=csv.DictWriter(new_csv, fieldnames=columns)
                        new_writer.writeheader()
                        check=True
                        for dictionary in store_list:
                            if sold_product in dictionary["prodotto"]:
                                if int(sold_quantity) > int(dictionary["quantità"]):
                                    new_writer.writerow(dictionary)
                                    check=False
                                    print("ERRORE! LA QUANTITA' SELEZIONATA SUPERA LA DISPONIBILITA' DI MAGAZZINO. RIPROVARE SELEZIONANDO UNA QUANTITA MINORE O UGUALE ALLA DISPONIBILITA DI MAGAZZINO PER POTER REGISTRARE LA VENDITA NEL MARKET STORE")
                                else:
                                    registered_product.append(sold_product) 
                                    n_product.append(sold_quantity)
                                    dictionary["quantità"]=(int(dictionary["quantità"]))-sold_quantity

                                    if dictionary["quantità"]<=0:                                       
                                        del dictionary
                                        print(f"A seguito dell'ultima vendita hai esaurito tutte le scorte di magazzino!")
                                    else:
                                        print(f"il numero di unità restanti di {dictionary['prodotto']} è: {dictionary['quantità']}")
                                        new_writer.writerow(dictionary)
                            else:
                                new_writer.writerow(dictionary)

                query=input("Aggiungere la vendita di un altro prodotto ? (si/no)")
                
                if query=="si":
                  continue

                else:
                    if check==True:                            
                            print("VENDITA REGISTRATA")
                            registered_sales=list(zip(registered_product,n_product))
                            registered_sales_print=list(zip(registered_sales, product_price))
                            for i in registered_sales_print:
                                print(f"{i[0][1]} X {i[0][0]}: €{i[1]}")
                            with open("sales.csv", "a+",newline="") as csv_sales_file:
                                sales_list=csv.writer(csv_sales_file)
                                sales=None
                                for i in registered_sales_print:
                                    sales=int((i[0][1])) * (float(i[1]))
                                    sales_list.writerow([i[0][0], i[0][1], i[1], sales])                        
                            break
                    else:
                        print("NESSUNA VENDITA REGISTRATA")
                        break

        except ValueError:
                print("Errore di inserimento dati: Non è possibile registrare la vendita")       
        finally:
            pass          

    
    def show():
            """
            This method displays the warehouse availability (read from store.csv), returning as a tabulated result the updated warehouse stock 
            and the corresponding selling price.
            """
            with open("store.csv") as file:
                csv_show=csv.DictReader(file)
                print("PRODOTTO\t",f"{'QUANTITA':>12}\t",f"{'PREZZO':>12}")
                for row in csv_show:
                    print(f"{row['prodotto']:<10}\t\t{row['quantità']}\t\t{row['prezzo di vendita']}")    
    
    def _opencost():
        """
        This method attempts to open the "costs.csv" file. If it finds the file, it returns "True"; otherwise, it returns "False".
        """
        try:
            with open("costs.csv", "r") as csv_reader:
                cost_dict_reader=csv.DictReader(csv_reader, fieldnames=columns_costs)
                cost_list=list(cost_dict_reader)
            return True
        except FileNotFoundError:
            return False

    def _cost_calculator():
        """
        This method opens the "cost.csv" file in read mode, and if the file exists, it calculates the total amount of warehouse expenses. 
        Otherwise, if it encounters a "FileNotFoundError," the function will return 0.
        """
        try:
            total_cost_list=[]
            total_cost_sum=None
            with open("costs.csv", "r") as csv_reader:
                cost_dict_reader=csv.DictReader(csv_reader, fieldnames=columns_costs)
                cost_list=list(cost_dict_reader)
                for i in cost_list:
                    total_cost_list.append(float(i["costi"]))
            total_cost_sum=sum(total_cost_list)
            return total_cost_sum
        except FileNotFoundError:
            return 0

    def _opensales():
            """
            This method attempts to open the "sales.csv" file. If it finds the file, it returns 'True'; otherwise, it returns 'False'.
            """
            try:
                with open("sales.csv","r") as csv_reader:
                    sales_list_reader=csv.reader(csv_reader)
                    sales_list=list(sales_list_reader)
                return True
            except FileNotFoundError:
                return False

    def _sales_calculator():
            """
            The method opens the "sales.csv" file (if it exists) and calculates the total revenue (related to sales).
            Otherwise, if it encounters a FileNotFoundError, it returns 0.
            """
            total_cost_list=[]
            _list_sales=[]
            try:
                with open("sales.csv","r") as csv_reader:
                    sales_list_reader=csv.reader(csv_reader)
                    sales_list=list(sales_list_reader)
                    for i in sales_list:
                        _list_sales.append(float(i[3]))
                total_sales_sum=sum(_list_sales)
                return total_sales_sum
            except FileNotFoundError:
                return 0

    
    def profit_calculator():
            """
            For the correct functioning of the profit_calculator() method, this method utilizes other methods defined by the class 
            and creates internal variables that will be used to calculate the profits of the vegan store, finally calculating 
            the gross profit (total revenue) and net profit (total revenue minus warehouse expenses).It can return different types 
            of informational messages depending on the considered case.
            """
            check_cost=VeganStore._opencost()
            check_sales=VeganStore._opensales()   
            cost_calculation=VeganStore._cost_calculator()
            sales_calculation=VeganStore._sales_calculator()
            net_profit=(sales_calculation)-(cost_calculation)
            if check_cost==True:
                if check_sales==True:
                        print (f"Profitto: lordo=€{round(sales_calculation,2)} netto=€{round(net_profit,2)}")
                else:
                    print(f"Non sono state registrate vendite in passato! \n Il profitto netto è negativo: €{net_profit}")
            else:
                return VeganStore.instruction()

    def instruction():
        """
        This method is automatically called by the profit_calculator() method to display 
        on-screen instructions for effectively using the profit function of the vegan store.
        """
        info= """Nessuna Voce presente in magazzino. 
        Per utilizzare correttamente la funzione calcolo profitti è necessario:
        1. Registrare un nuovo prodotto in magazzino con la funzione aggiungi dal menù principale
        2. Registrare le vendite di tale prodotto in magazzino (nome, quantità venduta)"""
        return print(info)
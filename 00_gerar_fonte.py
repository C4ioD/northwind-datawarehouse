import sqlite3
import pandas as pd
import numpy as np 
import random
import datetime  as dt
import os 

random.seed(42) #defini uma semente aleatória - isso faz com que o código gere os mesmo números aleatórios sempre

np.random.seed(42)  #defini uma semente aleatória - isso faz com que o código gere os mesmo números aleatórios sempre

os.makedirs('data',exist_ok=True) #Cria a pasta "data" caso exista não faz nada

con = sqlite3.connect("data/northwind.db")

# Tabelas de dimensão: categorias, fornecedores, produtos, clientes, funcionarios

categories = pd.DataFrame(
        {
            "CategoryID":range(1,9),
            "CategoryName":["Beverages", "Condiments", "Confections", "Dairy Products",
                     "Grains/Cereals", "Meat/Poultry", "Produce", "Seafood"]
        }
)

suppliers = pd.DataFrame(
    {
        "SupplierID": range(1, 6),
    "CompanyName": ["Exotic Liquids", "New Orleans Cajun", "Grandma Kelly's",
                    "Tokyo Traders", "Cooperativa Quesos"],
    "Country": ["UK", "USA", "USA", "Japan", "Spain"]
    }
)

prod_names = ["Chai", "Chang", "Aniseed Syrup", "Chef Anton's Cajun", "Gumbo Mix",
              "Grandma's Boysenberry", "Uncle Bob's Pears", "Northwoods Cranberry",
              "Mishi Kobe Niku", "Ikura", "Queso Cabrales", "Queso Manchego",
              "Konbu", "Tofu", "Genen Shouyu", "Pavlova", "Alice Mutton",
              "Carnarvon Tigers", "Teatime Biscuits", "Sir Rodney's"]

products = pd.DataFrame({
    "ProductID": range(1, 21),
    "ProductName": prod_names,
    "SupplierID": np.random.randint(1, 6, 20),
    "CategoryID": np.random.randint(1, 9, 20),
    "UnitPrice": np.round(np.random.uniform(5, 80, 20), 2),
    "UnitsInStock": np.random.randint(0, 120, 20),
    "Discontinued": np.random.choice([0, 0, 0, 1], 20)
})

cust_ids = ["ALFKI", "ANATR", "AROUT", "BERGS", "BLAUS",
            "BONAP", "BOTTM", "ERNSH", "FOLKO", "GODOS"]
customers = pd.DataFrame({
    "CustomerID": cust_ids,
    "CompanyName": ["Alfreds", "Ana Trujillo", "Around the Horn", "Berglunds",
                    "Blauer See", "Bon app", "Bottom-Dollar", "Ernst Handel",
                    "Folk Cafe", "Godos Cocina"],
    "Country": ["Germany", "Mexico", "UK", "Sweden", "Germany",
                "France", "Canada", "Austria", "Sweden", "Spain"]
})

employees = pd.DataFrame({
    "EmployeeID": range(1, 6),
    "LastName": ["Davolio", "Fuller", "Leverling", "Peacock", "Buchanan"],
    "FirstName": ["Nancy", "Andrew", "Janet", "Margaret", "Steven"]
})

orders = []
details = []
oid = 10248

for _ in range(200):
    cust = random.choice(cust_ids)
    emp = random.randint(1,5)
    d = dt.date(2023,1,1) + dt.timedelta(days=random.randint(0,540))

    # random.random() gera numero aleatorios de 0.0 a 1.0
    # <0.03  gera ~3% de erro
    #isoformat() transforma a data em uma string format 'AAAA-MM-DD'
    order_date = None if random.random() < 0.03 else d.isoformat() # Operador ternario é só uma forma resumida de escrever if/else

    #ramdom.uniform gera um numero decimal aleatorio entre intervalos
    orders.append((oid, cust, emp, order_date, round(random.uniform(0, 60), 1)))

    for _ in range(random.randint(1,4)):
        pid = random.randint(1,20)
        up =  round(float(products.loc[products.ProductID == pid, "UnitPrice"].iloc[0]),1)
        qty = random.randint(1,40)
        disc = random.choice([0, 0, 0, 0.05, 0.1, 0.15, 0.25])
        #sujeira de ~2%  de quantidades negativas
        if random.random() < 0.02:
            qty = -qty
        details.append((oid,pid,up,qty,disc))
         #sujeira de ~2% de linhas duplicadas
        if  random.random() < 0.02:
            details.append((oid,pid,up,qty,disc))
    oid += 1

orders = pd.DataFrame(orders, columns=["OrderID", "CustomerID", "EmployeeID", "OrderDate", "Freight"])
order_details = pd.DataFrame(details, columns=["OrderID", "ProductID", "UnitPrice", "Quantity", "Discount"])

tables = {

    "categories": categories, "suppliers": suppliers, "products": products,
    "customers": customers, "employees": employees,
    "orders": orders, "order_details": order_details,

}

for name, df  in tables.items():
    df.to_sql(name,con,if_exists="replace", index=False)

con.commit()
con.close()
print("Banco criado em data/northwind.db")
print(f"Pedidos: {len(orders)} | Itens: {len(order_details)}")
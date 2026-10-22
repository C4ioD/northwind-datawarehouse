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
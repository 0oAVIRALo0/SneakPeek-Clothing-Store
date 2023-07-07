import mysql.connector as sql
from prettytable import PrettyTable

connection = sql.connect(host='localhost', user='root', passwd='12345678', database='sneakpeek')

global customer_id

def customer_login(name):
    try:
        cursor = connection.cursor()
        query = "SELECT Customer_ID FROM customers WHERE Customer_Name = %s;"
        cursor.execute(query, (name,))
        global customer_id
        customer_id = cursor.fetchone()[0]
        query = "SELECT * FROM customers WHERE Customer_Name = %s"
        cursor.execute(query, (name,))
        results = cursor.fetchall()
        if results:
            customer_menu()
        else:
            print("Customer with ID {} and name {} does not exist.".format(id, name))
            print()
    except Exception as e:
        print("An error occurred while trying to log in as a customer:", e)

def storeOwner_login(name):
    try:
        cursor = connection.cursor()
        query = "SELECT Owner_ID FROM storeowners WHERE Owner_FirstName = %s;"
        cursor.execute(query, (name,))
        global owner_id
        owner_id = cursor.fetchone()[0]
        query = "SELECT * FROM storeowners WHERE Owner_ID = %s AND Owner_FirstName = %s"
        cursor.execute(query, (owner_id, name))
        results = cursor.fetchall()
        if results:
            storeowner_menu()
        else:
            print("Store owner with ID {} and name {} does not exist.".format(id, name))
            print()
    except Exception as e:
        print("An error occurred while trying to log in as a store owner:", e)

def execute_trigger1():
    try:
        cursor = connection.cursor()
        cursor.execute(" drop trigger if exists contactNumberLength")
        cursor.execute('''CREATE TRIGGER contactNumberLength BEFORE INSERT ON customers FOR EACH ROW BEGIN IF LENGTH(NEW.Customer_ContactNumber) < 10 THEN signal sqlstate '45000' set message_text = 'Invalid contact number'; end if; END''')
        connection.commit()
    except:
        print("Error while generating trigger")
        print()

def execute_trigger2():
    try:
        cursor = connection.cursor()
        cursor.execute(" drop trigger if exists contactNumberLength2")
        cursor.execute('''CREATE TRIGGER contactNumberLength2 BEFORE INSERT ON customers FOR EACH ROW BEGIN IF LENGTH(NEW.Customer_ContactNumber) > 10 THEN signal sqlstate '45000' set message_text = 'Invalid contact number'; end if; END''')
        connection.commit()
    except:
        print("Error while generating trigger")
        print()

def execute_trigger3():
    try:
        cursor = connection.cursor()
        cursor.execute(" drop trigger if exists customerID")
        cursor.execute('''CREATE TRIGGER customerID BEFORE INSERT ON customers FOR EACH ROW BEGIN IF NEW.Customer_ID < 0 THEN signal sqlstate '45000' set message_text = 'Invalid customer id'; end if; END''')
        connection.commit()
    except:
        print("Error while generating trigger")
        print()

def customer_sign_up(name, email, address, contact):
    try:
        execute_trigger1()
        execute_trigger2()
        execute_trigger3()
        cursor = connection.cursor()
        query = "SELECT COALESCE(MAX(Customer_ID), 0) FROM customers;"
        cursor.execute(query)
        customer_id = cursor.fetchone()[0]
        query = "INSERT INTO customers (Customer_ID, Customer_Name, Customer_Email, Customer_Address, Customer_ContactNumber) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(query, (customer_id+1, name, email, address, contact))
        connection.commit()
        print("Successfully signed up!")
        print()
    except Exception as e:
        print("Error inserting customer data into database:", e)


def store_owner_sign_up(first_name, middle_name, last_name, contact):
    try:
        execute_trigger1()
        execute_trigger2()
        execute_trigger3()
        cursor = connection.cursor()
        query = "SELECT COALESCE(MAX(Owner_ID), 0) FROM storeowners;"
        cursor.execute(query)
        owner_id = cursor.fetchone()[0]
        query = "INSERT INTO storeowners (Owner_ID, Owner_FirstName, Owner_MiddleName, Owner_LastName, Owner_ContactNumber) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(query, (owner_id+1, first_name, middle_name, last_name, contact))
        connection.commit()
        print()
        print("Successfully signed up!")
        print()
        return True
    except:
        print("Error occurred while signing up!")
        print()
        return False
    

def mensFootwear():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM products WHERE Category_ID IN (1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13);"
        cursor.execute(query)
        result = cursor.fetchall()

        table = PrettyTable()
        table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]

        for row in result:
            table.add_row(row)

        print(table)

        print()
        print()
        response = input("Do you want to add anything to the cart? (Y/N) ")
        print()
        if response.lower() == "y":
            product_id = int(input("Enter the product ID you want to select from the list of products: "))
            quantity = int(input("Enter quantity: "))
            print()
            print()
            add_to_cart(customer_id ,product_id, quantity)
        else:
            filterChoice = input("Do you want to filter the list of products? (Y/N) ")
            print()
            if filterChoice.lower() == "y":
                while True:
                    print("1. Filter on the basis of Brand \n2. Filter on the basis of size \n3. Filter on the basis of price ranges \n4. Back")
                    print()
                    print()
                    choice = int(input("Enter your choice: "))
                    print()
                    print()

                    filter_table = PrettyTable()
                    filter_table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]

                    if choice == 1:
                        brand_table = PrettyTable()
                        brand_table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]

                        print("1. Air Jordans \n2. Reebok \n3. Nike \n4. Adidas \n5. Back")
                        print()
                        print()
                        c = int(input("Select any of the above options: "))
                        print()
                        if c == 1:
                            query = "SELECT * FROM products WHERE Category_ID = 6;"
                            cursor.execute(query)
                            result = cursor.fetchall()
                            for row in result:
                                brand_table.add_row(row)

                            print(brand_table)
                            print()
                            print()
                            response = input("Do you want to add anything to the cart? (Y/N)")
                            print()
                            if response.lower() == "y":
                                product_id = int(input("Enter the product ID you want to select from the list of products: "))
                                quantity = int(input("Enter quantity: "))
                                print()
                                print()
                                add_to_cart(customer_id, product_id, quantity)

                        elif c == 2:
                            query = "SELECT * FROM products WHERE Category_ID = 7;"
                            filter_choice = 2
                            cursor.execute(query)
                            result = cursor.fetchall()
                            for row in result:
                                brand_table.add_row(row)

                            print(brand_table)
                            print()
                            print()
                            response = input("Do you want to add anything to the cart? (Y/N)")
                            print()
                            if response.lower() == "y":
                                product_id = int(input("Enter the product ID you want to select from the list of products: "))
                                quantity = int(input("Enter quantity: "))
                                print()
                                print()
                                add_to_cart(customer_id, product_id, quantity)
                            
                        elif c == 3:
                            query = "SELECT * FROM products WHERE Category_ID = 8;"
                            filter_choice = 3
                            cursor.execute(query)
                            result = cursor.fetchall()
                            for row in result:
                                brand_table.add_row(row)

                            print(brand_table)
                            print()
                            print()
                            response = input("Do you want to add anything to the cart? (Y/N)")
                            print()
                            if response.lower() == "y":
                                product_id = int(input("Enter the product ID you want to select from the list of products: "))
                                quantity = int(input("Enter quantity: "))
                                print()
                                print()
                                add_to_cart(customer_id, product_id, quantity)

                        elif c == 4:
                            query = "SELECT * FROM products WHERE Category_ID = 9;"
                            filter_choice = 4
                            cursor.execute(query)
                            result = cursor.fetchall()
                            for row in result:
                                brand_table.add_row(row)

                            print(brand_table)
                            print()
                            print()
                            response = input("Do you want to add anything to the cart? (Y/N)")
                            print()
                            if response.lower() == "y":
                                product_id = int(input("Enter the product ID you want to select from the list of products: "))
                                quantity = int(input("Enter quantity: "))
                                print()
                                print()
                                add_to_cart(customer_id, product_id, quantity)
                        
                        else:
                            break
                    
                    elif choice == 2:
                        size = int(input("What is your shoe size: "))
                        print()
                        print()
                        query = "SELECT * FROM products WHERE Product_Size = %s;"
                        cursor.execute(query, (size,))
                        result = cursor.fetchall()
                        for row in result:
                                filter_table.add_row(row)

                        print(filter_table)
                        print()
                        print()
                        response = input("Do you want to add anything to the cart? (Y/N)")
                        print()
                        if response.lower() == "y":
                            product_id = int(input("Enter the product ID you want to select from the list of products: "))
                            quantity = int(input("Enter quantity: "))
                            print()
                            print()
                            add_to_cart(customer_id, product_id, quantity)
                    
                    elif choice == 3:
                        min = int(input("Enter a minimum price: "))
                        max = int(input("Enter a maximum price: "))
                        print()
                        print()
                        query = "SELECT * FROM products WHERE Product_Price BETWEEN %s AND %s;"
                        cursor.execute(query, (min, max))
                        result = cursor.fetchall()
                        for row in result:
                                filter_table.add_row(row)

                        print(filter_table)
                        print()
                        print()
                        response = input("Do you want to add anything to the cart? (Y/N)")
                        print()
                        if response.lower() == "y":
                            product_id = int(input("Enter the product ID you want to select from the list of products: "))
                            quantity = int(input("Enter quantity: "))
                            print()
                            print()
                            add_to_cart(customer_id, product_id, quantity)
                    
                    else:
                        break

    except Exception as e:
        print("An error occurred: ", e)


def womensFootwear():
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM products WHERE Category_ID IN (1, 2, 3, 5, 6, 7, 8, 9, 10, 13);"
        cursor.execute(query)
        result = cursor.fetchall()
        table = PrettyTable()
        table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]

        for row in result:
            table.add_row(row)

        print(table)

        print()
        print()
        response = input("Do you want to add anything to the cart? (Y/N)")
        print()
        if response.lower() == "y":
            product_id = int(input("Enter the product ID you want to select from the list of products: "))
            quantity = int(input("Enter quantity: "))
            print()
            print()
            add_to_cart(customer_id, product_id, quantity)

        while True:
            print("1. Filter on the basis of Brand \n2. Filter on the basis of size \n3. Filter on the basis of price ranges \n4. Back")
            print()
            print()
            choice = int(input("Enter your choice: "))
            print()
            print()

            filter_table = PrettyTable()
            filter_table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]

            if choice == 1:
                brand_table = PrettyTable()
                brand_table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]

                print("1. Air Jordans \n2. Reebok \n3. Nike \n4. Adidas \n5. Heels \n6. Back")
                print()
                print()
                c = int(input("Select any of the above options: "))
                print()
                if c == 1:
                    query = "SELECT * FROM products WHERE Category_ID = 6;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        brand_table.add_row(row)

                    print(brand_table)
                    print()
                    print()
                    response = input("Do you want to add anything to the cart? (Y/N)")
                    print()
                    if response.lower() == "y":
                        product_id = int(input("Enter the product ID you want to select from the list of products: "))
                        quantity = int(input("Enter quantity: "))
                        print()
                        print()
                        add_to_cart(customer_id, product_id, quantity)

                elif c == 2:
                    query = "SELECT * FROM products WHERE Category_ID = 7;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        brand_table.add_row(row)

                    print(brand_table)
                    print()
                    print()
                    response = input("Do you want to add anything to the cart? (Y/N)")
                    print()
                    if response.lower() == "y":
                        product_id = int(input("Enter the product ID you want to select from the list of products: "))
                        quantity = int(input("Enter quantity: "))
                        print()
                        print()
                        add_to_cart(customer_id, product_id, quantity)
                    
                elif c == 3:
                    query = "SELECT * FROM products WHERE Category_ID = 8;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        brand_table.add_row(row)

                    print(brand_table)
                    print()
                    print()
                    response = input("Do you want to add anything to the cart? (Y/N)")
                    print()
                    if response.lower() == "y":
                        product_id = int(input("Enter the product ID you want to select from the list of products: "))
                        quantity = int(input("Enter quantity: "))
                        print()
                        print()
                        add_to_cart(customer_id, product_id, quantity)

                elif c == 4:
                    query = "SELECT * FROM products WHERE Category_ID = 9;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        brand_table.add_row(row)

                    print(brand_table)
                    print()
                    print()
                    response = input("Do you want to add anything to the cart? (Y/N)")
                    print()
                    if response.lower() == "y":
                        product_id = int(input("Enter the product ID you want to select from the list of products: "))
                        quantity = int(input("Enter quantity: "))
                        print()
                        print()
                        add_to_cart(customer_id, product_id, quantity)

                elif c == 5:
                    query = "SELECT * FROM products WHERE Category_ID = 10;"
                    cursor.execute(query)
                    result = cursor.fetchall()
                    for row in result:
                        brand_table.add_row(row)

                    print(brand_table)
                    print()
                    print()
                    response = input("Do you want to add anything to the cart? (Y/N)")
                    print()
                    if response.lower() == "y":
                        product_id = int(input("Enter the product ID you want to select from the list of products: "))
                        quantity = int(input("Enter quantity: "))
                        print()
                        print()
                        add_to_cart(customer_id, product_id, quantity)
                
                else:
                    break
            
            elif choice == 2:
                size = int(input("What is your shoe size: "))
                print()
                print()
                query = "SELECT * FROM products WHERE Product_Size = %s;"
                cursor.execute(query, (size,))
                result = cursor.fetchall()
                for row in result:
                    filter_table.add_row(row)

                print(filter_table)
                print()
                print()
                response = input("Do you want to add anything to the cart? (Y/N)")
                print()
                if response.lower() == "y":
                    product_id = int(input("Enter the product ID you want to select from the list of products: "))
                    quantity = int(input("Enter quantity: "))
                    print()
                    print()
                    add_to_cart(customer_id, product_id, quantity)
            
            elif choice == 3:
                min = int(input("Enter a minimum price: "))
                max = int(input("Enter a maximum price: "))
                print()
                print()
                query = "SELECT * FROM products WHERE Product_Price BETWEEN %s AND %s;"
                cursor.execute(query, (min, max))
                result = cursor.fetchall()
                for row in result:
                    filter_table.add_row(row)

                print(filter_table)
                print()
                print()
                response = input("Do you want to add anything to the cart? (Y/N)")
                print()
                if response.lower() == "y":
                    product_id = int(input("Enter the product ID you want to select from the list of products: "))
                    quantity = int(input("Enter quantity: "))
                    print()
                    print()
                    add_to_cart(customer_id, product_id, quantity)
            
            else:
                break
    
    except Exception as e:
        print("An error occurred: ", e)


def add_to_cart(customer_id, product_id, quantity):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM products WHERE Product_ID = %s;"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        if not product:
            print("Product not found.")
            return

        if product[4] < quantity:
            print("Not enough stock available.")
            return

        price = product[2] * quantity

        # decrease product stock by the quantity being added to cart
        new_stock = product[4] - quantity
        update_query = "UPDATE products SET Product_Stock = %s WHERE Product_ID = %s;"
        cursor.execute(update_query, (new_stock, product_id))

        # add product to cart table
        cart_query = "INSERT INTO carts (Cart_ID, Customer_ID, Product1, TotalPrice) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE TotalPrice = TotalPrice + %s, Product1 = %s;"
        cursor.execute(cart_query, (customer_id, customer_id, product_id, price, price, price))
        connection.commit()

        print("Product added to cart successfully.")
        print()
        print()

    except Exception as e:
        print("An error occurred while adding the product to the cart.")
        print("Error message: ", e)



def showCart(cutomer_id):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM carts WHERE Customer_ID = %s;"
        cursor.execute(query, (customer_id,))
        cart = cursor.fetchone()

        if not cart:
            print("Cart is empty.")
            print()
            return

        # create dictionary of product IDs and quantities
        products = {cart[2]: 1, cart[3]: 1, cart[4]: 1, cart[5]: 1, cart[6]: 1}
        total_price = 0

        for product_id, quantity in products.items():
            if product_id is None:
                continue
            product_query = "SELECT Product_Name, Product_Price FROM products WHERE Product_ID = %s;"
            cursor.execute(product_query, (product_id,))
            product = cursor.fetchone()
            if product:
                product_name = product[0]
                product_price = product[1] * quantity # calculate total price for this product
                total_price += product_price
                print("- " + product_name + " x " + str(quantity) + " : $" + str(product_price))

        print("Total price: $" + str(total_price))
        print()
        print()

        response = input("Do you want to pay for this order? (Y/N)")
        if response.lower() == "y":
            creditcardNumber = int(input("Enter the card number: "))
            cvv = int(input("Enter the card cvv: "))
            print()
            print("Payment processed.")
            delete_query = "DELETE FROM carts WHERE Customer_ID = %s;"
            cursor.execute(delete_query, (customer_id,))
            connection.commit()
            print("Cart deleted.")
            print()
        else:
            print("Order not processed.")
            print()

    except Exception as e:
        print("An error occurred while showing the cart.")
        print("Error message: ", e)


def openStore(owner_id):
    cursor = connection.cursor()
    query1 = "SELECT COALESCE(MAX(Store_ID), 0) FROM stores;"
    cursor.execute(query1)
    storeID = cursor.fetchone()[0]
    storeName = input("Enter the store name: ")
    storeLocation = input("Enter the store location: ")
    storeContactNumber = input("Enter the store contact number: ")
    print()
    query = "INSERT INTO stores (`Store_ID`, `Store_Name`, `Store_Location`, `Store_ContactNumber`, `Owner_ID`) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(query, (storeID+1, storeName, storeLocation, storeContactNumber, owner_id))
    connection.commit()
    table = PrettyTable()
    table.field_names = ["Store ID", "Store Name", "Store Location", "Contact Number", "Owner ID"]
    table.add_row([storeID+1, storeName, storeLocation, storeContactNumber, owner_id])
    print(table)
    print()


def addNewProduct():
    cursor = connection.cursor()
    query1 = "SELECT COALESCE(MAX(Product_ID), 0) FROM products;"
    cursor.execute(query1)
    productID = cursor.fetchone()[0]
    productName = input("Enter the product name: ")
    productPrice = int(input("Enter the product price: "))
    productSize = int(input("Enter the product size: "))
    productStock = int(input("Enter the product stock: "))
    categoryID = int(input("Enter the category ID: "))
    storeID = int(input("Enter the store ID in which you want to store the product: "))
    query = "INSERT INTO products (Product_ID, Product_Name, Product_Price, Product_Size, Product_Stock, Category_ID, Store_ID) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(query, (productID+1, productName, productPrice, productSize, productStock, categoryID, storeID))
    connection.commit()
    table = PrettyTable()
    table.field_names = ["Product_ID", "Product_Name", "Product_Name", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]
    table.add_row(productID+1, productName, productPrice, productSize, productStock, categoryID, storeID)
    print(table)
    print()

def displayProductsSortedByPrice(order):
    cursor = connection.cursor()
    if order == 'asc':
        query = """SELECT * FROM products ORDER BY Product_Price ASC;"""
    elif order == 'desc':
        query = """SELECT * FROM products ORDER BY Product_Price DESC"""
    cursor.execute(query)
    result = cursor.fetchall()
    table = PrettyTable()
    table.field_names = ["Product_ID", "Product_Name", "Product_Price", "Product_Size", "Product_Stock", "Category_ID", "Store_ID"]
    for row in result:
        table.add_row(row)
    print(table)
    print()

def storeowner_menu():
    while True:
        print()
        print("*** WELCOME ***")
        print()
        print("You can choose of the following actions: ")
        print()
        print("1. Add new product \n2. Open more stores \n3. Who are the top 5 customers who placed the most orders and their contact information \n4. What are the total number of orders made by each customer \n5. What is the average price of products in each category \n6. Number of out-of-stock products in each store \n7. Back")
        print()
        try:
            choice = int(input("Enter your choice: "))
            print()
            if choice == 1:
                addNewProduct()

            elif choice == 2:
                openStore(owner_id)
            
            elif choice == 3:
                cursor = connection.cursor()
                query = "SELECT c.Customer_Name, c.Customer_Email, c.Customer_ContactNumber, COUNT(o.Order_ID) AS Total_Orders FROM customers c JOIN carts ct ON c.Customer_ID = ct.Customer_ID JOIN orders o ON ct.Cart_ID = o.Cart_ID GROUP BY c.Customer_ID ORDER BY Total_Orders DESC LIMIT 5;"
                cursor.execute(query)
                result = cursor.fetchall()
                table = PrettyTable()
                table.field_names = ["Customer Name", "Customer Email", "Customer Contact Number", "Total Orders"]
                for row in result:
                    table.add_row(row)
                print(table)
                print()

            elif choice == 4:
                cursor = connection.cursor()
                query = """SELECT c.Customer_Name, COUNT(o.Order_ID) AS Total_Orders
                            FROM customers c
                            JOIN carts ca ON c.Customer_ID = ca.Customer_ID
                            JOIN orders o ON ca.Cart_ID = o.Cart_ID
                            GROUP BY c.Customer_ID;"""
                cursor.execute(query)
                result = cursor.fetchall()
                table = PrettyTable()
                table.field_names = ["Customer Name", "Total Orders"]
                for row in result:
                    table.add_row(row)
                print(table)
                print()

            elif choice == 5:
                cursor = connection.cursor()
                query = """SELECT c.Category_Name, AVG(p.Product_Price) AS Average_Price
                            FROM products p
                            JOIN categories c ON p.Category_ID = c.Category_ID
                            GROUP BY c.Category_ID;"""
                cursor.execute(query)
                result = cursor.fetchall()
                table = PrettyTable()
                table.field_names = ["Category Name", "Average Price"]
                for row in result:
                    table.add_row(row)
                print(table)
                print()

            elif choice == 6:
                cursor = connection.cursor()
                query = """SELECT stores.Store_Name, COUNT(products.Product_ID) AS Out_of_Stock_Count
                            FROM stores
                            INNER JOIN products ON stores.Store_ID = products.Store_ID
                            WHERE products.Product_Stock = 0
                            GROUP BY stores.Store_Name;"""
                cursor.execute(query)
                result = cursor.fetchall()
                table = PrettyTable()
                table.field_names = ["Store Name", "Out of Stock Count"]
                for row in result:
                    table.add_row(row)
                print(table)
                print()

            elif choice == 7:
                break

            else:
                print("Please enter a valid choice.")

        except Exception as e:
            print("Error:", e)
            print("Invalid input. Please enter a valid integer choice.")

def customer_menu():
    while True:
        print()
        print("*** WELCOME ***")
        print()
        print("You can choose of the following actions: ")
        print()
        print("1. Show men's footwear \n2. Show women's footwear \n3. Show Cart \n4. Show all the products where price ranges from low to high \n5. Show all the products where price ranges from high to low \n6. Back")
        print()
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                mensFootwear()
            
            elif choice == 2:
                womensFootwear()
            
            elif choice == 3:
                showCart(customer_id)

            if choice == 4:
                displayProductsSortedByPrice('asc')

            elif choice == 5:
                displayProductsSortedByPrice('desc')

            elif choice == 6:
                break
            
            else:
                print("Please enter a valid choice.")
    
        except ValueError:
            print("Please enter a valid integer choice.")


prev_choice = None

print()
print()
print("*** Welcome to SneakPeak ***")
print()
print()

while True:
    try:
        print("Please Select one of the following options to enter the App:")
        print()
        print("1. Store Owner Sign Up")
        print("2. Store Owner Login")
        print("3. Customer Sign Up")
        print("4. Customer Login")
        print("5. Exit")
        print()
        choice = int(input("Enter your choice: "))
        if choice == 1:
            print()
            print("****************************************************************")
            print()
            first_name = input("Enter owner first name: ")
            middle_name = input("Enter owner middle name (optional): ")
            last_name = input("Enter owner last name: ")
            contact = input("Enter owner contact number: ")
            prev_choice = 1
            store_owner_sign_up(first_name, middle_name, last_name, contact)

        elif choice == 2:
            print()
            print("****************************************************************")
            print()
            storeowner_name = input("Please enter your name: ")
            prev_choice = 2
            storeOwner_login(storeowner_name)

        elif choice == 3:
            print()
            print("****************************************************************")
            print()
            name = input("Please enter your name: ")
            contact = int(input("Please enter your contact number: "))
            address = input("Please enter your address: ")
            email = input("Please enter your email: ")
            print()
            customer_sign_up(name, email, address, contact)
            prev_choice = 3
        
        elif choice == 4:
            print()
            print("****************************************************************")
            print()
            customer_name = input("Please enter your name: ")
            prev_choice = 4
            customer_login(customer_name)

        elif choice == 5:
            break

        else:
            print()
            print("Enter a valid choice")

    except Exception as e:
        print()
        print("An error occurred:", e)
        print("Please try again.")

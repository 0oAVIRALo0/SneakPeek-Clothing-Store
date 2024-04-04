# **SneakPeek Online Shopping System**

SneakPeek is an online shopping system that allows customers to browse and purchase products from various categories. It also provides functionality for store owners to manage their inventory and track sales. The system is built using Python and MySQL database.

## **Features**

- **Customer Sign-up/Login**: Customers can create an account and log in to access their profile and make purchases.
- **Store Owner Sign-up/Login**: Store owners can register their stores and manage inventory, pricing, and sales.
- **Product Browsing**: Users can browse products from different categories and filter products based on brand, size, and price range.
- **Adding to Cart**: Customers can add products to their shopping cart for future purchase.
- **Triggers**: Triggers are implemented to enforce constraints on data integrity, such as validating contact numbers and customer IDs.

## **Components**

### **1. Customer Module**

- **`customer_sign_up(name, email, address, contact)`**: Registers a new customer in the database.
- **`customer_login(name)`**: Allows a registered customer to log in and access their profile and shopping options.
- **`mensFootwear()`**: Displays a list of men's footwear products available for purchase and provides options to filter and add products to the cart.

### **2. Store Owner Module**

- **`store_owner_sign_up(first_name, middle_name, last_name, contact)`**: Registers a new store owner in the database.
- **`storeOwner_login(name)`**: Allows a registered store owner to log in and manage their store inventory and sales.

### **3. Database Triggers**

- **`execute_trigger1()`**, **`execute_trigger2()`**, **`execute_trigger3()`**: Define triggers to enforce constraints on data integrity during customer sign-up.

## **Usage**

1. Ensure you have MySQL installed and running on your system.
2. Create a database named **`sneakpeek`** and import the schema provided.
3. Install required Python libraries: **`mysql-connector`**, **`prettytable`**.
4. Run the **`main.py`** file to start the SneakPeek system.
5. Follow the prompts to sign up/login as a customer or store owner, browse products, and perform actions.

## **Contributions**

Contributions to enhance features, fix bugs, or improve system performance are welcome! Please feel free to submit issues or pull requests.

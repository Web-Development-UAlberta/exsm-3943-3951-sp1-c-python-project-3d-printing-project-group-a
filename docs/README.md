# 3D Printing Online Store - Project Setup & Usage Guide (Python)
The 3D Printing Online Store functions through Python. This README gives Users everything they need to install, configure, and run the project locally.

## **Overview**
3D Printing Online Store is a Python-based platform for ordering custom 3D prints. It includes:
- Product catalog for models and materials
- Customizing 3D model attributes and print options
- File upload system for .3TL and .3MF models
- Automated pricing engine
- Order management dashboard
- Admin panel for managing printers and inventory
- User accounts and authentication

## **Tech Stack**
|Layer|Technology|Purpose|
|--|--|--|
|Repository|GitHub|Proect Management, Version Control|
|Frontend|Next.js 16.2.4|Storefront, Admin UI|
|Frontend|HTML5|Storefront, UI Design|
|Frontend|Tailwind CSS|Storefront, Styling|
|Backend|Python 3.10|Backend, Functions|
|Database|MariaDB|Inventory Management|
|Testing|Python Unittest|Backend Testing|
|Testing|Jest|Frontend Testing|
|Testing|React Testing Library|Storefront, Admin UI|

## **Features**
### **Customer-Facing**
* Browse product catalog
* Product filtering and sorting
* Custom model upload
* Configure preference and design
* Automated quote estimates
* Checkout and order tracking
* User accounts and saved orders

### **Admin-Facing**
* CRUD operations
* Print queue management
* Order dashboard
* Inventory management

### **Backend Services**
* Payment integration (Stripe)

## **Project Structure**
```
Main/
│
├── docs/                   # Directory for project documentation 
│   ├── erd/                # Directory for backend blueprints
│   └── wireframes/         # Directory for frontend blueprints
│
├── node_modules/           # Directory for Node.js external libraries and dependencies
│
├── printshop-frontend/     # Directory for frontend code
│   ├── __tests__/          # Directory for frontend tests
│   ├── app/                # Next.js pages
│   ├── jest.config.js      # Jest configuration
│   ├── jest.setup.js       # Jest setup file
│   └── package.json        # Frontend dependencies
│
├── src/
│   ├── app/                # Directory for backend code
│   ├── model_files/        # Directory for storing model files
│   ├── model_image/        # Directory for storing model images
│   ├── routes /            # Directory for storing backend HTTP layer and JSON
│   ├── services /          # Directory for storing backend functions
│   ├── alembic/            # Directory for Alembic dependencies
│   ├── databases/          # Directory for database code
│   ├── run.py              # File to run backend service
│   └── seed.py             # Seed data for database
│
└── tests/                  # Directory for backend tests
```

## **Local Development Setup**

### **1. Install Python**
* Download the latest installer from [python.org](https://www.python.org/downloads/)
* Run the installer (64-bit recommended)
* **Important:** Select the checkbox that says "Add Python to PATH" at the bottom of the installer
* Run the following command in Terminal to check installation succession
```
python --version
```

### **2. Install MariaDb**
* Download the latest installer from [mariadb.org](https://mariadb.org/download/)
* Run the installer
* Configure a strong root password when prompted
* Run the following command in Terminal to check installation succession
```
mariadb --version
```

### **3. Clone the repository**
* In a local directory, open the folder in VS Code (preferred choice of IDE)
* Open a new Terminal
* Use the following command to clone the repository:
```
git clone https://github.com/Web-Development-UAlberta/exsm-3943-3951-sp1-c-python-project-3d-printing-project-group-a.git
```

### **4. Create a virtual environment**
* In VS Code code, press "Ctrl+Shift+P"
* Select "Python: Create Environment"
* Select "venv"
```
git clone https://github.com/Web-Development-UAlberta/exsm-3943-3951-sp1-c-python-project-3d-printing-project-group-a.git
```

### **5. Setup Frontend dependencies**
The frontend will be using Next.js 16.2.4, Jest, and React Testing Library.
* Download the latest installer from [nodejs.org](https://nodejs.org/en/download)
* Run the installer
* Run the following command in Terminal to check installation succession
```
node --version
```
* Run the following command in Terminal to change directories
```
cd printshop-frontend
```
* Run the following commands in Terminal to install all dependencies
```
npm install
```

### **6. Setup Backend dependencies**
* Run the following command in Terminal
```
pip install sqlalchemy
```
* Run the following command in Terminal
```
pip install mysqlclient
```

### **7. Run database migrations**
* Run the following command in MariaDB to create a database
```
CREATE DATABASE 3d_printing_project
```
* Run the following command in Terminal to copy env.example template
```
cp .env.example .env
```
* Open the ".env" file from main directory
* Update the following lines with your MariaDB Password
```
DB_URL=mysql+mysqldb://root:YOUR_DB_PASSWORD@localhost:3306/3d_printing_project
```
* Save the file
* Run the following commands in Terminal to install dependencies:
```
cd src
pip install -r requirements.txt
```
* Run the following commands in Terminal to run database migration
```
alembic upgrade head
```

### **8. Start the development server**
* Run the following command in Terminal to run a development server
```
npm run dev
```
* In an internet browser, go to the following URL
```
http://localhost:3000
```

### **9. Database Preparations**
* Open the following file "src/seed.py"
* In each table, replace placeholder data with real data
* Run the following command in Terminal to push data into database
```
alembic upgrade head
```

### **10. Payments**
Stripe is integrated for 
* Checkout sessions
* Payment handling

To test locally, use the following command:
```
stripe listen --forward-to localhost:8000/api/payments/webhook/
```

### **11. Create a superuser**
* Run the following command in MariaDB
```
USE 3d_printing_project
```
* Update the below values tagged as [YOUR_]. Run the following commands once database is selected
```
INSERT INTO Users(
    username, full_name, 
    phone_number, city, 
    street_address, province, 
    postal_code, is_admin)
VALUES('YOUR_USERNAME','YOUR_FULL_NAME', 'YOUR_PHONENUMBER, 'YOUR_CITY', 'YOUR_STREET_ADDRESS', 'YOUR_PROVINCE', 'YOUR_POSTALCODE', TRUE);
COMMIT;
```


## **Usage Guide**

### **1. Table Management**

#### **Table Stucture:**

  |Table|Description|
  |-|-|
  |Model|Stores inventory for product catalog|
  |Filament|Stores inventory for filament|
  |Tag|Stores model classification|
  |Model Filament|Links model with usable filaments|
  |Model Tag|Links model with tag classification|
  |Order Detail|Product configuration for selected model|
  |Order Header|Cart view of selected products|
  |Printer|Links printers with filament, printer type. Captures printer queue|
  |Printer Type|Stores inventory for printers|
  |Users|Stores database of user profiles|

#### **Model Setup**

* Add 3D files and images
    * Store model files in `src/app/model_files`. Files should have file extension of .stl or .3mf.
    * Store preview images of 3D models in `src/app/model_images`. Files should be an image format.

* Custom 3d files and image
    * Uploaded model files are stored in `src/app/model_files`. The filename will contain order_id.
    * Default preview custom image is stored at `src/app/model_images/custom_print.png`.

### **2. Frontend Usage**
* Base Layout: `app/page.tsx`
    * Renders header, navigation, footer, and product catalog.
* Product Page: `app/products/[id]/page.tsx`
    * Renders model attributes and information.
* Custom Model Page: `app/custom/page.tsx`
    * Renders custom product configuration for custom models.
* Order Page: `app/orders/page.tsx`
    * Renders product selections, and quote calculations.
* Cart Page: `app/cart/page.tsx`
    * Renders product configuration for model selection.
* Checkout Page: `app/checkout/page.tsx`
    * Renders checkout page for payment and shipping details.
* Profile Page: `app/profile/page.tsx`
    * Renders profile page of logged in user.
* Profile Edit Page: `app/profile/edit/page.tsx`
    * Renders profile page for modifications.
* Login Page: `app/login/page.tsx`
    * Renders login screen for existing users.
* Register Page: `app/register/page.tsx`
    * Renders registration screen for new users.
* Admin Page: `app/admin/page.tsx`
    * Renders admin dashboard for printer, orders, and filament management.

### **3. User Routes**

* **Home / Product Catalog:**
  
  GET: `/models` 
  
  Description: Displays models, categories, and materials.

* **Product Detail:**
  
  GET: `/models<int:model_id>` 
  
  Description: Displays the selected model info.

* **Product Detail:**
  
  POST: `/quote` 
  
  Description: Displays the real-time calculation of model selection and configuration.

* **Custom Product Upload:**
  
  POST: `/upload` 
  
  Description: Triggers file uploads to directory.

* **Custom Model Product:**
  
  POST: `/upload_model` 
  
  Description: Triggers a new model record to be stored in database.

* **Order Page:**
  
  GET: `/orders` 
  
  Description: Displays the Cart page

* **View Order:**
  
  GET: `/orders/<int:order_id>` 
  
  Description: Displays the current Cart selections.

* **Order Deletion:**
  
  PUT: `/orders/<int:order_id>/cancel`
  
  Description: Allows user to cancel the order.

* **Add To Cart:**
  
  POST: `/cart`
  
  Description: Retrieves cart item selected.

* **Delete Cart Item:**
  
  DELETE: `/cart<int:order_detail_id>`
  
  Description: Deletes the cart item from order. 

* **Delete Cart:**
  
  DELETE: `/cart`
  
  Description: Empties the cart. 

* **Payment Details:**
  
  POST: `/checkout/create-intent`
  
  Description: Navigates user to payment details. 

* **Confirm Checkout:**
  
  POST: `/checkout/confirm`
  
  Description: Processes order payment and order confirmation. 

* **Payment Confirmation:**
  
  POST: `/checkout/webhook`
  
  Description: Updates order status based on payment status.

* **User Login:**
  
  POST: `/auth/login`
  
  Description: Navigation to login to a profile.

* **User Register:**
  
  POST: `/auth/register`
  
  Description: Navigation to register a profile.

* **User Profile:**
  
  GET: `/users/me`
  
  Description: Displays the current profile of logged in user.

* **Update User Profile:**
  
  PUT: `/users/me`
  
  Description: Modifications for specific user profile.

* **Update User Password:**
  
  PUT: `/users/me/password`
  
  Description: Modifications for specific user password.

### **4. Admin Routes**

* **Admin Dashboard:**
  
  GET: `/dashboard` 
  
  Description: A dashboard for managing filaments, printers, orders, models, and users.

* **Filament Management:**
  
  GET: `/filaments` 
  
  Description: Filament management for stock inventory.

* **Delete Filament:**
  
  DELETE: `/filaments` 
  
  Description: Removes filament from stock inventory.

* **Filament Modification:**
  
  PUT: `/filaments/<int:filament_id>` 
  
  Description: Modifications for specific filament selection.
    
* **Printer Queue Management:**
  
  GET: `/printers`  
  
  Description: Printer management for printing queue.

* **Delete Printer:**
  
  DELETE: `/printers`  
  
  Description: Removes printers from printing queue.

* **Printer Queue Modification:**
  
  PUT: `/printers/<int:printer_id>`
  
  Description: Modifications for specific printer selection.

* **Printer Type Modification:**
  
  POST: `/printer-types` 
  
  Description: Add additional printers to inventory.

* **Delete Printer Types:**
  
  DELETE: `/printer-types` 
  
  Description: Delete printers from inventory.
    
* **Order Management:**
  
  GET: `/orders`
  
  Description: Order management for user orders.

* **Order Modifications:**
  
  PUT: `/orders<int:order_id>` 
  
  Description: Modifications for specific order selection.
    
* **Model Management:**
  
  GET: `/models`
  
  Description: Model management for product models.

* **Delete Model:**
  
  DELETE: `/models/<int:model_id>`  
  
  Description: Delete specific model from catalog.

* **Model Modifications:**
  
  POST: `/models/<int:model_id>`  
  
  Description: Modifications for specific model selection.

* **User Management:**
  
  GET: `/users`
  
  Description: User management for customer profiles.

* **Delete User:**
  
  DELETE: `/users/<int:user_id>`  
  
  Description: Deletes specific user from system.

* **User Modifications:**
  
  PUT: `/users/<int:user_id>`  
  
  Description: Modifications for specific user selection.

* **Admin Users:**
  
  PUT: `/users/<int:user_id>/make-admin`  
  
  Description: Modifications to make a user an admin.

### **5. Environment Variables**
Environment variables are user-defined values meant to be stored privately at system level or locally. Programs will be able to reference the secret keys that are hidden from public view. `.env`

|Secret Variable|Key|Description|
|-|-|-|
|Database|DB_URL|Private string to connect app to MariaDB|
|JWT|JWT_SECRET|Private string used by server to sign and verify tokens|
|Stripe|STRIPE_SECRET_KEY|Private token used to authenticate Stripe API|
|Flask|FLASK_ENV|Specifies the mode to run Flask (development vs production)|
|Custom Model Files|CUSTOM_UPLOAD|Directory to store custom model files|
|Model Images|MODEL_IMAGES|Directory to store model preview images|

### **6. Running Tests**
#### **Frontend Automated Tests (Next.js)**
* For automated frontend testing, run the following command in Terminal
```
npm ci
npm install --save-dev jest jest-environment-jsdom @testing-library/react @testing-library/jest-dom @testing-library/dom
npm test
```


#### **Backend Automated Tests (Unittest)**
* For automated backend testing, run the following command in Terminal
```
python -m unittest discover
```
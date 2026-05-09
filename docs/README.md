# 3D Printing Online Store - Project Setup & Startup Guide (Python)
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
|Backend|Python 3.14|Backend, Functions|
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
│   ├── __tests__/          # Directory for backend tests
│   ├── app/                # Next.js pages
│   ├── jest.config.js      # Jest configuration
│   ├── jest.setup.js       # Jest setup file
│   └── package.json        # Frontend dependencies
├── src/
│   ├── alembic/            # Directory for Alembic dependencies
│   │   └── versions/       # Directory for database seed data
│   └── databases/          # Directory for database code
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
* Run the following command in Terminal to install all dependencies
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
* Run the following command in MariaDB
```
CREATE DATABASE 3d_printing_project
```
* In the "src" directory, open "models.py" file
* Update the following line
```
mysql+mysqldb://{your root}:{your password}@localhost:3306/3d_printing_project'
```
* Run the following commands in Terminal
```
pip install alembic
alembic init alembic
```
* In the "src" directory, open "alembic.ini" file
* Change the following line
```
sqlalchemy.url = mysql+mysqldb://{yor root}:{your password}@localhost:3306/3d_printing_project
```
* Run the following commands in Terminal
```
alembic revision --autogenerate -m"Initial migration
alembic upgrade head
```

### **8. Create a superuser**
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

### **9. Start the development server**
* Run the following command in Terminal to run a development server
```
npm run dev
```
* In an internet browser, go to the following URL
```
http://localhost:3000
```

### **10. Database Preparations**
Run the following command in Terminal
```
alembic revision -m "seed_data"
```
* Open the **src/alembic/versions/seed.py** file
* Copy contents in the file into seed_data file
* Modify the contents of seed_data file to include database data
* Run the following command in Terminal
```
alembic upgrade head
```

### **11. Payments**
Stripe is integrated for 
* Checkout sessions
* Payment handling

To test locally, use the following command:
```
stripe listen --forward-to localhost:8000/api/payments/webhook/
```

## **Running Tests**
### **Frontend Automated Tests (Unittest)**
* For automated frontend testing, run the following command in Terminal
```
python -m unittest discover
```
* You should see all 15 tests passing

### **Backend Automated Tests (Next.js)**
* For automated backend testing, run the following command in Terminal
```
npm test
```
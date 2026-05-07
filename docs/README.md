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
- Next.js 16.2.4 (frontend framework)
- Python 3.14 (backend framework)
- HTML (web framework)
- Tailwind CSS (frontend styling)
- MariaDB (primary database)
- GitHub (code repository)
- Python Unittest (backend testing framework)
- Jest (frontend testing framework)
- React Testing Library (frontend testing framework)

## **Project Structure**
```
Main/
│
├── docs/                   # Directory for project documentation 
│   ├── erd/                # Directory for backend blueprints
│   └── wireframes/         # Directory for  frontend blueprints
│
├── node_modules/           # Directory for Node.js external libraries and dependencies
│
├── printshop-frontend/     # Directory for frontend code
│   ├── __tests__/           # Directory for backend tests
│   ├── app/                     -- Next.js pages
│   ├── jest.config.js           -- Jest configuration
│   ├── jest.setup.js            -- Jest setup file
│   └── package.json             -- Frontend dependencies
├── src/
│   ├── alembic/            # Directory for Alembic dependencies
│   │   └── versions/       # Directory for database seed data
│   └── databases/          # Directory for database code
│
└── tests/                  # Directory for backend tests
```

## **Local Development Setup**

#### **1. Install Python**
* Download the latest installer from [python.org](https://www.python.org/downloads/)
* Run the installer (64-bit recommended)
* **Important:** Select the checkbox that says "Add Python to PATH" at the bottom of the installer
* Run the following command in Terminal to check installation succession
```
python --version
```

#### **2. Install MariaDb**
* Download the latest installer from [mariadb.org](https://mariadb.org/download/)
* Run the installer
* Configure a strong root password when prompted
* Run the following command in Terminal to check installation succession
```
mariadb --version
```

#### **3. Clone the repository**
* In a local directory, open the folder in VS Code (preferred choice of IDE)
* Open a new Terminal
* Use the following command to clone the repository:
```
git clone https://github.com/Web-Development-UAlberta/exsm-3943-3951-sp1-c-python-project-3d-printing-project-group-a.git
```

#### **4. Create a virtual environment**
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

### **7. Run database migrations** [PENDING]
* Run the following commands in Terminal
```
pip install alembic
alembic init alembic
```
* In the "alembic" directory, open the "env.py" file
* Update the following line with MariaDB password
```
url = config.get_main_option("mysql+mysqldb://root:yourpassword@localhost:3306/yourfoldername")
```

### **8. Create a superuser** [PENDING]
Create a superuser using the following method:

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
#### **Frontend Automated Tests**
* For automated frontend testing, run the following command in Terminal
```
python -m unittest discover
```
* You should see all 15 tests passing

#### **Backend Automated Tests**
* For automated backend testing, run the following command in Terminal
```
npm test
```
* You should see all 11 tests passing:

```
PASS __tests__/home.test.jsx
PASS __tests__/login.test.jsx
PASS __tests__/register.test.jsx
PASS __tests__/custom-upload.test.jsx
PASS __tests__/configurator.test.jsx
PASS __tests__/cart.test.jsx
PASS __tests__/checkout.test.jsx
PASS __tests__/order-tracking.test.jsx
PASS __tests__/profile.test.jsx
PASS __tests__/edit-profile.test.jsx
PASS __tests__/admin.test.jsx

Tests: 11 passed
```
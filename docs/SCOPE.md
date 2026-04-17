# Scope Document: 3D Printing Online Store
### **1. Goals & Objectives**
- The objective is to create a system that can be interacted by the Business and Customer. Both frontend and backend will allow seamless execution of activities and tracking throughout the system ecosystem.

### **2. Requirements**
- A database to host 3D Models
- Ability for Customer to access 3D Models from database
- Ability to select preferences (colour, material, 3D model)
- Ability for System to generate a quote
- Ability to calculate turnaround times based on materials in stock
- Ability to calculate turnaround times based on ordering time
- Ability to expedite orders
- A database to host User Accounts
- Ability for Customer to create a profile
- Ability to update profile, preference, payment info, track orders
- A database to host store inventory
- Ability to track stock inventory, quantity
- Ability for System to process payments

### **3. Scope Description**
- Database to store 3D Models
- Database for User Management
- Database to track stock inventory
- User Interface for Customer
- User Interface for Business
- Functionality for Customer order selection
- Functionality for Customer payment transaction
- Functionality for Customer profile creation/modification
- Functionality for Customer quotation
- Functionality for Business order tracking
- Functionality for Business stock tracking

### **4. Exclusions**
- Ability for Customer to create their own 3D Models
- Ability for Customer to use Digital Wallets, Paypal payment methods

### **5. Constraints**
- TBD

### **6. Assumptions**
- Customer Quote will add an automatic default of “n” hours for low stock transactions where “n” is defined by Business
- Customers will not be able to design their own 3D Models. They must select from database
- No restrictions to Customer placing orders while “Low stock” and “No inventory”

### **7. Project Deliverables**
- Week 1: Scope draft, design draft
- Week 2: ERD Mapping draft, wireframes draft, test plans
- Week 3: Finalize ERD, wireframes, test plans
- Week 4: Database creation
- Week 5: Frontend and backend creation
- Week 6: Final Product
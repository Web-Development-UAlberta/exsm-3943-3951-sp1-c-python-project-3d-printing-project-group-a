# Scope Document: 3D Printing Online Store

### **1. Project Overview**
**Application Name:** 3D Printing Online Store

**Development Team:** Johnny Kwan, Robel Measho, Rami Ayesh

**Purpose:** Allow Customers to select/customize/design their own 3D objects for print, automate the quotating process to calculate costs of print/delivery, enable a payment system for order fulfillment, manage User accounts to store Customer information, and build an inventory management for Business to track assets.

### **2. Scope Deliverables & Objectives**
- Responsive frontend to allow efficiency on User navigation and system interaction
- Simplified product selection and customization for better usability
- Real-time calculations for cost and delivery
- Maintainable storage and security of User account details
- Inventory tracking for resupply and stock management
- Automated order payment to decrease manual processing

### **3. High-Level Business Requirements**

| Impacted Area | Business Needs |
| -------- | -------- |
| **Customers (Frontend User)** | - A registration/login page for the User profile creation/login (Account Management)
| |- A selection page to access/select/update 3D models (Asset Management)
| |- A customization page to design/customize selected 3D model (Product Management)
| |- A configuration page to configure printing preferences (Material, Colour, Quantity)
| |- A cart page to calculate price of product based on design/material (Quote)
| |- A cart page to expedite orders for additional costs
| |- A cart page to calculate shipping costs (Quote)
| |- A cart page to calculate turnaround times based on product, material, 
| |- A checkout page to accept payment for order fulfillment (Payment System)
| |- A tracking page to view the progress of their orders |
| **Business (Backend User)** | - An admin page to manage User profiles (Account Management)
| |- A dashboard to review orders for processing (Order Management)
| |- An order page to update order status (Order Management)
| |- A tracker page to for stock inventory (Asset Management) |
| **System (Application)** | - A table to store general 3D models
| |- A table to store 3D models uploaded by User
| |- A table to manage Business assets/inventory
| |- Notifications for low inventory based on threshold amounts (Asset Management)
| |- Automated processing of online payments |
| |

### **4. Core Features**
#### **A. Frontend Features**
- Design Editor: An interface to configure and customize order selections
- Quotation: Real-time quotes with instant calculations and pricing
- Account Management: Control and maintain profile settings and preferences

#### **B. Backend Features**
- Asset Management: Simple visibility and control over stock and inventory
- Notifications: Automation of system alerts for depleting assets
- Payment Management: 

### **5. Exclusions/Out of Scope**
[No Exclusions captured]

### **6. Scope Assumptions, Constraints, and Risks**

| Impacted Area | Assumption |
| -------- | -------- |
| Payment Management |  Payment methods will be delivered as a proof of concept. Online payments will be simulated with no real-time payments triggers
| |

| Impacted Area | Constraints |
| -------- | -------- |
| Time-Constraints |  The deliverables of the project will focus on essential business needs required for a functional system. Additional non-essential requirements may be placed in backlog due to project time-constraints. The Business will determine which requirements are essential and non-essential
| |

| Impacted Area | Risks |
| -------- | -------- |
| TBD |  No Risks Captured
| |

### **7. Project Deliverables**
- Week 1: Scope draft, design draft
- Week 2: ERD Mapping draft, wireframes draft, test plans draft
- Week 3: Finalize ERD, wireframes, test plans
- Week 4: Database creation
- Week 5: Frontend and backend creation
- Week 6: Final Product
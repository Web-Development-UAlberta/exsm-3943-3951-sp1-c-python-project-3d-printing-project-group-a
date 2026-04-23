# Scope Document — 3D Printing E-Commerce Platform

## Table of Contents

1. [Project Overview](#project-overview)
2. [Team Members](#team-members)
3. [In-Scope Features](#in-scope-features)
4. [Out-of-Scope Features](#out-of-scope-features)
5. [Pending Client Clarification](#pending-client-clarification)
6. [Constraints](#constraints)
7. [Risks](#risks)

---

## Project Overview

A web-based e-commerce platform for a 3D printing business. Customers can browse a library of 3D models, enter their desired dimensions, choose a filament material and color, and receive an automated live price quote. The system manages filament inventory, calculates turnaround times based on stock levels, and processes orders through a cart and checkout flow. Customers can track orders, cancel pending orders, and leave seller reviews. An admin dashboard allows the store owner to manage inventory via CSV upload and update order statuses.

---

## Team Members

| Name         | Role                         |
| ------------ | ---------------------------- |
| Robel Measho | Frontend Developer (Next.js) |
| Rami Ayesh   | Backend Developer (Python)   |
| Johnny Kwan  | Backend / Lead               |

---

## In-Scope Features

### User Accounts

- Customer registration and login with JWT authentication
- Customer profile page showing account details and order history
- Edit profile information
- Cancel pending orders from profile page

### Product Browsing & Configuration

- Browse library of available 3D models with previews
- Filter models by material and color
- Enter custom dimensions (length, width, height in mm) per order
- Select filament material and color
- Toggle multi-color print option
- Upload a reference image or file (any file type) on home page and configurator
- Option to pay an expedited service fee for faster turnaround

### Live Quoting & Pricing

- Quote updates automatically as customer changes dimensions, material, and color
- Price calculated based on material cost, color/filament cost, machine wear and tear, and extra fee
- Turnaround time calculated based on filament stock levels
- Lead time added automatically if selected material or color is out of stock
- Estimated completion date and shipping date displayed to customer

### Cart

- Add products to cart from configurator
- View all cart items with model name, material, color, and quantity
- Adjust quantity per item with stepper (+/-)
- Remove individual items from cart
- Cancel entire cart
- View running subtotal and total price
- Proceed to checkout from cart

### Order Management

- Checkout with pseudo payment processing (always approved)
- Cancel checkout and return to cart
- Order statuses: Pending, Printing, Shipped, Completed
- Cancel order only when status is Pending — cannot cancel once Printing starts
- View full order history with status badges
- View individual order details including all order items and sub-totals
- Filament stock automatically decrements when order is placed

### Seller Reviews

- Customers can leave a review on completed orders only
- Star rating (1-5) and written comment
- Reviews displayed on customer profile page with overall rating summary
- Rating breakdown bars showing distribution of reviews
- Customer can delete their own reviews

### Inventory Management

- Admin uploads Color inventory via CSV file
- Admin uploads Material inventory via CSV file
- System tracks stock levels per color and material
- Stock bars show visual low-stock warnings in admin dashboard
- Low stock flagged for admin attention

### Admin Dashboard

- Stat cards showing active orders, low stock count, and total orders
- Upload and manage Color CSV and Material CSV files
- View all orders with ability to update status
- Admin can cancel any order regardless of status

---

## Out-of-Scope Features

- Physical 3D printer hardware integration
- Real-time print job monitoring
- Mobile app — web only
- Multi-language support
- Customer support chat or ticketing system
- Marketing features such as promotions, discount codes, or email campaigns
- Shipping carrier API integration — shipping dates are estimated not live
- Real 3D model file parsing for automatic dimension extraction

---

## Pending Client Clarification

The following items are not yet confirmed and will be updated once the client responds on Slack:

- **Payment processing** — pseudo always-approved confirmed in spec but awaiting final client confirmation
- **Customer model uploads** — admin-only CSV uploads currently in scope, customer self-uploads TBD
- **Turnaround time formula** — exact calculation logic (hours per mm3, per material) to be confirmed
- **Expedited fee amount** — exact dollar amount or percentage to be confirmed
- **Machine wear and tear cost** — cost per material per hour to be confirmed or estimated
- **Lead time values** — number of days per material/color when out of stock to be confirmed
- **Must-haves vs nice-to-haves** — final priority list to be confirmed with client

---

## Constraints

- Project must be completed within 6 weeks
- Tech stack: Next.js (frontend), Python (backend), GitHub for version control
- Branch protection: pull requests to main require 2 approvals, direct commits to main are blocked
- All tests must pass before final submission

---

## Risks

| Risk                                            | Likelihood | Impact | Mitigation                                                            |
| ----------------------------------------------- | ---------- | ------ | --------------------------------------------------------------------- |
| Turnaround time formula not confirmed by client | Medium     | High   | Follow up on Slack immediately, use placeholder logic until confirmed |
| Dimension-based pricing logic is complex        | Medium     | High   | Backend team to define and document formula early                     |
| CSV format inconsistencies from client          | Medium     | Medium | Define expected CSV column format in design doc                       |
| Frontend and backend integration issues         | Medium     | High   | API contract agreed in design doc before any coding begins            |
| Scope creep from client requests                | Medium     | Medium | Refer all new requests back to this scope document                    |
| Team member falling behind                      | Low        | High   | Soft deadlines in team norms, ask for help early                      |
| Cart and order state management complexity      | Medium     | Medium | Agree on state management approach in Week 2 design review            |

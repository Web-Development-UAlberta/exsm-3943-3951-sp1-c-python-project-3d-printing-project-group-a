# Test Plan: 3D Printing Online Store
### **1. Document Information**

|||
|-----------|-----------|
|Prepared by: |Johnny Kwan, Robel Measho, Rami Ayesh|
|Version:| V1.0   |
|Status: |  Draft |

### **2. Introduction**

This document defines the strategy and execution of test plan activities. The purpose is to ensure the application is functional and usable by Users upon Production go-live. The test plans serve as the primary reference for the client's confidence in quality assurance.

Test plans will cover strategies for frontend and backend activities.

### **3. Scope**
#### 3.1 In Scope
- Account Management: User registration, login accessibility, preferences, order tracking, review tracking, and profile management
- Product Catalog: Product sorting, product filtering, browsing library, item pricing, model preview, product detailing, and user selection
- Custom Products: File uploads, model preview, storage, product customization, and cart order
- Standard Products: Model preview, model selection, product configuration, and cart order
- Quotation: Real-time calculations, selection preview, shipping estimates, and status tracking
- Cart: Order tracking, quantity management, product configuration, and checkout
- Checkout: Order summary, real-time calculations, payment preferences, and order placement
- Order Tracking: Order history, fulfillment status, shipment estimates, customer details, and order details
- Admin Dashboard: Analytics dashboard, order tracking, inventory tracking, user management, and product management
- Notifications: Client emails, and Admin notifications
- Page Design: Responsiveness, W3C compliance, and browser compatibility
- Security: Authentication, authorization, and data encryption

#### 3.2 Out of Scope
- Payment Method: Real-time payment methods to banking networks
- Model Upload: Non-image filetype based

### **4. Objectives**
- Validate functional requirements against scope document
- User navigation is responsive and interactive
- Images and links are active and functional
- File uploads are processed and loaded
- Model previews demonstrate product results
- Products provide preference selections and drive costs
- Live quote generating real-time calculations
- Shipping costs and delivery estimates are accurate
- Order creations are successful
- Cart controls quantity and User actions
- Submission of Cart for checkout is successful
- Registration produces secured profile creation
- Login enables data encryption and authorization
- Payment methods allow User input
- Order summarization is accurate against order
- Tracking displays order status and progress
- Customer profiles can be viewed and modified
- Seller reviews is visible in customer profile
- Order tracking is visible in customer profile
- Reviews can be written by purchasing customer
- Admin dashboard to track active orders and low inventory stock
- Visibility to an overview of filament stock levels
- Track and update order status

### **5. Test Strategy**
|Testing Type|Description|Tools/Approach|
|-----------|-----------|-----------|
|Functional Testing|Validate all features and user workflows against requirements and functional interactions. Cover positive and negative scenarios. | Manual |
|Unit Testing|Validate code base coverage meets acceptable thresholds performed by system automation.|Python unittest|
|Performance Testing|Validate load/stress for system and database responsiveness.| Manual |
|Security Testing|Validate penetration and vulnerability of user storage.| Manual |
|Accessibility Testing|Validate compliance of accessibility and SEO.| Manual |
|User Acceptance Testing|End-User testing by the Client and stakeholders for real-life scenarios| Manual 

### **6. Functional Test Scenarios**
The following test scenarios will be broken up into modules. Each category will contain functional test scenarios specific to the module.

#### 6.1 User Management

|ID|Test Scenario|Expected|Type|
|-|-|-|-|
UM-001|Register with a unique Username | Account created successfully, redirect back to login page|Positive
UM-002|Register with an existing Username | Account not created, error message appears|Negative
UM-003|Register with a unique Email Address | Account created successfully, redirect to login page|Positive
UM-004|Register with an existing Email Address | Account not created, error message appears|Negative|Negative
UM-005|Register with a Password at least 12 alphanumeric characters | Account created successfully, redirect to login page|Positive
UM-006|Register with a Password 11 alphanumeric characters or less | Account not created, error message appears|Negative|Negative
UM-007|Login with existing Username and Password | User logged into Account, redirect back to previous page|Positive
UM-008|Login with non-existent Username and Password | User not logged in, error message appears|Negative

#### 6.2 Page Navigation
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
PN-001|Navigate to the Home hyperlink | Page redirects to the Home page|Positive
PN-002|Navigate to the Models hyperlink | Page redirects to the Models page|Positive
PN-003|Navigate to the Cart hyperlink | Page redirects to the Cart page|Positive
PN-004|Navigate to the Orders hyperlink | Page redirects to the Orders page|Positive
PN-005|Navigate to the Profile hyperlink | Page redirects to the Profile page|Positive
PN-006|Navigate to the Logout hyperlink | User logged out of account, redirect to login page|Positive
PN-007|Navigate to non-existent page in URL | Browser error for page not found|Negative

#### 6.3 Product Catalog
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
PT-001|Filter products by Material | Model library displays models based on Materials filter|Positive
PT-002|Filter products by Material | Unselected Material not rendered|Negative
PT-003|Filter products by Color | Model library displays models based on Color filter |Positive
PT-004|Filter products by Color | Unselected Color not rendered|Negative
PT-005|View product Images | Images are active and rendered|Positive
PT-006|View product Details | Product Name and Pricing are rendered|Positive
PT-007|Upload supported Files | File upload modal accepts upload, image stored in product table|Positive
PT-008|Upload unsupported Files | File upload modal rejects upload, error message appears|Negative

#### 6.4 Product Configuration
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
PF-001|View selected model | Preview image of model renders|Positive
PF-002|Enter integers for model Dimensions | Integer input for Length, Width, and Height of model allowed|Positive
PF-003|Enter letters for model Dimensions| Letter input for Length, Width, and Height of model disallowed > error message appears|Negative
PF-004|Select model Material | Selection of Material is persistent, additional cost added to quote if applicable|Positive
PF-005|Select model Color | Selection of Color is persistent, additional cost added to quote if applicable|Positive
PF-006|Select Multi-color print | Selection of Multi-color print is persistent, additional cost added to quote if applicable|Positive
PF-007|Expedite an order | Selection of expedite is persistent, additional cost added to quote if applicable|Positive

#### 6.5 Product Quotation
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
PQ-001|Select Dimensions of the model | Dimensions drive quote calculations| Positive
PQ-002|Select Material of the model | Material drive quote calculations| Positive
PQ-003|Select Color of the model | Color drive quote calculations| Positive
PQ-004|Select Multi-color option for print | Multi-colors drive quote calculations| Positive
PQ-005|Select Expedite of the order | Expedite option drive quote calculations| Positive
PQ-006|View quote Subtotal | Subtotal will be calculated based on selected attributes| Positive
PQ-007|View Completion date | Completion date will be calculated based on order attributes and stock availability| Positive
PQ-008|View Shipping date | Shipping date will be calculated based on order attributes and stock availability| Positive
PQ-009|View order Status | Default status before submission will be Pending status| Positive

#### 6.6 Order Cart
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
OC-001|View selected Products | Cart will render selected products with model image and attributes| Positive
OC-002|Change order quantity | Selected product quantity can be modified, subtotal recalculated based on quantity| Positive
OC-003|Remove selected Products | Selected product will be removed, subtotal recalculated based on Products left in Cart| Positive
OC-004|Cancel the Cart | All items in the Cart will be removed, cleared items cannot be undone| Positive
OC-005|Keep shopping | Redirects user back to the Product catalog, selected products are persistent| Positive
OC-006|Proceed to Checkout | Redirects user to checkout page| Positive

#### 6.7 Checkout
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
CO-001|Enter integers for payment Card number| Integer input for Card number is allowed | Positive
CO-002|Enter letters for payment Card number| Letter input for Card number is disallowed | Negative
CO-003|Enter integers for payment Expiry date| Integer input for Expiry date is allowed | Positive
CO-004|Enter letters for payment Expiry| Letter input for Expiry date is disallowed | Negative
CO-005|Enter integers for payment CVV| Integer input for CVV is allowed | Positive
CO-006|Enter letters for payment CVV| Letter input for CVV is disallowed | Negative
CO-007|Enter letters for payment Name on card| Letter input for Name on card is allowed | Positive
CO-008|Enter integers for payment Name on card| Integer input for Name on card is disallowed | Negative
CO-009|Place order with payment details| Payment processed, redirect to order tracking page| Positive
CO-010|Place order without payment details| Payment not processed, error message appears| Negative
C0-011|View Order summary|Breakdown of order attributes and pricing renders|Positive

#### 6.8 Order Tracking
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
|OT-001|View Order Id against order status|Status reflects current order status|Positive|
|OT-002|View Order Id against order total|Total reflects current order total|Positive|
|OT-003|View Order Id against order ship date|Ship Date reflects estimated ship date|Positive|
|OT-004|Cancel an Order in Pending Status|Cancel button available, order cancelled, order id removed from order tracking|Positive|
|OT-005|Cancel an Order past Pending Status|Cancel button no avilable, order not cancelled, order id remains in order tracking|Negative|
|OT-006|Select Order Id to view Order Info|Order Info is displayed|Positive|

#### 6.9 Customer Profile
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
|CP-001|View User Profile view|Profile details displayed, Edit Profile button available|Positive|
|CP-002|View Recent Orders grid|Past orders displayed under Recent Orders|Positive|

#### 6.10 Admin Dashboard
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
|AD-001|View Active Order counter|Counter rolls up all orders not in Completed status|Positive|
|AD-002|View Low Stock counter|Counter rolls up filaments in low stock, filament reached refill thresholds|Positive|
|AD-003|View Total Orders counter|Counter rolls up orders submitted, all order statuses included|Positive|
|AD-004|View Revenue totals|Calcuation based on total orders against production costs and product customization|Positive|
|AD-005|Update Filament stock|User enters in new filament amounts|Positive|
|AD-006|View filament stock levels|Dashboard renders stock levels, filament measured in grams, low stock highlighted|Positive|
|AD-007|View Active orders|Displays Orders submitted not in Completed status.|Positive|

### **7. Non-Functional Test Scenarios**
The following test scenarios will be broken up into modules. Each category will contain non-functional test scenarios specific to the module.

#### 7.1 Performance
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
|NP-001|Navigate product catalog|Acceptable response for product rendering|Positive|
|NP-002|Filter product catalog|Acceptable response for product filtering action|Positive|
|NP-003|Select a product|Acceptable response for product selection action|Positive|
|NP-004|Upload a custom product|Acceptable response for model upload to backend storage|Positive|
|NP-005|Real-time quote estimates|Instant response for quote calculations, preferences drive different costs|Positive|
|NP-006|Add to cart|Acceptable response to add product to cart table|Positive|
|NP-007|View cart|Acceptable response to display selected products|Positive|
|NP-008|Make a Payment|Acceptable response to payment servers, return payment response|Positive|

#### 7.2 Compatibility
|ID|Test Scenario|Expected|Type|
|-|-|-|-|
|NC-001|Browser Compatibility|Application viewable through different browser types|Positive|
|NC-002|Mobile Compatibility|Application viewable through mobile devices|Positive|

### **8. User Flow Test Cases**
The following end-to-end User flows will validate complete order process flow across multiple modules. Each flow will simulate a realistic user journey within the application.

#### Flow 1: New Customer - Browse and Order Products
**Objective:** Validate purchase experience for a New Customer

1. Visit the 3D Printing Online Store homepage
2. Browse the model library and select a non-custom Product
3. Apply dimensions, material, and color to the model
4. Verify the quote summary and click "Add to Cart"
5. Adjust the quantity of the selected Product
6. Click "Proceed to Checkout"
7. Fill in Customer details and click "Create Account" to register an account
8. Once redirected to Cart page, click "Proceed to Checkout"
9. Verify the order summary totals are the same as quote summary
10. Enter payment details and click "Place Order"
11. Verify order status is "Pending" from the Order Tracking page

#### Flow 2: Existing Customer - Browse and Order Products
**Objective:** Validate purchase experience for an Existing Customer

1. Visit the 3D Printing Online Store homepage
2. Browse the model library and select a non-custom Product
3. Apply dimensions, material, and color to the model
4. Verify the quote summary and click "Add to Cart"
5. Adjust the quantity of the selected Product
6. Click "Proceed to Checkout"
7. Enter existing Username/Password and click "Sign In"
8. Once redirected to order summary page, verify order summary totals match quote summary
9. Enter payment details and click "Place Order"
10. Verify order status is "Pending" from the Order Tracking page

### **9. Test Data**
Test data will be used to simulate a proof-of-concept.

|Data Category|Sample Values|Purpose|
|-|-|-|
|User Account|johnny_k / Pass@1234!!0|Login, Profile, Order Tracking|
|Credit Card|1111-2222-3333-4444 / 01/30 / 123 / Johnny Kay|Payment Processing|
|3D Model File|custom_product.png|File Upload|
|||

### **10. Acceptance Criteria**
#### Functional
- All critical user scenarios complete without errors
- Model file upload supports .PNG up to 100MB
- Instant quote renders 100% accuracy based on Product configuration
- Payment processing complete without errors

#### Non-Functional
- Page loads under 2 seconds during normal load
- Model file upload completes under 10 seconds for 100MB and less
- Payment processing completes under 10 seconds after validation
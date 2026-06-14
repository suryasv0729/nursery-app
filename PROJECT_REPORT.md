# TECHNICAL PROJECT REPORT: GreenHaven Nursery E-Commerce Platform

## 1. ABSTRACT
GreenHaven Nursery is a full-stack, responsive web application tailored for the digital sale of flora, ranging from indoor succulents to outdoor landscaping plants. Designed with a priority on rapid UI/UX interactions, robust backend security, and extensive administrative capability, the platform integrates modern web development methodologies, database pooling, real-time SMTP, artificial intelligence assistance (rule-based NLP), and third-party payment processing.

## 2. TECHNOLOGY STACK
The application utilizes a decoupled, API-driven architecture. 
### 2.1 Backend Layer
* **Language & Framework:** Python 3.10+, Flask (Microframework)
* **Architecture:** Modular Blueprint (MVC-inspired routing architecture)
* **Authentication:** PyJWT (JSON Web Tokens) stateless authentication, Werkzeug security (Password Hashing via Scrypt)
* **Payment Processing:** Razorpay API SDK

### 2.2 Database Layer
* **Engine:** MySQL (Relational Database Management System)
* **Driver:** PyMySQL 
* **Connection Management:** Utility-based connection pooling (context-managed cursors).
* **Environment Configuration:** `python-dotenv` for secure environment variable injection.

### 2.3 Frontend Layer
* **Markup:** HTML5 (Jinja2 Template Engine compatible)
* **Styling Framework:** Tailwind CSS (via edge CDN for rapid utility-first styling) & FontAwesome Icons.
* **Interactivity:** Vanilla JavaScript (`main.js`), Async/Await paradigm for REST API interactions (Fetch API).

### 2.4 External Services
* **SMTP (Simple Mail Transfer Protocol):** `smtplib` routed via Gmail's application infrastructure.
* **CDN Services:** TailwindCSS CDN, Razorpay Checkout JS.

---

## 3. SYSTEM ARCHITECTURE & DATABASE SCHEMA
The application is structured using Flask Blueprints to isolate controllers and routers, maintaining a clean codebase. 

### 3.1 Conceptual Workflow (MVC)
- **Model:** Represents database interactions located within `utils/db.py` and direct cursor executions within the `controllers/` folder.
- **View:** Consists of `.html` files in the `templates/` directory served via Jinja2. These views are dynamic but primarily serve as a shell for JS manipulation.
- **Controller:** Located in `routes/` (intercepts HTTP request) and hands payload to `controllers/` (business logic).

### 3.2 Relational Database Schema (`schema.sql`)
1. **users:** 
   - `id`, `name`, `email` (UNIQUE), `password_hash`, `role` (ENUM: 'user', 'admin'), `created_at`
2. **products:** 
   - `id`, `name`, `description`, `price`, `category`, `stock`, `image_url`
3. **cart & wishlist:**
   - Bridge tables linking `user_id` and `product_id`. Cart includes `quantity`.
4. **orders & order_items:**
   - Centralizes transactional data. `orders` ties to Razorpay order IDs and `status` (pending, paid, shipped). `order_items` freezes the price at the time of purchase.
5. **messages & reviews:**
   - Stores user-generated text content tied to specific plants or administrative inboxes.

---

## 4. CORE MODULES & FUNCTIONALITY

### 4.1 Authentication & Security (`auth_controller.py`)
- **Stateless JWT:** Upon successful login and Scrypt password verification, the server generates a cryptographically signed JWT. This token is stored in the client's `localStorage` and passed sequentially as a `Bearer` token in the `Authorization` header for all subsequent API requests.
- **Role-Based Access Control (RBAC):** Custom python decorators (`@authorize()`) intercept incoming API requests, decode the JWT, extract the `role`, and reject access with `401 Unauthorized` or `403 Forbidden` if criteria aren't met.

### 4.2 E-Commerce Engine (`product_controller.py` & `cart_controller.py`)
- Products are exposed via public GET API routes.
- The shopping cart manipulates the relational bridge table. When an item is added, the server executes an `UPSERT` (Insert or Update on duplicate key) against the user's cart registry. Total costs are derived dynamically on the frontend via JS `data.reduce`.

### 4.3 Financial Transactions (`order_controller.py`)
- **Payment Lifecycle:** 
  1. The user requests checkout. The backend calculates total cart value and pings Razorpay server-to-server to create an official "Razorpay Order ID".
  2. The frontend spawns the Razorpay JS interceptor modal.
  3. Upon a user's successful card/net banking execution, Razorpay fires a payment signature token.
  4. The frontend routes this token back to the backend `/verify` node, bridging the items from `cart` to `orders`, and clears the active cart.
- **Mock Mode / Failsafe:** The code is architected to detect missing API keys and intelligently revert to "Simulation Mode" to prevent deployment crashes.

### 4.4 Real-Time SMTP Module (`mail.py`)
- During password resets, successful payments, or incoming customer inquiries, the backend builds a `MIMEMultipart` data string and hooks securely over `STARTTLS` port 587 to broadcast an automated electronic mail delivery. 
- Integrated a dual-funnel strategy for the `contact` module, providing the customer an auto-response whilst instantaneously copying the text and routing it to the internal administrative inbox.

### 4.5 PlantBot AI Algorithm
- Operates locally inside `main.js`. 
- Utilizing rule-based Natural Language Processing with basic regex substring identification (`\b(sick|water|light)\b`).
- Triggers asynchronous visual `typing` animations using standard `setTimeout` chaining to simulate a live customer support representative for basic botanical queries.

### 4.6 Administrative Domain (CRM)
- A highly shielded analytical sub-application.
- Javascript detects admin roles during authentication, rerouting them from standard shopping endpoints into `admin/dashboard.html`.
- Allows complex CRUD operations directly converting frontend Form payloads into SQL `UPDATE` and `DELETE` queries, dynamically manipulating live product listings, stock statuses, or purging irrelevant users. 

---

## 5. STANDARD USER WORKFLOW (JOURNEY)
1. **Acquisition:** Visitor lands on identical layout template cleanly routed via Flask.
2. **Engagement:** User browses infinite product list, triggers hovering interactive animations without needing an account.
3. **Conversion / Signup:** User clicks "Wishlist" -> Blocked by Auth middleware. A sleek white Material Design modal appears prompting registration via Fetch API interception.
4. **Checkout Phase:** User builds cart, enters checkout. JS fetches Razorpay keys from backend payload, executes real-world payment, redirecting user to an interactive "Successful Invoice" page capable of generating standalone PDFs (`window.print` formatting overrides).
5. **Post-Purchase:** Customer receives order confirmation SMTP email. Admin receives updated revenue analytics on the heavily guarded dashboard portal. 

---

## 6. PROJECT SETUP & EXECUTION

### 6.1 Prerequisites
Ensure that you have Python 3.10+ and a local instance of MySQL installed and running on your machine.

### 6.2 Interpreting the Dependencies (`requirements.txt`)
Each library included in the project fulfills a specific architectural requirement:
* **`Flask`**: The core micro web-framework. It acts as the backbone of our backend API, handling routing, middleware, and rendering Jinja2 HTML templates.
* **`PyMySQL`**: The Python MySQL database connection driver, allowing our backend controllers to execute dynamic SQL commands securely against the database.
* **`python-dotenv`**: A core security utility. It prevents hardcoded secrets by securely loading sensitive environment variables (API keys, DB passwords, SMTP keys) from a hidden `.env` file into the OS scope.
* **`PyJWT`**: Facilitates the stateless creation, signing, and verification of JSON Web Tokens (JWT) used to authenticate users and admins across the platform securely.
* **`Werkzeug`**: Specifically leveraged for its battle-tested security hashing utilities (e.g., `generate_password_hash` & `check_password_hash`), which securely salts and hashes user passwords using the `scrypt` algorithm.
* **`razorpay`**: The official Python SDK for securely transacting and verifying e-commerce financial payloads with Razorpay servers.
* **`cryptography`**: A foundational security library essential for allowing `PyMySQL` to authenticate with modern MySQL databases utilizing the `caching_sha2_password` protocol.

### 6.3 Step-by-Step Commands to Run Locally
1. **Open the Terminal**: Navigate into your project directory footprint (`nursery_app`).
2. **(Optional) Setup Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies**: Command Python's package manager to build the stack.
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Secrets (.env)**: Ensure a `.env` file exists at the root. Fill in the required parameters such as `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, and your SMTP configurations.
5. **Database Initialization**: Assuming your MySQL server is spun up locally, run the seeder script to automatically build tables and inject beautiful default plant arrays:
   ```bash
   python init_db.py
   ```
6. **Launch the Application**:
   ```bash
   python app.py
   ```
7. **View in Browser**: Open your internet browser and navigate to `http://127.0.0.1:5000/`. The frontend GUI will instantly populate.

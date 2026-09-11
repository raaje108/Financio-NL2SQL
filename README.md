# Financio - Smart Business Ledger & NLP Query System

Financio is a business management and ledger system equipped with a local Natural Language Processing (NLP) engine. It enables shop owners and managers to track inventory, record transactions, monitor customer balances, and execute natural-language database queries seamlessly.

---

## 📁 Project Structure

```
nlp_sql/
├── docs/                                  # Project Architecture & Documentation Assets
│   ├── ER.drawio.xml                      # Entity-Relationship (ER) Diagram
│   ├── hydra.drawio.png                   # System Architecture Diagram
│   ├── graph.png                          # Performance & Data Analytics Graphs
│   └── Market_Basket_Analysis_Report.pdf  # Market Basket Analysis Technical Report
├── financio/
│   ├── backend/                           # Node.js Express API & Python NLP Microservice
│   │   ├── src/
│   │   │   ├── app.js                     # Express application configuration & middleware
│   │   │   ├── index.js                   # Server entrypoint (spawns Python NLP process)
│   │   │   ├── controllers/               # Route controllers (user, shop, ledger)
│   │   │   ├── db/                        # MySQL database connection pool (mysql2)
│   │   │   ├── middlewares/               # JWT authentication middleware
│   │   │   ├── nlp/                       # Python NLP Intent & SQL Microservice
│   │   │   │   ├── nlp_server.py          # Naive Bayes Classifier & SQL Query Engine
│   │   │   │   └── run_classifier_tests.py# Test suite for NLP classifier & entity extraction
│   │   │   └── routes/                    # API routes (users, shops, ledger, nlp)
│   │   ├── .env.example                   # Environment configuration template
│   │   └── package.json                   # Node.js dependencies and scripts
│   └── frontend/                          # Client Web Interfaces (HTML / CSS / JS)
│       ├── landingpage/                   # Homepage & marketing landing page
│       ├── login/                         # User login portal
│       ├── signup/                        # Registration portal
│       ├── main/                          # Main dashboard & ledger interface
│       ├── profile/                       # User profile management & avatars
│       ├── about/                         # Information & feature guide
│       └── contact/                       # Contact & feedback form
├── .gitignore                             # Git ignore rules
└── README.md                              # Project documentation
```

---

## 🚀 Key Features

- **Natural Language Database Interface**: Perform complex ledger queries and insert transactions using natural sentence phrasing.
- **Privacy-First & Zero-Cost**: The NLP engine runs 100% locally in Python using a Naive Bayes classifier without any external cloud API calls.
- **Automated Process Lifecycle**: Node.js automatically spawns and manages the Python NLP server process on startup (`src/index.js`).
- **Complete Business Operations**:
  - **Ledger Tracking**: Outstanding balances, payment records, and credit management per shop.
  - **Stock & Inventory Management**: Product catalog, stock levels, and automated low-stock warnings.
  - **Business Insights**: Automatic month-over-month revenue analysis, top sellers, and debtor reports.

---

## 🤖 Supported Natural Language Intents

| Intent | Example Utterance | Action Executed |
| :--- | :--- | :--- |
| **`ADD_TRANSACTION`** | *"add a sale of 5 notebooks at 20 each to ramesh"* | Inserts sale/purchase record into `shop_inventory`. |
| **`QUERY_SALES`** | *"show me sales for this week"* | Summarizes total revenue, units sold, and top movers. |
| **`QUERY_STOCK`** | *"what items are low on stock"* | Fetches inventory counts and product stock levels. |
| **`QUERY_LEDGER`** | *"how much does ramesh owe me"* | Retrieves total outstanding dues and payment history. |
| **`GET_INSIGHTS`** | *"give me insights on my business"* | Analyzes revenue growth, top movers, and debtors. |

---

## ⚙️ Setup & Installation

### Prerequisites
- **Node.js**: v18+
- **Python**: v3.10+ (with `pymysql` installed: `pip install pymysql`)
- **MySQL Database**: Running instance with the `ledger` database schema created.

### 1. Database Configuration
Ensure MySQL is running locally and set up the `ledger` database. The Python NLP server and Node.js backend share the following schema structure:
- `users(id, full_name, email, password)`
- `shops(shop_id, user_id, shop_name, shop_owner)`
- `shop_inventory(item_id, shop_id, product_name, quantity, price, total_amount, amount_paid, amount_rem, payment_method, entry_date)`

### 2. Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd financio/backend
   ```
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Update `.env` with your local database credentials and desired port:
   ```env
   PORT=8000
   DB_HOST=127.0.0.1
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=ledger
   JWT_SECRET=your_jwt_secret
   ```

### 3. Running the Application
Start the backend development server (this automatically spawns the Python NLP engine on port `5005`):
```bash
npm run dev
```

### 4. Running NLP Classifier Tests
To verify intent classification and entity extraction independently:
```bash
cd financio/backend/src/nlp
python run_classifier_tests.py
```

---

## 📖 Documentation & Diagrams

Architecture and design diagrams are located in the [`docs/`](docs/) directory:
- 📊 **[ER Diagram](docs/ER.drawio.xml)**: Database relationships and schema definitions.
- 🏗️ **[System Architecture](docs/hydra.drawio.png)**: High-level overview of Express, Python NLP, and MySQL interactions.
- 📈 **[Market Basket Report](docs/Market_Basket_Analysis_Report.pdf)**: Data analysis and market basket report.

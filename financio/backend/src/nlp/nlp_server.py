import os
import sys
import json
import re
import math
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import pymysql

# --- Load Environment Variables ---
def load_env():
    env_vars = {
        "DB_HOST": "127.0.0.1",
        "DB_USER": "root",
        "DB_PASSWORD": "",
        "DB_NAME": "ledger"
    }
    # Path to .env file relative to this script: backend/.env
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))
    if os.path.exists(env_path):
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, val = line.split('=', 1)
                        env_vars[key.strip()] = val.strip()
        except Exception as e:
            print(f"[NLP Server] Error reading .env: {e}", file=sys.stderr)
    return env_vars

ENV = load_env()

# --- Database Connection Helper ---
def get_db_connection():
    return pymysql.connect(
        host=ENV.get("DB_HOST", "127.0.0.1"),
        user=ENV.get("DB_USER", "root"),
        password=ENV.get("DB_PASSWORD", ""),
        database=ENV.get("DB_NAME", "ledger"),
        cursorclass=pymysql.cursors.DictCursor
    )

# --- Naive Bayes Intent Classifier ---
class NaiveBayesClassifier:
    def __init__(self):
        self.class_counts = {}
        self.word_counts = {}
        self.vocab = set()
        self.total_docs = 0

    def tokenize(self, text):
        # Convert to lowercase and find words
        return re.findall(r'\b[a-z0-9]+\b', text.lower())

    def train(self, training_data):
        self.class_counts = {}
        self.word_counts = {}
        self.vocab = set()
        self.total_docs = 0

        for intent, phrases in training_data.items():
            self.class_counts[intent] = 0
            self.word_counts[intent] = {}
            for phrase in phrases:
                self.total_docs += 1
                self.class_counts[intent] += 1
                tokens = self.tokenize(phrase)
                for word in tokens:
                    self.word_counts[intent][word] = self.word_counts[intent].get(word, 0) + 1
                    self.vocab.add(word)
        print(f"[NLP Server] Intent classifier trained on {len(training_data)} intents with {self.total_docs} utterances.")

    def classify(self, text):
        tokens = self.tokenize(text)
        if not tokens or self.total_docs == 0:
            return "UNKNOWN", 0.0

        scores = {}
        vocab_size = len(self.vocab)

        for intent, count in self.class_counts.items():
            # Prior probability
            prior = count / self.total_docs
            log_prob = math.log(prior)

            # Total words in this class
            total_words_in_intent = sum(self.word_counts[intent].values())

            for word in tokens:
                word_count = self.word_counts[intent].get(word, 0)
                # Laplace smoothing
                word_prob = (word_count + 1) / (total_words_in_intent + vocab_size)
                log_prob += math.log(word_prob)

            scores[intent] = log_prob

        # Softmax normalize scores for relative confidence
        max_score = max(scores.values())
        exp_scores = {intent: math.exp(score - max_score) for intent, score in scores.items()}
        total_exp = sum(exp_scores.values())
        normalized_scores = {intent: val / total_exp for intent, val in exp_scores.items()}

        sorted_scores = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)
        top_intent, confidence = sorted_scores[0]

        if confidence < 0.4:
            return "UNKNOWN", confidence
        return top_intent, confidence

# --- Training Data ---
TRAINING_DATA = {
    "ADD_TRANSACTION": [
        "add a sale of 5 notebooks at 20 each to ramesh",
        "record sale 3 pens to suresh for 15 rupees each",
        "log a purchase of 10 units of rice at 40 per unit",
        "add new entry sold 2 chairs to priya",
        "create a transaction for 7 bags of cement to the site",
        "i sold 4 bottles of oil to kumar today",
        "add expense of 500 for shop electricity bill",
        "record a payment received of 2000 from ramesh",
        "log purchase 20 kg sugar from supplier at 45 rs",
        "payment of 1500 received from suresh",
        "refund issued of 400 to kumar",
        "record refund of 250 to priya",
        "sold 10 packets of chips for 15 rupees each to ram",
        "purchased 50 items of light bulbs at 30 each from supplier",
        "add a cash payment of 1200 from rahul electronics",
        "registered payment of 500 from sai kirana",
        "spent 300 on transport tea snacks expense",
        "gave a refund of 150 to sharma shop",
        "logged sale 12 boxes of pens to nikhil at 100 rs per box",
        "record purchase of 5 tons of bricks for 15000",
        "add transaction 15 shirts sold at 400 rupees to amit",
        "log new payment of 4500 received from ganesh",
        "record expense of 3000 for rent this month"
    ],
    "QUERY_SALES": [
        "what were my top selling items last month",
        "show me sales for this week",
        "how much did i sell yesterday",
        "what is my total revenue this month",
        "give me sales report for last 7 days",
        "how many units of rice were sold this month",
        "what did ramesh buy last time",
        "show total sales for today",
        "which item sold the most last week",
        "list my transactions for today",
        "how much sales revenue did we make last quarter",
        "show me the sales breakdown for yesterday",
        "what is the total value of sales this week",
        "list all sales entries of cement this month",
        "what was sold to suresh yesterday",
        "find all sales records between monday and wednesday",
        "how many transactions did we have today",
        "show the revenue summary for the last 30 days",
        "what is my best selling product this week",
        "display sales log for last month",
        "how much did i earn from sales yesterday",
        "give me the sales history for sai kirana"
    ],
    "QUERY_STOCK": [
        "what items are low on stock",
        "how much rice is left in stock",
        "show me current inventory",
        "which products are out of stock",
        "check stock level for sugar",
        "do we have enough cement in stock",
        "list items below reorder level",
        "show product quantities",
        "how many notebooks do we have left",
        "what is the stock status of pens",
        "list all products with zero stock",
        "display the inventory levels for all items",
        "do we need to reorder any stock",
        "check stock for books",
        "how much quantity is left for oil bottles",
        "list items in stock",
        "show stock levels of electronics",
        "check inventory count",
        "are we running out of sugar",
        "how many bags of cement are available",
        "what is the quantity of shirts left",
        "inventory levels report"
    ],
    "QUERY_LEDGER": [
        "how much does ramesh owe me",
        "show ledger for suresh",
        "what is the outstanding balance for priya",
        "show all pending payments",
        "who owes me money",
        "show transaction history for kumar",
        "give me outstanding statement",
        "how much balance is pending for amit",
        "who has not paid their due yet",
        "what is the ledger balance for sai kirana store",
        "show outstanding dues for all shops",
        "how much credit is given to rahul electronics",
        "list all unpaid transactions",
        "does suresh owe any money",
        "outstanding statement for ganesh",
        "who owes the highest amount",
        "show credit history for priya",
        "how much cash balance is remaining from kumar",
        "ledger details for ram",
        "find outstanding balance for sharma shop",
        "is there any due balance from nikhil",
        "give me the ledger summary for all customers"
    ],
    "GET_INSIGHTS": [
        "give me insights on my business",
        "summarize my shop performance",
        "how is my business doing this month",
        "give me a summary of sales and stock",
        "show me trends for this month",
        "analyze my revenue growth",
        "what insights do you have for me",
        "give me business performance analysis",
        "how is my shop doing compared to last month",
        "summarize my revenue and outstanding balance",
        "what are the key highlights of my business this week",
        "give me a general report on how my shop is performing",
        "analyze my sales and debt trends",
        "is my business profitable this month",
        "give me a summary of my business growth",
        "tell me how my shops are performing overall",
        "what insights can you give about my debtors",
        "show my business summary report",
        "analyze trends in sales and inventory",
        "how has my revenue changed compared to last week",
        "business health check report",
        "summarize overall sales performance"
    ],
    "UNKNOWN": [
        "hello",
        "hi there",
        "hey assistant",
        "good morning",
        "good evening",
        "how are you today",
        "yo",
        "what's up",
        "who are you",
        "what is the meaning of life",
        "can you tell me a joke",
        "what is the weather like",
        "where is Paris",
        "who won the football match yesterday",
        "how do I cook pasta",
        "what is the capital of India",
        "help me with my homework",
        "tell me about yourself",
        "can you write a poem",
        "recommend a movie",
        "sing a song",
        "testing 1 2 3",
        "asdfasdf",
        "hello world",
        "blah blah blah"
    ]
}

classifier = NaiveBayesClassifier()
classifier.train(TRAINING_DATA)

# --- Entity Extractor ---
def find_longest_match(text, candidates):
    lower_text = text.lower()
    match = None
    for candidate in candidates:
        c = candidate.lower()
        # Look for word bounds or substring matching
        if c in lower_text:
            if not match or len(c) > len(match.lower()):
                match = candidate
    return match

def extract_date_range(text):
    lower = text.lower()
    now = datetime.now()
    start_of_day = lambda d: datetime(d.year, d.month, d.day, 0, 0, 0)
    end_of_day = lambda d: datetime(d.year, d.month, d.day, 23, 59, 59)

    if "today" in lower:
        return {"from": start_of_day(now), "to": now, "label": "today"}
    if "yesterday" in lower:
        y = now - timedelta(days=1)
        return {"from": start_of_day(y), "to": end_of_day(y), "label": "yesterday"}
    if "last 7 days" in lower or "this week" in lower or "past week" in lower:
        start = now - timedelta(days=7)
        return {"from": start_of_day(start), "to": now, "label": "last 7 days"}
    if "last month" in lower:
        # First day of last month
        first_day_this_month = datetime(now.year, now.month, 1)
        last_day_last_month = first_day_this_month - timedelta(days=1)
        first_day_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)
        return {"from": start_of_day(first_day_last_month), "to": end_of_day(last_day_last_month), "label": "last month"}
    if "this month" in lower:
        start = datetime(now.year, now.month, 1)
        return {"from": start_of_day(start), "to": now, "label": "this month"}
    
    # Fallback to last 30 days
    start = now - timedelta(days=30)
    return {"from": start_of_day(start), "to": now, "label": "last 30 days (default)"}

def extract_entities(text, context):
    known_items = context.get("knownItems", [])
    known_customers = context.get("knownCustomers", [])
    lower = text.lower()

    # Determine transaction type hint (closest keyword to numbers if multiple appear)
    transaction_type = None
    type_patterns = {
        'sale': r'\b(sold|sale|sales)\b',
        'purchase': r'\b(purchase|bought|buy)\b',
        'expense': r'\b(expense|bill)\b',
        'payment': r'\b(payment|received|paid|pay)\b',
        'refund': r'\b(refund|returned)\b'
    }

    keyword_matches = []
    for t_type, pattern in type_patterns.items():
        for match in re.finditer(pattern, lower):
            keyword_matches.append((t_type, match.start()))

    # Find number matches and their start positions
    number_matches = [match.start() for match in re.finditer(r'\b\d+(?:\.\d+)?\b', lower)]

    if keyword_matches:
        if number_matches:
            first_num_pos = number_matches[0]
            closest_match = min(keyword_matches, key=lambda km: abs(km[1] - first_num_pos))
            transaction_type = closest_match[0]
        else:
            closest_match = min(keyword_matches, key=lambda km: km[1])
            transaction_type = closest_match[0]

    # Extract numbers
    numbers = [float(n) for n in re.findall(r'\b\d+(?:\.\d+)?\b', text)]
    
    quantity = None
    unit_price = None
    amount = None

    if transaction_type in ['payment', 'refund', 'expense']:
        # For payments/refunds/expenses, a single number is the total payment amount
        if numbers:
            amount = numbers[0]
            unit_price = 0
            quantity = 0
    else:
        # For sales/purchases:
        if len(numbers) >= 2:
            quantity = round(numbers[0])
            unit_price = numbers[-1]
            amount = quantity * unit_price
        elif len(numbers) == 1:
            # Guess based on context words
            num = numbers[0]
            # If "at 50" or "for 50 each" or "50 rs"
            if re.search(r'\b(at|for|each|rs|rupees)\s+' + re.escape(str(round(num) if num.is_integer() else num)), lower) or \
               re.search(re.escape(str(round(num) if num.is_integer() else num)) + r'\s*(rs|rupees|each|per)', lower):
                unit_price = num
                quantity = 1
                amount = num
            else:
                quantity = round(num)
                unit_price = None
                amount = None

    # Longest match for items
    item = find_longest_match(text, known_items)
    
    # Smart Fallback for items (e.g. if the item is not yet in the user's DB)
    if not item and transaction_type in ['sale', 'purchase', None]:
        if quantity is not None:
            q_str = str(round(quantity))
            # Match words following the quantity, ending at a preposition or price indicator
            m = re.search(r'\b' + q_str + r'\s+([a-zA-Z\s]+?)\s+\b(at|for|each|rs|rupees|to|from)\b', lower)
            if m:
                candidate = m.group(1).strip()
                # Clean up unit descriptors
                candidate = re.sub(r'\b(units|kg|bags|bottles|packs|pieces|items|units of|kg of|bags of|bottles of|packs of|pieces of|items of)\b', '', candidate).strip()
                if candidate:
                    item = candidate.title()
        if not item:
            # Match "sale of X" or similar
            m = re.search(r'\b(sale|purchase|of|sold|bought)\s+([a-zA-Z\s]+?)\s+\b(to|from|at|for)\b', lower)
            if m:
                candidate = m.group(2).strip()
                candidate = re.sub(r'\b(units|kg|bags|bottles|packs|pieces|items|units of|kg of|bags of|bottles of|packs of|pieces of|items of)\b', '', candidate).strip()
                if candidate:
                    item = candidate.title()
    
    # Longest match for customers/shops
    customer = find_longest_match(text, known_customers)

    date_range = extract_date_range(text)

    return {
        "quantity": quantity,
        "unitPrice": unit_price,
        "amount": amount,
        "item": item,
        "customer": customer,
        "dateRange": date_range,
        "transactionType": transaction_type
    }

# --- Intent Handlers ---

def handle_add_transaction(conn, user_id, entities):
    t_type = entities["transactionType"]
    qty = entities["quantity"]
    price = entities["unitPrice"]
    item = entities["item"]
    customer = entities["customer"]
    amount = entities["amount"]

    if not t_type:
        return {"text": "I couldn't tell if that's a sale, payment, or refund — could you rephrase? (e.g., 'add a sale of...', 'record payment of...')", "data": None}

    if not customer:
        return {"text": "Please specify which shop or business this transaction is for (e.g., 'to ramesh', 'from general store').", "data": None}

    # Find the shop matching the customer name/owner
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT shop_id, shop_name, shop_owner FROM shops WHERE user_id = %s AND (LOWER(shop_name) = %s OR LOWER(shop_owner) = %s) LIMIT 1",
            (user_id, customer.lower(), customer.lower())
        )
        shop = cursor.fetchone()

    if not shop:
        return {"text": f"I couldn't find a shop matching '{customer}' in your profile. Make sure the shop name or owner name is spelled correctly.", "data": None}

    shop_id = shop["shop_id"]
    shop_name = shop["shop_name"]

    # Map transaction inputs to shop_inventory table
    product_name = item if item else ("Payment Received" if t_type == 'payment' else ("Refund Issued" if t_type == 'refund' else "Ledger Entry"))
    db_qty = qty if qty is not None else 0
    db_price = price if price is not None else 0
    
    # Determine amount actually paid (amount_paid) vs total amount
    # In a ledger:
    # A sale increases total_amount. If they pay, amount_paid > 0. If it's on credit, amount_paid = 0.
    # A payment has total_amount = 0 (qty=0, price=0), and amount_paid = positive.
    # A refund has total_amount = 0, and amount_paid = negative.
    if t_type == 'payment':
        amount_paid = amount if amount is not None else 0
        db_qty = 0
        db_price = 0
        payment_method = "CASH"
    elif t_type == 'refund':
        amount_paid = -abs(amount if amount is not None else 0)
        db_qty = 0
        db_price = 0
        payment_method = "CASH"
    else: # sale / purchase / general
        amount_paid = 0 # Default sale is on credit (unpaid) so they owe us
        payment_method = "CASH"

    # Insert into shop_inventory
    with conn.cursor() as cursor:
        sql = """
            INSERT INTO shop_inventory (shop_id, product_name, quantity, price, amount_paid, payment_method, notes, entry_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
        """
        cursor.execute(sql, (shop_id, product_name, db_qty, db_price, amount_paid, payment_method, "Added via NLP assistant"))
        conn.commit()
        insert_id = cursor.lastrowid

    # Display text
    if t_type == 'payment':
        display_text = f"Logged payment of ₹{amount_paid:.2f} received from shop '{shop_name}'."
    elif t_type == 'refund':
        display_text = f"Logged refund of ₹{abs(amount_paid):.2f} issued to shop '{shop_name}'."
    else:
        total_val = db_qty * db_price
        display_text = f"Logged sale of {db_qty} '{product_name}' at ₹{db_price:.2f} each (Total: ₹{total_val:.2f}) to shop '{shop_name}' on credit."

    return {
        "text": display_text,
        "data": {
            "id": insert_id,
            "shop_id": shop_id,
            "product_name": product_name,
            "quantity": db_qty,
            "price": db_price,
            "amount_paid": float(amount_paid),
            "payment_method": payment_method
        }
    }

def handle_query_sales(conn, user_id, entities):
    date_range = entities["dateRange"]
    item = entities["item"]
    customer = entities["customer"]

    params = [user_id, date_range["from"], date_range["to"]]
    sql = """
        SELECT i.item_id, i.product_name, i.quantity, i.price, i.total_amount, i.amount_paid, i.amount_rem, i.entry_date, s.shop_name
        FROM shop_inventory i
        JOIN shops s ON i.shop_id = s.shop_id
        WHERE s.user_id = %s AND i.quantity > 0 AND i.entry_date BETWEEN %s AND %s
    """
    
    if item:
        sql += " AND LOWER(i.product_name) = %s"
        params.append(item.lower())
    if customer:
        sql += " AND (LOWER(s.shop_name) = %s OR LOWER(s.shop_owner) = %s)"
        params.extend([customer.lower(), customer.lower()])

    sql += " ORDER BY i.entry_date DESC"

    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()

    if not rows:
        return {"text": f"No sales entries found for {date_range['label']}.", "data": []}

    total_revenue = sum(float(r["total_amount"]) for r in rows)
    total_units = sum(int(r["quantity"]) for r in rows)

    # Format the data for JSON
    for r in rows:
        r["total_amount"] = float(r["total_amount"])
        r["price"] = float(r["price"])
        r["amount_paid"] = float(r["amount_paid"])
        r["amount_rem"] = float(r["amount_rem"])
        r["entry_date"] = r["entry_date"].strftime("%Y-%m-%d")

    # Find top selling product
    by_product = {}
    for r in rows:
        prod = r["product_name"]
        by_product[prod] = by_product.get(prod, 0) + r["quantity"]
    
    top_product = sorted(by_product.items(), key=lambda x: x[1], reverse=True)[0]

    text = f"For {date_range['label']}: {len(rows)} sales records, {total_units} units sold, total revenue ₹{total_revenue:.2f}."
    text += f" Top seller: {top_product[0]} ({top_product[1]} units)."

    return {"text": text, "data": rows}

def handle_query_stock(conn, user_id, entities):
    item = entities["item"]

    with conn.cursor() as cursor:
        if item:
            sql = """
                SELECT i.product_name, SUM(i.quantity) as total_qty, s.shop_name
                FROM shop_inventory i
                JOIN shops s ON i.shop_id = s.shop_id
                WHERE s.user_id = %s AND LOWER(i.product_name) = %s
                GROUP BY s.shop_id, i.product_name
            """
            cursor.execute(sql, (user_id, item.lower()))
            rows = cursor.fetchall()
            
            if not rows:
                return {"text": f"I couldn't find any ledger entries for '{item}' in your shops.", "data": []}
            
            total_qty = sum(int(r["total_qty"]) for r in rows)
            details = ", ".join([f"{r['shop_name']} ({int(r['total_qty'])})" for r in rows])
            return {
                "text": f"Total '{item}' logged: {total_qty} units. Breakdown: {details}.",
                "data": [{ "product_name": r["product_name"], "total_qty": int(r["total_qty"]), "shop_name": r["shop_name"] } for r in rows]
            }
        else:
            sql = """
                SELECT i.product_name, SUM(i.quantity) as total_qty
                FROM shop_inventory i
                JOIN shops s ON i.shop_id = s.shop_id
                WHERE s.user_id = %s AND i.quantity > 0
                GROUP BY i.product_name
                ORDER BY total_qty DESC
            """
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                return {"text": "No products found in your shops' ledgers.", "data": []}

            list_str = ", ".join([f"{r['product_name']} ({int(r['total_qty'])})" for r in rows])
            return {
                "text": f"Items logged in ledger: {list_str}.",
                "data": [{ "product_name": r["product_name"], "total_qty": int(r["total_qty"]) } for r in rows]
            }

def handle_query_ledger(conn, user_id, entities):
    customer = entities["customer"]

    with conn.cursor() as cursor:
        if customer:
            sql = """
                SELECT s.shop_id, s.shop_name, 
                       COALESCE(SUM(i.total_amount), 0) as total_amount,
                       COALESCE(SUM(i.amount_paid), 0) as total_paid,
                       COALESCE(SUM(i.amount_rem), 0) as total_owed
                FROM shops s
                LEFT JOIN shop_inventory i ON s.shop_id = i.shop_id
                WHERE s.user_id = %s AND (LOWER(s.shop_name) = %s OR LOWER(s.shop_owner) = %s)
                GROUP BY s.shop_id
            """
            cursor.execute(sql, (user_id, customer.lower(), customer.lower()))
            shop = cursor.fetchone()

            if not shop:
                return {"text": f"I couldn't find a shop matching '{customer}'.", "data": None}

            owed = float(shop["total_owed"])
            shop_name = shop["shop_name"]

            # Fetch last few transactions for this shop
            cursor.execute(
                "SELECT product_name, quantity, price, amount_paid, amount_rem, entry_date FROM shop_inventory WHERE shop_id = %s ORDER BY entry_date DESC LIMIT 5",
                (shop["shop_id"],)
            )
            txs = cursor.fetchall()
            for t in txs:
                t["amount_paid"] = float(t["amount_paid"])
                t["price"] = float(t["price"])
                t["amount_rem"] = float(t["amount_rem"])
                t["entry_date"] = t["entry_date"].strftime("%Y-%m-%d")

            if owed > 0:
                text = f"Shop '{shop_name}' has an outstanding balance of ₹{owed:.2f} (Total purchases: ₹{float(shop['total_amount']):.2f}, Paid: ₹{float(shop['total_paid']):.2f})."
            else:
                text = f"Shop '{shop_name}' account is settled (Outstanding: ₹{owed:.2f})."

            return {"text": text, "data": { "shop": shop_name, "owed": owed, "recent_transactions": txs }}
        
        else:
            # Query outstanding balance across all shops
            sql = """
                SELECT s.shop_name, COALESCE(SUM(i.amount_rem), 0) as total_owed
                FROM shops s
                LEFT JOIN shop_inventory i ON s.shop_id = i.shop_id
                WHERE s.user_id = %s
                GROUP BY s.shop_id
                HAVING total_owed > 0
                ORDER BY total_owed DESC
            """
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                return {"text": "All shops are settled up! No outstanding balances.", "data": []}

            list_str = ", ".join([f"{r['shop_name']}: ₹{float(r['total_owed']):.2f}" for r in rows])
            
            # Format output data
            for r in rows:
                r["total_owed"] = float(r["total_owed"])

            return {
                "text": f"Outstanding balances — {list_str}.",
                "data": rows
            }

def handle_get_insights(conn, user_id):
    now = datetime.now()
    start_of_this_month = datetime(now.year, now.month, 1)
    
    # Last month boundaries
    first_day_this_month = datetime(now.year, now.month, 1)
    last_day_last_month = first_day_this_month - timedelta(days=1)
    start_of_last_month = datetime(last_day_last_month.year, last_day_last_month.month, 1)
    end_of_last_month = datetime(last_day_last_month.year, last_day_last_month.month, last_day_last_month.day, 23, 59, 59)

    with conn.cursor() as cursor:
        # This month's revenue
        cursor.execute(
            """
            SELECT COALESCE(SUM(i.total_amount), 0) AS revenue, COALESCE(SUM(i.quantity), 0) AS units
            FROM shop_inventory i
            JOIN shops s ON i.shop_id = s.shop_id
            WHERE s.user_id = %s AND i.quantity > 0 AND i.entry_date >= %s
            """,
            (user_id, start_of_this_month)
        )
        this_month_data = cursor.fetchone()
        
        # Last month's revenue
        cursor.execute(
            """
            SELECT COALESCE(SUM(i.total_amount), 0) AS revenue, COALESCE(SUM(i.quantity), 0) AS units
            FROM shop_inventory i
            JOIN shops s ON i.shop_id = s.shop_id
            WHERE s.user_id = %s AND i.quantity > 0 AND i.entry_date BETWEEN %s AND %s
            """,
            (user_id, start_of_last_month, end_of_last_month)
        )
        last_month_data = cursor.fetchone()

        # Top 3 movers this month
        cursor.execute(
            """
            SELECT i.product_name, SUM(i.quantity) AS units
            FROM shop_inventory i
            JOIN shops s ON i.shop_id = s.shop_id
            WHERE s.user_id = %s AND i.quantity > 0 AND i.entry_date >= %s
            GROUP BY i.product_name
            ORDER BY units DESC LIMIT 3
            """,
            (user_id, start_of_this_month)
        )
        top_movers = cursor.fetchall()

        # Top shops with debt
        cursor.execute(
            """
            SELECT s.shop_name, COALESCE(SUM(i.amount_rem), 0) as total_owed
            FROM shops s
            LEFT JOIN shop_inventory i ON s.shop_id = i.shop_id
            WHERE s.user_id = %s
            GROUP BY s.shop_id
            HAVING total_owed > 0
            ORDER BY total_owed DESC LIMIT 3
            """,
            (user_id,)
        )
        top_debtors = cursor.fetchall()

    rev_this = float(this_month_data["revenue"])
    units_this = int(this_month_data["units"])
    rev_last = float(last_month_data["revenue"])

    revenue_delta = None
    if rev_last > 0:
        revenue_delta = ((rev_this - rev_last) / rev_last) * 100

    lines = [
        f"This month's revenue: ₹{rev_this:.2f} from {units_this} units logged."
    ]
    if revenue_delta is not None:
        direction = "up" if revenue_delta >= 0 else "down"
        lines.append(f"That's {direction} {abs(revenue_delta):.1f}% versus last month (₹{rev_last:.2f}).")
    
    if top_movers:
        movers_str = ", ".join([f"{m['product_name']} ({int(m['units'])})" for m in top_movers])
        lines.append(f"Top moving items: {movers_str}.")
    
    if top_debtors:
        debtors_str = ", ".join([f"{d['shop_name']} (₹{float(d['total_owed']):.2f})" for d in top_debtors])
        lines.append(f"⚠️ Shops with highest outstanding balance: {debtors_str}.")
    else:
        lines.append("All shops ledger accounts are clear and healthy.")

    # Convert counts to standard float/int
    this_month_data["revenue"] = float(this_month_data["revenue"])
    this_month_data["units"] = int(this_month_data["units"])
    last_month_data["revenue"] = float(last_month_data["revenue"])
    last_month_data["units"] = int(last_month_data["units"])
    for m in top_movers:
        m["units"] = int(m["units"])
    for d in top_debtors:
        d["total_owed"] = float(d["total_owed"])

    return {
        "text": " ".join(lines),
        "data": {
            "thisMonth": this_month_data,
            "lastMonth": last_month_data,
            "topMovers": top_movers,
            "topDebtors": top_debtors
        }
    }

# --- HTTP API Request Handler ---

class NLPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default server logs to keep console clean
        pass

    def do_POST(self):
        if self.path == '/chat':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request_data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_error_response(400, f"Invalid JSON body: {str(e)}")
                return

            message = request_data.get("message")
            user_id = request_data.get("user_id")

            if not message or not user_id:
                self.send_error_response(400, "Both 'message' and 'user_id' are required fields.")
                return

            try:
                conn = get_db_connection()
            except Exception as e:
                self.send_error_response(500, f"Database connection failed: {str(e)}")
                return

            try:
                # 1. Classify intent
                intent, confidence = classifier.classify(message)

                if intent == "UNKNOWN":
                    self.send_json_response({
                        "reply": "I'm not sure what you mean — try things like 'show sales for this week', 'add a sale of 5 notebooks at 20 to Ramesh', or 'give me outstanding balances'.",
                        "intent": intent,
                        "confidence": confidence,
                        "data": None
                    })
                    return

                # 2. Get contextual lists for entity extraction (shops and items)
                with conn.cursor() as cursor:
                    # Get user's shop names and owner names
                    cursor.execute("SELECT shop_name, shop_owner FROM shops WHERE user_id = %s", (user_id,))
                    shops = cursor.fetchall()
                    known_customers = []
                    for s in shops:
                        if s["shop_name"]: known_customers.append(s["shop_name"])
                        if s["shop_owner"]: known_customers.append(s["shop_owner"])
                    
                    # Get user's distinct item names
                    cursor.execute(
                        "SELECT DISTINCT product_name FROM shop_inventory i JOIN shops s ON i.shop_id = s.shop_id WHERE s.user_id = %s",
                        (user_id,)
                    )
                    items = cursor.fetchall()
                    known_items = [i["product_name"] for i in items if i["product_name"]]

                context = {"knownItems": known_items, "knownCustomers": known_customers}

                # 3. Extract entities
                entities = extract_entities(message, context)

                # 4. Handle intent
                result = {"text": "Intent understood but no handler mapped.", "data": None}
                if intent == "ADD_TRANSACTION":
                    result = handle_add_transaction(conn, user_id, entities)
                elif intent == "QUERY_SALES":
                    result = handle_query_sales(conn, user_id, entities)
                elif intent == "QUERY_STOCK":
                    result = handle_query_stock(conn, user_id, entities)
                elif intent == "QUERY_LEDGER":
                    result = handle_query_ledger(conn, user_id, entities)
                elif intent == "GET_INSIGHTS":
                    result = handle_get_insights(conn, user_id)

                self.send_json_response({
                    "reply": result["text"],
                    "data": result["data"],
                    "intent": intent,
                    "confidence": confidence,
                    "entities": {
                        "quantity": entities["quantity"],
                        "unitPrice": entities["unitPrice"],
                        "amount": entities["amount"],
                        "item": entities["item"],
                        "customer": entities["customer"],
                        "transactionType": entities["transactionType"]
                    }
                })

            except Exception as e:
                import traceback
                print(f"[NLP Server] Error handling request: {e}", file=sys.stderr)
                traceback.print_exc()
                self.send_error_response(500, f"Error processing message: {str(e)}")
            finally:
                conn.close()
        else:
            self.send_error_response(404, "Endpoint not found")

    def send_json_response(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode('utf-8'))

    def do_OPTIONS(self):
        # Enable CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run_server():
    server_address = ('', 5005)
    httpd = HTTPServer(server_address, NLPHandler)
    print("[NLP Server] Running Python NLP Service on port 5005...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[NLP Server] Stopping server...")
        httpd.server_close()

if __name__ == '__main__':
    run_server()

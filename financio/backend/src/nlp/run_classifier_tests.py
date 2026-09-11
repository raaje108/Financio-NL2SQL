import sys
import os

# Set current path to search nlp_server.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from nlp_server import classifier

TEST_CASES = [
    # --- ADD_TRANSACTION ---
    ("add a sale of 5 notebooks at 20 each to ramesh", "ADD_TRANSACTION"),
    ("record sale 3 pens to suresh for 15 rupees each", "ADD_TRANSACTION"),
    ("log a purchase of 10 units of rice at 40 per unit", "ADD_TRANSACTION"),
    ("add new entry sold 2 chairs to priya", "ADD_TRANSACTION"),
    ("create a transaction for 7 bags of cement to the site", "ADD_TRANSACTION"),
    ("i sold 4 bottles of oil to kumar today", "ADD_TRANSACTION"),
    ("add expense of 500 for shop electricity bill", "ADD_TRANSACTION"),
    ("record a payment received of 2000 from ramesh", "ADD_TRANSACTION"),
    ("log purchase 20 kg sugar from supplier at 45 rs", "ADD_TRANSACTION"),
    ("payment of 1500 received from suresh", "ADD_TRANSACTION"),
    ("refund issued of 400 to kumar", "ADD_TRANSACTION"),
    ("record refund of 250 to priya", "ADD_TRANSACTION"),
    ("sold 10 packets of chips for 15 rupees each to ram", "ADD_TRANSACTION"),
    ("purchased 50 items of light bulbs at 30 each from supplier", "ADD_TRANSACTION"),
    ("add a cash payment of 1200 from rahul electronics", "ADD_TRANSACTION"),
    ("registered payment of 500 from sai kirana", "ADD_TRANSACTION"),
    ("spent 300 on transport tea snacks expense", "ADD_TRANSACTION"),
    ("gave a refund of 150 to sharma shop", "ADD_TRANSACTION"),
    ("logged sale 12 boxes of pens to nikhil at 100 rs per box", "ADD_TRANSACTION"),
    ("record purchase of 5 tons of bricks for 15000", "ADD_TRANSACTION"),
    ("add transaction 15 shirts sold at 400 rupees to amit", "ADD_TRANSACTION"),

    # --- QUERY_SALES ---
    ("what were my top selling items last month", "QUERY_SALES"),
    ("show me sales for this week", "QUERY_SALES"),
    ("how much did i sell yesterday", "QUERY_SALES"),
    ("what is my total revenue this month", "QUERY_SALES"),
    ("give me sales report for last 7 days", "QUERY_SALES"),
    ("how many units of rice were sold this month", "QUERY_SALES"),
    ("what did ramesh buy last time", "QUERY_SALES"),
    ("show total sales for today", "QUERY_SALES"),
    ("which item sold the most last week", "QUERY_SALES"),
    ("list my transactions for today", "QUERY_SALES"),
    ("how much sales revenue did we make last quarter", "QUERY_SALES"),
    ("show me the sales breakdown for yesterday", "QUERY_SALES"),
    ("what is the total value of sales this week", "QUERY_SALES"),
    ("list all sales entries of cement this month", "QUERY_SALES"),
    ("what was sold to suresh yesterday", "QUERY_SALES"),
    ("find all sales records between monday and wednesday", "QUERY_SALES"),
    ("how many transactions did we have today", "QUERY_SALES"),
    ("show the revenue summary for the last 30 days", "QUERY_SALES"),
    ("what is my best selling product this week", "QUERY_SALES"),
    ("display sales log for last month", "QUERY_SALES"),
    ("how much did i earn from sales yesterday", "QUERY_SALES"),

    # --- QUERY_STOCK ---
    ("what items are low on stock", "QUERY_STOCK"),
    ("how much rice is left in stock", "QUERY_STOCK"),
    ("show me current inventory", "QUERY_STOCK"),
    ("which products are out of stock", "QUERY_STOCK"),
    ("check stock level for sugar", "QUERY_STOCK"),
    ("do we have enough cement in stock", "QUERY_STOCK"),
    ("list items below reorder level", "QUERY_STOCK"),
    ("show product quantities", "QUERY_STOCK"),
    ("how many notebooks do we have left", "QUERY_STOCK"),
    ("what is the stock status of pens", "QUERY_STOCK"),
    ("list all products with zero stock", "QUERY_STOCK"),
    ("display the inventory levels for all items", "QUERY_STOCK"),
    ("do we need to reorder any stock", "QUERY_STOCK"),
    ("check stock for books", "QUERY_STOCK"),
    ("how much quantity is left for oil bottles", "QUERY_STOCK"),
    ("list items in stock", "QUERY_STOCK"),
    ("show stock levels of electronics", "QUERY_STOCK"),
    ("check inventory count", "QUERY_STOCK"),
    ("are we running out of sugar", "QUERY_STOCK"),
    ("how many bags of cement are available", "QUERY_STOCK"),
    ("what is the quantity of shirts left", "QUERY_STOCK"),

    # --- QUERY_LEDGER ---
    ("how much does ramesh owe me", "QUERY_LEDGER"),
    ("show ledger for suresh", "QUERY_LEDGER"),
    ("what is the outstanding balance for priya", "QUERY_LEDGER"),
    ("show all pending payments", "QUERY_LEDGER"),
    ("who owes me money", "QUERY_LEDGER"),
    ("show transaction history for kumar", "QUERY_LEDGER"),
    ("give me outstanding statement", "QUERY_LEDGER"),
    ("how much balance is pending for amit", "QUERY_LEDGER"),
    ("who has not paid their due yet", "QUERY_LEDGER"),
    ("what is the ledger balance for sai kirana store", "QUERY_LEDGER"),
    ("show outstanding dues for all shops", "QUERY_LEDGER"),
    ("how much credit is given to rahul electronics", "QUERY_LEDGER"),
    ("list all unpaid transactions", "QUERY_LEDGER"),
    ("does suresh owe any money", "QUERY_LEDGER"),
    ("outstanding statement for ganesh", "QUERY_LEDGER"),
    ("who owes the highest amount", "QUERY_LEDGER"),
    ("show credit history for priya", "QUERY_LEDGER"),
    ("how much cash balance is remaining from kumar", "QUERY_LEDGER"),
    ("ledger details for ram", "QUERY_LEDGER"),
    ("find outstanding balance for sharma shop", "QUERY_LEDGER"),
    ("is there any due balance from nikhil", "QUERY_LEDGER"),

    # --- GET_INSIGHTS ---
    ("give me insights on my business", "GET_INSIGHTS"),
    ("summarize my shop performance", "GET_INSIGHTS"),
    ("how is my business doing this month", "GET_INSIGHTS"),
    ("give me a summary of sales and stock", "GET_INSIGHTS"),
    ("show me trends for this month", "GET_INSIGHTS"),
    ("analyze my revenue growth", "GET_INSIGHTS"),
    ("what insights do you have for me", "GET_INSIGHTS"),
    ("give me business performance analysis", "GET_INSIGHTS"),
    ("how is my shop doing compared to last month", "GET_INSIGHTS"),
    ("summarize my revenue and outstanding balance", "GET_INSIGHTS"),
    ("what are the key highlights of my business this week", "GET_INSIGHTS"),
    ("give me a general report on how my shop is performing", "GET_INSIGHTS"),
    ("analyze my sales and debt trends", "GET_INSIGHTS"),
    ("is my business profitable this month", "GET_INSIGHTS"),
    ("give me a summary of my business growth", "GET_INSIGHTS"),
    ("tell me how my shops are performing overall", "GET_INSIGHTS"),
    ("what insights can you give about my debtors", "GET_INSIGHTS"),
    ("show my business summary report", "GET_INSIGHTS"),
    ("analyze trends in sales and inventory", "GET_INSIGHTS"),
    ("how has my revenue changed compared to last week", "GET_INSIGHTS"),
    ("business health check report", "GET_INSIGHTS"),

    # --- UNKNOWN ---
    ("hello", "UNKNOWN"),
    ("hi there", "UNKNOWN"),
    ("hey assistant", "UNKNOWN"),
    ("good morning", "UNKNOWN"),
    ("good evening", "UNKNOWN"),
    ("how are you today", "UNKNOWN"),
    ("yo", "UNKNOWN"),
    ("what's up", "UNKNOWN"),
    ("who are you", "UNKNOWN"),
    ("what is the meaning of life", "UNKNOWN"),
    ("can you tell me a joke", "UNKNOWN"),
    ("what is the weather like", "UNKNOWN"),
    ("where is Paris", "UNKNOWN"),
    ("who won the football match yesterday", "UNKNOWN"),
    ("how do I cook pasta", "UNKNOWN"),
    ("what is the capital of India", "UNKNOWN"),
    ("help me with my homework", "UNKNOWN"),
    ("tell me about yourself", "UNKNOWN"),
    ("can you write a poem", "UNKNOWN"),
    ("recommend a movie", "UNKNOWN"),
    ("sing a song", "UNKNOWN"),
    ("testing 1 2 3", "UNKNOWN"),
    ("asdfasdf", "UNKNOWN"),
    ("hello world", "UNKNOWN"),
    ("blah blah blah", "UNKNOWN"),
]

def run_tests():
    passed = 0
    total = len(TEST_CASES)
    mismatches = []
    
    results_md_lines = [
        "# Naive Bayes Classifier Test Results",
        "",
        f"This report shows the validation results of testing the Naive Bayes Intent Classifier on **{total} validation prompts**.",
        "",
        "## Summary Metrics",
        ""
    ]

    print(f"Running classifier validation on {total} test prompts...")

    # Run classifications
    detailed_rows = []
    for prompt, expected in TEST_CASES:
        predicted, confidence = classifier.classify(prompt)
        is_correct = (predicted == expected)
        
        if is_correct:
            passed += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
            mismatches.append((prompt, expected, predicted, confidence))
            
        detailed_rows.append(f"| {prompt} | `{expected}` | `{predicted}` | {confidence * 100:.1f}% | {status} |")

    accuracy = (passed / total) * 100
    
    # Write summary
    results_md_lines.append(f"- **Total Prompts Tested**: {total}")
    results_md_lines.append(f"- **Passed**: {passed}")
    results_md_lines.append(f"- **Failed**: {total - passed}")
    results_md_lines.append(f"- **Accuracy Rate**: **{accuracy:.2f}%**")
    results_md_lines.append("")
    
    if mismatches:
        results_md_lines.append("## Mismatch Details")
        results_md_lines.append("| Test Prompt | Expected Intent | Predicted Intent | Confidence |")
        results_md_lines.append("| :--- | :--- | :--- | :--- |")
        for prompt, expected, predicted, confidence in mismatches:
            results_md_lines.append(f"| \"{prompt}\" | `{expected}` | `{predicted}` | {confidence * 100:.1f}% |")
        results_md_lines.append("")
        
    results_md_lines.append("## Detailed Test Log")
    results_md_lines.append("| Prompt | Expected Intent | Predicted Intent | Confidence | Status |")
    results_md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
    results_md_lines.extend(detailed_rows)
    
    # Save markdown report to artifacts folder
    artifact_dir = "C:/Users/Dell/.gemini/antigravity/brain/ba6e6f06-7b8e-49e0-9f62-747337c3a873"
    report_path = os.path.join(artifact_dir, "nlp_test_results.md")
    
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(results_md_lines))
        print(f"Test report written successfully to: {report_path}")
    except Exception as e:
        print(f"Error writing markdown report: {e}")
        
    # Output to stdout
    print(f"\nTest Execution Complete!")
    print(f"Accuracy: {passed}/{total} ({accuracy:.2f}%)")
    if mismatches:
        print(f"Mismatches: {len(mismatches)}")

if __name__ == "__main__":
    run_tests()

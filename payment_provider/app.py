from flask import Flask, jsonify, request, redirect, render_template
import random
import string
from logger import Logger

app = Flask(__name__)
logger = Logger()

transactions = {}

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/", methods=["GET"])
def process_payment():
    try:
        logger.info("Processing payment")
        
        user_id = request.args.get("user_id")
        total = request.args.get("total")
        currency = request.args.get("currency")
        return_url = request.args.get("return")
        transaction_id = generate_random_string(8)
        
        logger.info(f"Payment processed for transaction_id: {transaction_id}")
        
        return render_template("payment_form.html", user_id=user_id, total=total, currency=currency, return_url=return_url, transaction_id = transaction_id)
    
    except Exception as e:
        logger.error(f"Error processing payment: {str(e)}")
        return jsonify({"error": str(e)})

@app.route("/submit-payment", methods=["POST"])
def submit_payment():
    try:
        logger.info("Submitting payment")
        
        form_data = request.form
        user_id = form_data.get("user_id")
        transaction_id = form_data.get("transaction_id")
        total = form_data.get("total")
        currency = form_data.get("currency")
        return_url = form_data.get("return")
        
        transactions[transaction_id] = {"result": "success", "user_id": user_id, "total": total, "currency": currency}
        
        logger.info(f"Payment submitted for transaction_id: {transaction_id}")
        
        return_url += f"&transaction={transaction_id}&user_id={user_id}"
        
        return redirect(return_url, code=302)
    except Exception as e:
        logger.error(f"Error submitting payment: {str(e)}")
        return jsonify({"error": str(e)})

@app.route("/transaction-status", methods=["GET"])
def transaction_status():
    try:
        logger.info("Getting transaction status")
        transaction_id = request.args.get("transaction")
        
        if transaction_id in transactions:
            logger.info(f"Transaction status retrieved for transaction_id: {transaction_id}")
            return jsonify(transactions[transaction_id])
        
        else:
            logger.error(f"Transaction not found for transaction_id: {transaction_id}")
            return jsonify({"result": "error", "message": "Transaction not found"})
        
    except Exception as e:
        logger.error(f"Error getting transaction status: {str(e)}")
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8010)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}")

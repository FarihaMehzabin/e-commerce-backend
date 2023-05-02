from flask import Flask, jsonify, request, redirect, render_template
import random
import string

app = Flask(__name__)

transactions = {}


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


@app.route("/", methods=["GET"])
def process_payment():
    user_id = request.args.get("user_id")
    total = request.args.get("total")
    currency = request.args.get("currency")
    return_url = request.args.get("return")

    transaction_id = generate_random_string(8)  # Generate a unique transaction ID here

    transactions[transaction_id] = {
        "result": "success",
        "user_id": user_id,
        "total": total,
        "currency": currency,
    }
    
    return render_template("payment_form.html", user_id=user_id, total=total, currency=currency, return_url=return_url, transaction_id = transaction_id)


@app.route("/transaction-status", methods=["GET"])
def transaction_status():
    transaction_id = request.args.get("transaction")


    if transaction_id in transactions:
        return jsonify(transactions[transaction_id])
    else:
        return jsonify({"result": "error", "message": "Transaction not found"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010)

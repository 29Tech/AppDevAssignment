from flask import Flask, request, render_template, session, redirect, url_for
import shelve

app = Flask(__name__)
app.secret_key = "supersecretkey"
MAX_POINTS = 2000


def get_items():
    with shelve.open("rewards.db") as db:
        items = db.get("items", {})
    print(f"DEBUG: Available items = {items}")
    print(f"DEBUG: Item names in DB = {list(items.keys())}")  # List all item names
    return items



def save_items(items):
    with shelve.open("rewards.db", writeback=True) as db:
        db["items"] = items


@app.route("/", methods=["GET", "POST"])
def index():
    name = session.get("name", "Guest")

    if request.method == "POST":
        points = request.form.get("points")
        if points and points.isdigit():
            with shelve.open("user_data.db", writeback=True) as db:
                user_data = db.get(name, {"cumulative_points": 0, "spendable_points": 0, "redeemed_items": []})
                user_data["cumulative_points"] += int(points)
                user_data["spendable_points"] += int(points)
                db[name] = user_data
            return redirect(url_for("index"))

    with shelve.open("user_data.db") as db:
        user_data = db.get(name, {"cumulative_points": 0, "spendable_points": 0, "redeemed_items": []})
        cumulative_points = user_data.get("cumulative_points", 0)
        spendable_points = user_data.get("spendable_points", 0)
        redeemed_items = user_data.get("redeemed_items", [])

    percentage = min((cumulative_points / MAX_POINTS) * 100, 100)
    points_left = max(MAX_POINTS - cumulative_points, 0)

    return render_template(
        "profile.html",
        cumulative_points=cumulative_points,
        spendable_points=spendable_points,
        percentage=percentage,
        name=name,
        points_left=points_left,
        redeemed_items=redeemed_items,
    )



@app.route("/points")
def points():
    return render_template("points.html")



@app.route("/profile/<name>")
def profile(name):
    session["name"] = name
    print(f"DEBUG: Profile set for {name}")
    return redirect(url_for("index"))



@app.route("/redeempoints", methods=["GET", "POST"])
def redeempoints():
    name = session.get("name", "Guest")
    is_admin = name.lower() == "admin"
    message = None

    with shelve.open("user_data.db", writeback=True) as db:
        user_data = db.get(name, {"cumulative_points": 0, "spendable_points": 0})
        spendable_points = user_data.get("spendable_points", 0)

    items = get_items()

    if request.method == "POST":
        action = request.form.get("action")
        item_name = request.form.get("item")

        # User Redeems an Item
        if action == "redeem" and item_name in items:
            address = request.form.get("address")
            item = items[item_name]

            if spendable_points >= item["price"] and item["stock"] > 0:
                spendable_points -= item["price"]
                item["stock"] -= 1

                with shelve.open("user_data.db", writeback=True) as db:
                    user_data["spendable_points"] = spendable_points
                    user_data.setdefault("redeemed_items", []).append({
                        "item": item_name,
                        "price": item["price"],
                        "address": address
                    })
                    db[name] = user_data

                save_items(items)
                message = f"Item '{item_name}' redeemed successfully!"
            else:
                message = "Not enough spendable points or item out of stock."

        # Admin Adds an Item
        elif is_admin and action == "add":
            price = request.form.get("price")
            stock = request.form.get("stock")

            if item_name and price and stock:
                try:
                    price = int(price)
                    stock = int(stock)

                    if item_name in items:
                        message = "Item already exists!"
                    else:
                        items[item_name] = {
                            "price": price,
                            "stock": stock,
                            "image": "default.jpg"  # Change as needed
                        }
                        save_items(items)
                        message = f"Item '{item_name}' added successfully!"

                except ValueError:
                    message = "Invalid price or stock value."

        # Admin Removes an Item
        elif is_admin and action == "remove" and item_name in items:
            del items[item_name]
            save_items(items)
            message = f"Item '{item_name}' removed successfully!"

        return redirect(url_for("redeempoints"))

    return render_template(
        "redeempoints.html",
        spendable_points=spendable_points,
        items=items,
        is_admin=is_admin,
        message=message,
    )




@app.route("/redeem_confirmation/<item_name>", methods=["POST"])
def redeem_confirmation(item_name):
    name = session.get("name", "Guest")

    items = get_items()
    item = items.get(item_name)

    if not item:
        return redirect(url_for("redeempoints"))

    with shelve.open("user_data.db", writeback=True) as db:
        user_data = db.get(name, {
            "cumulative_points": 0,
            "spendable_points": 0,
            "redeemed_items": []
        })

    spendable_points = user_data.get("spendable_points", 0)
    message = None

    if request.method == "POST":
        address = request.form.get("address")  # Get entered address
        if spendable_points >= item["price"] and item["stock"] > 0:
            spendable_points -= item["price"]
            item["stock"] -= 1

            if "redeemed_items" not in user_data:
                user_data["redeemed_items"] = []

            user_data["redeemed_items"].append({
                "item": item_name,
                "price": item["price"],
                "address": address
            })
            user_data["spendable_points"] = spendable_points

            with shelve.open("user_data.db", writeback=True) as db:
                db[name] = user_data
            save_items(items)

            message = f"Item '{item_name}' redeemed successfully!"
            return redirect(url_for("redeempoints", message=message))
        else:
            message = "Not enough spendable points or item out of stock."

    return render_template(
        "redeemconfirmation.html",
        item_name=item_name,
        item=item,
        spendable_points=spendable_points,
        message=message
    )





if __name__ == "__main__":
    app.run(debug=True)

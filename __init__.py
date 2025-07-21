from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from math import ceil
from Forms import PaymentForm, DonationForm, DetailForm, CreateSubForm
import shelve, Receipts, Donations, Details, Sub
import os
from werkzeug.utils import secure_filename
import random
from wtforms import Form, validators
from wtforms.fields import EmailField


app = Flask(__name__)
app.secret_key = 'your_secret_key'
MAX_POINTS = 2000

DATABASE = 'users.db'
SHELVE_FILE = 'products.db'
CART_FILE = 'cart.db'

UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.context_processor
def inject_user():
    return dict(username=session.get('username'))
















######################## Dashboard #########################################

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    with shelve.open(DATABASE) as db:
        users = db.get('users', {})
        user = users.get(username)

    if not user:
        flash("User not found.")
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=user)


















############################ Login ####################################



def init_db():
    """Initialize the shelve database."""
    with shelve.open(DATABASE) as db:
        if 'users' not in db:
            db['users'] = {}  # Correct key is 'users', as used in your code.


init_db()


@app.route('/')
def home():
    username = session.get('username')  # Get the username from the session
    print(username)
    return render_template('Homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with shelve.open(DATABASE) as db:
            users = db.get('users', {})
            user = users.get(username)

        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('aftlogin'))  # Redirect to user-specific dashboard
        else:
            message = 'Invalid username or password.'

    return render_template('Login.html', message=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            message = 'Passwords do not match!'
            return render_template('Signup.html', message=message)

        with shelve.open(DATABASE) as db:
            users = db.get('users', {})

            # Ensure email is unique
            if any(user['email'] == email for user in users.values()):
                message = 'Email already exists!'
                return render_template('Signup.html', message=message)

            # Add new user
            users[username] = {
                'username': username,
                'email': email,
                'password': password,
                'receipts': [],
                'donations': [],
                'cart': {}
            }
            db['users'] = users  # Save the updated dictionary

        message = 'Registration successful! Please log in.'
        return redirect(url_for('login'))

    return render_template('Signup.html', message=message)



@app.route('/Cpass', methods=['GET', 'POST'])
def cpass():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']

        # Open the database to check and update the user's password
        with shelve.open(DATABASE) as db:
            users = db.get('users', {})
            user_found = None

            # Check if the email exists
            for username, user in users.items():
                if isinstance(user, dict) and user.get('email') == email:  # Ensure user is a dict
                    user_found = username
                    break

            if user_found:
                # Update the user's password
                users[user_found]['password'] = new_password
                db['users'] = users
                message = "Your password has been successfully updated."
            else:
                message = "Email not found. Please try again."

    return render_template('Cpass.html', message=message)


@app.route('/aftlogin')
def aftlogin():
    print(session)
    username = session.get('username')  # Get the username from the session
    print(username)
    if not username:
        return redirect(url_for('login'))  # Redirect to login if no user is logged in
    return render_template('aftlogin.html', username=username)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    users_dict.pop(id)

    db['Users'] = users_dict
    db.close()

    return redirect(url_for('signup'))


@app.route('/signout')
def signout():
    session.clear()  # Clear all session data
    flash("You have been signed out.")
    return redirect(url_for('home'))


@app.route('/myaccount', methods=['GET', 'POST'])
def my_account():
    username = session.get('username')  # Get the username from the session
    if not username:
        return redirect(url_for('login'))  # Redirect to login if no user is logged in

    with shelve.open(DATABASE, writeback=True) as db:
        users = db.get('users', {})
        user = users.get(username)

        if not user:
            flash("User not found. Please log in again.")
            return redirect(url_for('login'))

        if request.method == 'POST':
            # Get updated values from the form
            updated_name = request.form['name']
            updated_email = request.form['email']

            if updated_name != user['username']:  # If the username changes
                # Update the username in the database
                users[updated_name] = user  # Create a new entry with the updated name
                del users[username]  # Delete the old entry
                user['username'] = updated_name  # Update the username in the user dictionary
                session['username'] = updated_name  # Update the session to reflect the new username

            # Update other user details
            user['name'] = updated_name
            user['email'] = updated_email
            db['users'] = users  # Save the updated user details back to the database

            flash("Profile updated successfully.")
            return redirect(url_for('my_account'))  # Refresh the page to reflect changes

    return render_template('myaccount.html', user=user)


@app.route('/loginCpassword', methods=['GET', 'POST'])
def logincpass():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']

        # Open the database to check and update the user's password
        with shelve.open(DATABASE) as db:
            users = db.get('users', {})
            user_found = None

            # Check if the email exists
            for username, user in users.items():
                if isinstance(user, dict) and user.get('email') == email:  # Ensure user is a dict
                    user_found = username
                    break

            if user_found:
                # Update the user's password
                users[user_found]['password'] = new_password
                db['users'] = users
                message = "Your password has been successfully updated."
            else:
                message = "Email not found. Please try again."

    return render_template('loginCpassword.html', message=message)














################## Product ############################

def initialize_default_products():
    default_products = [
        {"name": "Handheld Broom and Dustpan Set", "price": 5.99, "discount": 0.1, "description": "This compact broom and dustpan set is made from recycled plastic, making it a durable and eco-friendly option for quick cleanups around the house. Perfect for everyday use while helping reduce plastic waste.", "image_filename": "productImage1.jpg"},
        {"name": "Ziploc: Reusable Food Storage Bags", "price": 7.99, "discount": 0.12, "description": "These eco-friendly silicone food storage bags are made from recycled materials. They provide a sustainable alternative to disposable plastic bags, keeping your food fresh while being gentle on the environment.", "image_filename": "productImage2.jpg"},
        {"name": "Thermal Flask", "price": 8.99, "discount": 0.08, "description": "This thermal flask is made from recycled stainless steel, designed to keep your drinks hot or cold for longer. It’s a great way to enjoy your beverages while contributing to a cleaner planet.", "image_filename": "productImage3.jpg"},
        {"name": "Over-the-Door Hooks", "price": 4.99, "discount": 0.1, "description": "These over-the-door hooks are made from recycled metal, offering a sustainable and space-saving solution for hanging clothes and accessories. An efficient way to organize your home with a positive impact on the environment.", "image_filename": "productImage4.jpg"},
        {"name": "Collapsible Laundry Basket", "price": 9.99, "discount": 0.05, "description": "Made from recycled fabric, this collapsible laundry basket is both practical and eco-friendly. It’s perfect for organizing laundry while being mindful of your environmental footprint.", "image_filename": "productImage5.jpg"},
        {"name": "Silicone Kitchen Utensil Set", "price": 12.99, "discount": 0.15, "description": "This kitchen utensil set is made with 100% recycled silicone, offering heat resistance and durability. It's an environmentally friendly way to upgrade your cooking tools while reducing waste.", "image_filename": "productImage6.jpg"},
        {"name": "Mini Desk Fan", "price": 8.99, "discount": 0.1, "description": "Stay cool with this mini desk fan, crafted from recycled plastic. It’s an efficient and eco-conscious solution for personal cooling while working or studying.", "image_filename": "productImage7.jpg"},
        {"name": "Set of Microfiber Cleaning Cloths", "price": 6.99, "discount": 0.2, "description": "These microfiber cleaning cloths are made from recycled materials, offering superior absorbency for all your cleaning tasks. A reusable, sustainable alternative to paper towels and disposable wipes.", "image_filename": "productImage8.jpg"},
        {"name": "LED Night Light", "price": 4.99, "discount": 0.1, "description": "This LED night light is made from recycled plastic and features an automatic sensor for convenience. It’s energy-efficient and environmentally friendly, providing soft light for your home while minimizing waste.", "image_filename": "productImage9.jpg"},
        {"name": "Foldable Storage Boxes", "price": 8.99, "discount": 0.12, "description": "These foldable storage boxes are made from recycled cardboard, perfect for organizing your home in an eco-friendly way. Their collapsible design allows for easy storage when not in use.", "image_filename": "productImage10.jpg"},
        {"name": "Dish Sponge Holder", "price": 3.99, "discount": 0.1, "description": "This dish sponge holder is crafted from recycled plastic, designed to keep your sponges dry and organized. It’s an eco-friendly addition to your kitchen that helps reduce plastic waste.", "image_filename": "productImage11.jpg"},
        {"name": "Clothes Hangers (Set of 10)", "price": 5.99, "discount": 0.07, "description": "These sturdy clothes hangers are made from recycled wood, providing a sustainable way to organize your wardrobe. A great choice for those looking to reduce their environmental impact while keeping clothes neatly arranged.", "image_filename": "productImage12.jpg"},
        {"name": "Shower Curtain", "price": 8.49, "discount": 0.1, "description": "This shower curtain is made from recycled materials, providing a waterproof and eco-friendly option for your bathroom. It combines sustainability with style for a positive environmental impact.", "image_filename": "productImage13.jpg"}
    ]

    with shelve.open(SHELVE_FILE, writeback=True) as db:
        if not db:  # Only add if the database is empty
            for i, product in enumerate(default_products):
                product_id = str(i + 1)
                db[product_id] = {
                    'id': product_id,
                    'name': product["name"],
                    'price': product["price"],
                    'discount': product["discount"],
                    'discountPercent': round(product["discount"] * 100, 1),
                    'discountedPrice': round(product["price"] * (1 - product["discount"]), 2),
                    'description': product["description"],
                    'image_url': "uploads/" + product["image_filename"] 
                }


@app.route('/productUser', methods=['GET', 'POST'])
def product():
    username = session.get('username')  # Get logged-in user's username
    if not username:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    initialize_default_products()  # Ensure there are at least 12 products

    items_per_page = 12
    page = request.args.get('page', 1, type=int)

    with shelve.open(SHELVE_FILE) as db:
        items = list(db.values())
    with shelve.open(DATABASE) as user_db:
        users = user_db.get('users', {})
        user = users.get(username, {})

    total_items = len(items)
    total_pages = ceil(total_items / items_per_page)

    start = (page - 1) * items_per_page
    end = start + items_per_page
    paginated_items = items[start:end]

    # Handle cart actions (add/remove items)
    if request.method == 'POST':
        item_id = request.form.get('item_id')
        action = request.form.get('action')

        # Modify cart based on action (add/remove)
        if item_id and action and user:
            cart = user.get('cart', {})
            if action == 'add':
                if item_id in cart:
                    cart[item_id]['quantity'] += 1
                else:
                    # Add new item to the cart
                    product = next(item for item in items if item['id'] == item_id)
                    cart[item_id] = {'name': product['name'], 'price': product['price'], 'quantity': 1}
            elif action == 'remove' and item_id in cart:
                if cart[item_id]['quantity'] > 1:
                    cart[item_id]['quantity'] -= 1
                else:
                    del cart[item_id]
            
            # Save updated cart to user data
            with shelve.open(DATABASE, writeback=True) as user_db:
                users[username]['cart'] = cart
                user_db['users'] = users

    return render_template(
        'productUser.html',
        items=paginated_items,
        cart_items=user.get('cart', {}).values(),
        page=page,
        total_pages=total_pages,
        user=user
    )


@app.route('/productAdmin')
def productAdmin():
    initialize_default_products()  # Ensure default products exist

    with shelve.open(SHELVE_FILE) as db:
        items = list(db.values())
    with shelve.open(CART_FILE) as cart_db:
        cart_items = list(cart_db.values())

    return render_template('products.html', items=items, cart_items=cart_items)


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']
    discount = request.form['discount']
    description = request.form['description']
    image = request.files['image']

    try:
        price = float(price)
        if price <= 0:
            raise ValueError("Price must be greater than 0.")
    except ValueError as e:
        return f"Invalid price: {e}", 400
    
    try:
        discount = float(discount)
        if discount < 0 or discount >= 1:  # Ensure discount is between 0 and 1
            raise ValueError("Discount must be between 0 and 1.")
    except ValueError as e:
        return f"Invalid discount: {e}", 400

    if image and image.filename != '':
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_url = f"uploads/{filename}"
    else:
        image_url = None

    with shelve.open(SHELVE_FILE, writeback=True) as db:
        product_id = str(len(db) + 1)
        db[product_id] = {
            'id': product_id,
            'name': name,
            'price': price,
            'discountPercent': (discount*100),
            'discountedPrice': round(price * (1 - discount), 2),
            'description': description,
            'image_url': image_url
        }

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print("Saving image to:", image_path)  # Debug output
    print("Image URL:", url_for('static', filename='uploads/' + image_url))
    print("Final Image URL stored:", image_url)
    print("Expected:", url_for('static', filename='uploads/' + image_url))
    image.save(image_path)
    return redirect(url_for('productAdmin'))


@app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    with shelve.open(SHELVE_FILE) as db:
        db.pop(product_id, None)
    return redirect(url_for('productAdmin'))

@app.route('/add_to_cart/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    username = session.get('username')  # Get logged-in user's username
    if not username:
        return redirect(url_for('login'))  # If not logged in, redirect to login

    with shelve.open(DATABASE, writeback=True) as db:
        users = db.get('users', {})
        user = users.get(username)

        if not user:
            user = {'cart': {}}  # If user doesn't exist, initialize with empty cart
            users[username] = user

        with shelve.open(SHELVE_FILE) as product_db:
            product = product_db.get(product_id)

        if product:
            discounted_price = product.get('discountedPrice', product.get('price', 0))
            if product_id in user['cart']:
                user['cart'][product_id]['quantity'] += 1
            else:
                user['cart'][product_id] = {**product, 'quantity': 1, 'price': discounted_price}

        db['users'] = users  # Save the updated user data

    return redirect(url_for('product'))  # Redirect to product page to display cart


@app.route('/product/<product_id>')
def product_details(product_id):
    with shelve.open(SHELVE_FILE) as db:
        product = db.get(product_id)

    if not product:
        return "Product not found", 404

    return render_template('productDesc.html', product=product)













####################### Cart / Payment ###############################

@app.route('/cart')
def cart():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if the user is not logged in

    with shelve.open(DATABASE) as db:
        users = db.get('users', {})
        user = users.get(username, {})

    cart_items = user.get('cart', {}).values()  # Get items from the user's cart
    
    # Ensure that discounted prices are used in cart display
    for item in cart_items:
        item['price'] = item['price'] * (1 - item.get('discount', 0))  # Apply discount if any

    total_price = sum(float(item['price']) * int(item['quantity']) for item in cart_items)

    return render_template('cart.html', items=cart_items, total_price=total_price)

@app.route('/cart/update', methods=['POST'])
def update_cart():
    username = session.get('username')
    if not username:
        return jsonify({'error': 'User not logged in'}), 400

    data = request.get_json()
    item_id = data.get('item_id')
    action = data.get('action')

    with shelve.open(DATABASE, writeback=True) as db:
        users = db.get('users', {})
        user = users.get(username)
        if user and 'cart' in user:
            cart = user['cart']
            if item_id in cart:
                if action == 'add':
                    cart[item_id]['quantity'] += 1
                elif action == 'remove' and cart[item_id]['quantity'] > 1:
                    cart[item_id]['quantity'] -= 1
                elif action == 'remove' and cart[item_id]['quantity'] == 1:
                    del cart[item_id]
            db['users'] = users

    return jsonify({'cart': user['cart']})  # Return updated cart data to frontend


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))  # Redirect if not logged in

    with shelve.open(DATABASE) as db:
        users = db.get('users', {})
        user = users.get(username, {})
    
    cart_items = user.get('cart', {}).values()  # Pull cart items from user data

    create_payment_form = PaymentForm(request.form)

    if request.method == 'POST' and create_payment_form.validate():
        receipts_dict = {}
        db = shelve.open('receipt.db', 'c')

        try:
            receipts_dict = db['Receipts']
        except KeyError:
            print("Error in retrieving Receipts from receipt.db.")
        
        # Store items in receipt
        purchased_items = [
            {"name": item["name"], "quantity": int(item["quantity"]), "price": float(item["price"])}
            for item in cart_items
        ]

        receipt = Receipts.Receipt(
            create_payment_form.creditcard.data,
            purchased_items  # Pass items into receipt
        )

        receipts_dict[receipt.get_receipt_id()] = receipt
        db['Receipts'] = receipts_dict
        db.close()

        # Clear cart after successful purchase
        with shelve.open(DATABASE, writeback=True) as db:
            users[username]['cart'] = {}
            db['users'] = users

        return redirect(url_for('thankyou'))

    total_price = sum(float(item["price"]) * int(item["quantity"]) for item in cart_items)

    return render_template('Payment.html', items=cart_items, total_price=total_price, form=create_payment_form)



@app.route('/paymentDonation', methods=['GET', 'POST'])
def paymentDonation():
    create_donation_form = DonationForm(request.form)
    if request.method == 'POST' and create_donation_form.validate():
        donations_dict = {}
        db = shelve.open('donation.db', 'c')
        try:
            donations_dict = db['Donations']
        except:
            print("Error in retrieving Donations from donation.db.")
        donation = Donations.Donation(create_donation_form.creditcard.data, create_donation_form.date.data,
                                      create_donation_form.cvv.data, create_donation_form.name.data,
                                      create_donation_form.society.data, create_donation_form.donateamt.data)
        donations_dict[donation.get_donation_id()] = donation
        db['Donations'] = donations_dict

        db.close()

        return redirect(url_for('thankyoudonate'))
    return render_template('Donation.html', form=create_donation_form)


@app.route('/paymentDetails', methods=['GET', 'POST'])
def paymentDetails():
    create_details_form = DetailForm(request.form)
    if request.method == 'POST' and create_details_form.validate():
        details_dict = {}
        db = shelve.open('detail.db', 'c')
        try:
            details_dict = db['Details']
        except:
            print("Error in retrieving Details from details.db.")
        detail = Details.Detail(create_details_form.accountname.data, create_details_form.accountid.data,
                                create_details_form.doc.data, create_details_form.accountemail.data, )
        details_dict[detail.get_detail_id()] = detail
        db['Details'] = details_dict

        db.close()

        return redirect(url_for('cart'))
    return render_template('Details.html', form=create_details_form)


@app.route('/retrieveReceipts')
def retrieve_receipts():
    receipts_dict = {}
    db = shelve.open('receipt.db', 'r')
    receipts_dict = db['Receipts']
    db.close()
    receipts_list = []
    for key in receipts_dict:
        receipt = receipts_dict.get(key)
        receipts_list.append(receipt)
    return render_template('retrieveReceipts.html', count=len(receipts_list), receipts_list=receipts_list)


@app.route('/retrieveDonations')
def retrieve_donations():
    donations_dict = {}
    db = shelve.open('donation.db', 'r')
    donations_dict = db['Donations']
    db.close()
    donations_list = []
    for key in donations_dict:
        donation = donations_dict.get(key)
        donations_list.append(donation)
    return render_template('retrieveDonations.html', count=len(donations_list), donations_list=donations_list)


@app.route('/retrieveDetails')
def retrieve_details():
    details_dict = {}
    db = shelve.open('detail.db', 'r')
    details_dict = db['Details']
    db.close()
    details_list = []
    for key in details_dict:
        detail = details_dict.get(key)
        details_list.append(detail)
    return render_template('retrieveDetails.html', count=len(details_list), details_list=details_list)


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/thankyoudonate")
def thankyoudonate():
    return render_template("thankyoudonate.html")


@app.route('/deleteReceipt/<int:id>', methods=['POST'])
def delete_receipt(id):
    receipts_dict = {}
    db = shelve.open('receipt.db', 'w')
    receipts_dict = db['Receipts']
    receipts_dict.pop(id)
    db['Receipts'] = receipts_dict
    db.close()
    return redirect(url_for('retrieve_receipts'))


@app.route('/deleteDonation/<int:id>', methods=['POST'])
def delete_donation(id):
    donations_dict = {}
    db = shelve.open('donation.db', 'w')
    donations_dict = db['Donations']
    donations_dict.pop(id)
    db['Donations'] = donations_dict
    db.close()
    return redirect(url_for('retrieve_donations'))


@app.route('/deleteDetail/<int:id>', methods=['POST'])
def delete_detail(id):
    details_dict = {}
    db = shelve.open('detail.db', 'w')
    details_dict = db['Details']
    details_dict.pop(id)
    db['Details'] = details_dict
    db.close()
    return redirect(url_for('retrieve_details'))


@app.route('/updateDetails/<int:id>/', methods=['GET', 'POST'])
def update_details(id):
    update_detail_form = DetailForm(request.form)
    if request.method == 'POST' and update_detail_form.validate():
        db = shelve.open('detail.db', 'w')
        details_dict = db['Details']
        detail = details_dict.get(id)
        detail.set_accountname(update_detail_form.accountname.data)
        detail.set_accountid(update_detail_form.accountid.data)
        detail.set_doc(update_detail_form.doc.data)
        detail.set_accountemail(update_detail_form.accountemail.data)
        db['Details'] = details_dict
        db.close()
        return redirect(url_for('retrieve_details'))
    else:
        db = shelve.open('detail.db', 'r')
        details_dict = db['Details']
        db.close()
        detail = details_dict.get(id)
        update_detail_form.accountname.data = detail.get_accountname()
        update_detail_form.accountid.data = detail.get_accountid()
        update_detail_form.doc.data = detail.get_doc()
        update_detail_form.accountemail.data = detail.get_accountemail()
        return render_template('updateDetails.html', form=update_detail_form)


@app.route("/Donation", methods=["GET", "POST"])
def Donation():
    form = DonationForm(request.form)
    if request.method == "POST" and form.validate():
        return redirect(url_for('thankyou'))
    return render_template("Donation.html", form=form)

@app.route('/Collab1')
def Collab1():
    return render_template('Collab1.html')

@app.route('/Collab2')
def Collab2():
    return render_template('Collab2.html')

@app.route('/Collab3')
def Collab3():
    return render_template('Collab3.html')

@app.route('/Collab4')
def Collab4():
    return render_template('Collab4.html')

@app.route('/Collab5')
def Collab5():
    return render_template('Collab5.html')

@app.route('/Collab6')
def Collab6():
    return render_template('Collab6.html')

@app.route('/Collab7')
def Collab7():
    return render_template('Collab7.html')

@app.route('/Collab8')
def Collab8():
    return render_template('Collab8.html')

@app.route('/Collab9')
def Collab9():
    return render_template('Collab9.html')


############################ Subscription ##################################

prizes = ["$10 Gift Card", "$5 Discount", "Eco-Friendly NoteBook", "Water Bottle", "Try Again Next Time", "$20 Voucher", "Workshop Voucher", "Grand Prize", "Bamboo Utensil Sets", "A Tote Bag"]


@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html')

@app.route('/afterUpdate')
def afterUpdate():
    return render_template('afterUpdate.html')

@app.route('/subscription')
def subHome():
    return render_template('subHome.html')

@app.route('/afterSub')  # Ensure this matches the name used in url_for
def afterSub():
    return render_template('afterSub.html')

@app.route('/subHome', methods=['GET', 'POST'])
def game():
    selected_prize = None
    if request.method == 'POST':
        selected_prize = random.choice(prizes)
        return jsonify({'prize': selected_prize})
    return render_template('subHome.html', prizes=prizes)

@app.route('/createSub', methods=['GET', 'POST'])
def create_sub():
    create_sub_form = CreateSubForm(request.form)
    if request.method == 'POST' and create_sub_form.validate():
        subs_dict = {}
        db = shelve.open('sub.db', 'c')

        try:
            subs_dict = db['Subs']
        except:
            print("Error in retrieving Users from user.db.")

        sub = Sub.Sub(create_sub_form.first_name.data, create_sub_form.last_name.data, create_sub_form.gender.data,
                      create_sub_form.email.data, create_sub_form.remarks.data)
        subs_dict[sub.get_sub_id()] = sub
        db['Subs'] = subs_dict

        db.close()

        return redirect(url_for('afterSub'))
    return render_template('createSub.html', form=create_sub_form)


@app.route('/OurSubs')
def OurSubs():
    subs_dict = {}
    db = shelve.open('sub.db', 'r')
    subs_dict = db['Subs']
    db.close()

    subs_list = []
    for key in subs_dict:
        sub = subs_dict.get(key)
        subs_list.append(sub)

    return render_template('OurSubs.html', count=len(subs_list), subs_list=subs_list)


@app.route('/updateSub/<int:id>/', methods=['GET', 'POST'])
def update_sub(id):
    update_sub_form = CreateSubForm(request.form)
    if request.method == 'POST' and update_sub_form.validate():
        subs_dict = {}
        db = shelve.open('sub.db', 'w')
        subs_dict = db['Subs']

        sub = subs_dict.get(id)
        sub.set_first_name(update_sub_form.first_name.data)
        sub.set_last_name(update_sub_form.last_name.data)
        sub.set_gender(update_sub_form.gender.data)
        sub.set_email(update_sub_form.email.data)
        sub.set_remarks(update_sub_form.remarks.data)

        db['Subs'] = subs_dict
        db.close()

        return redirect(url_for('afterUpdate'))
    else:
        subs_dict = {}
        db = shelve.open('sub.db', 'r')
        subs_dict = db['Subs']
        db.close()

        sub = subs_dict.get(id)
        if sub:
            update_sub_form.first_name.data = sub.get_first_name()
            update_sub_form.last_name.data = sub.get_last_name()
            update_sub_form.gender.data = sub.get_gender()
            update_sub_form.email.data = sub.get_email()
            update_sub_form.remarks.data = sub.get_remarks()
        else:
            flash('Subscription not found.', 'error')
            return redirect(url_for('chooseSub'))


        return render_template('updateSub.html', form=update_sub_form)


@app.route('/deleteSub/<int:id>', methods=['POST'])
def delete_sub(id):
    subs_dict = {}
    db = shelve.open('sub.db', 'w')
    subs_dict = db['Subs']

    subs_dict.pop(id)

    db['Subs'] = subs_dict
    db.close()

    return redirect(url_for('OurSubs'))

@app.route('/chooseSub', methods=['GET', 'POST'])
def chooseSub():
    class EmailForm(Form):
        email = EmailField('Email', [validators.Email(), validators.DataRequired()])

    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data

        db = shelve.open('sub.db', 'r')
        subs_dict = db.get('Subs', {})
        db.close()

        for sub_id, sub in subs_dict.items():
            if sub.get_email() == email:
                return redirect(url_for('update_sub', id=sub_id))

        flash('Email not found. Please check your email or subscribe first.', 'error')
        return redirect(url_for('chooseSub'))

    return render_template('chooseSub.html', form=form)














############################### Points ###################################

def get_items():
    with shelve.open("rewards.db") as db:
        items = db.get("items", {})
    print(f"DEBUG: Available items = {items}")
    print(f"DEBUG: Item names in DB = {list(items.keys())}")  # List all item names
    return items


def save_items(items):
    with shelve.open("rewards.db", writeback=True) as db:
        db["items"] = items


@app.route("/profile", methods=["GET", "POST"])
def index():
    # Get the user's session name
    name = session.get("username", "Guest")

    # Handle points update if the form is submitted
    if request.method == "POST":
        points = request.form.get("points")
        if points and points.isdigit():
            with shelve.open("user_data.db", writeback=True) as db:
                # Fetch user data from the database or create an empty template if user doesn't exist
                user_data = db.get(name, {"cumulative_points": 0, "spendable_points": 0, "redeemed_items": []})

                # Add the points
                user_data["cumulative_points"] += int(points)
                user_data["spendable_points"] += int(points)

                # Update the user data in the database (keeping other data intact)
                db[name] = user_data

            return redirect(url_for("index"))

    # Fetch user data from the database
    with shelve.open("user_data.db") as db:
        user_data = db.get(name, {"cumulative_points": 0, "spendable_points": 0, "redeemed_items": []})
        cumulative_points = user_data.get("cumulative_points", 0)
        spendable_points = user_data.get("spendable_points", 0)
        redeemed_items = user_data.get("redeemed_items", [])

    # Calculate points progress
    percentage = min((cumulative_points / MAX_POINTS) * 100, 100)
    points_left = max(MAX_POINTS - cumulative_points, 0)

    print(f"DEBUG: Saving user data for {name}: {user_data}")

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
    name = session.get("name", "Guest")  # Get the session name, default to "Guest" if not set
    return render_template("points.html", name=name)  # Pass the name to the template


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


if __name__ == '__main__':
    initialize_default_products()
    app.run(debug=True)
import csv
import io
import re
from xhtml2pdf import pisa
from io import BytesIO
from sqlalchemy import func, text
import json
from time import sleep
from flask import make_response
from datetime import datetime
from flask import Flask,render_template,request,session,url_for,redirect,flash,get_flashed_messages,abort
from flask import Flask
from email_validator import validate_email, EmailNotValidError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, URL, Optional, Email, ValidationError, Length
from wtforms import PasswordField, EmailField, TextAreaField, SelectField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

load_dotenv()

#Admin Only Decorator Function
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If user is not logged in OR user is not ID #1
        if not current_user.is_authenticated or current_user.id != 1:
            # Return 403 (Forbidden)
            return abort(403)
        # Otherwise, let them in
        return f(*args, **kwargs)
    return decorated_function

# Expanded list of common burner domains
DISPOSABLE_DOMAINS = {
    'mailinator.com', 'yopmail.com', 'temp-mail.org', '10minutemail.com', 
    'guerrillamail.com', 'sharklasers.com', 'throwawaymail.com', 
    'getnada.com', 'dispostable.com', 'fake-email.com', 'tempr.email',
    'maildrop.cc', 'trashmail.com', 'mytemp.email', '7tags.com',
    'e4ward.com', 'guerillamail.net', 'spam4.me', 'spambox.us',
    'tempmail.com', 'anonbox.net', 'boximail.com', 'clrmail.com',
    'inbox.testmail.app', 'tmail.ws', 'moakt.com', 'temp-mail.ru'
}

ALLOWED_PROVIDERS = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com', 'protonmail.com'}

#Forms
class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('5', '⭐⭐⭐⭐⭐ (Excellent)'), 
                                            ('4', '⭐⭐⭐⭐ (Good)'), 
                                            ('3', '⭐⭐⭐ (Average)'), 
                                            ('2', '⭐⭐ (Poor)'), 
                                            ('1', '⭐ (Terrible)')], 
                         validators=[DataRequired()])
    text = TextAreaField('Your Review', validators=[DataRequired()])
    submit = SubmitField('Submit Review')

class CouponForm(FlaskForm):
    code = StringField('Code (e.g. SUMMER20)', validators=[DataRequired()])
    discount = IntegerField('Discount % (e.g. 20)', validators=[DataRequired()])
    submit = SubmitField('Create Coupon')

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired(),Length(min=8, message="Password must be at least 8 characters long.")])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")

    def validate_email(self, field):
        email_input = field.data

        # EXTRACT DOMAIN
        domain = field.data.split('@')[1].lower()

        if domain.lower() in DISPOSABLE_DOMAINS:
            raise ValidationError("Temp mail is not allowed.")
        
        # STRICT CHECK: If it's not on the list, kick them out.
        if domain not in ALLOWED_PROVIDERS:
            raise ValidationError("Sorry, we currently only accept Gmail, Outlook, Yahoo, iCloud, and ProtonMail.")
    
    def validate_password(self, field):
        password = field.data

        # Check for at least one Uppercase letter
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        
        # Check for at least one Lowercase letter
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        
        # Check for at least one Number
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one number.")
        
        # Check for at least one Symbol (Special Character)
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one symbol (!@#$%).")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")

class AddProductForm(FlaskForm):
    title = StringField('Product Name', validators=[DataRequired()])
    # Note: User enters dollars (e.g., 10.50), we will convert to cents later
    price = FloatField('Price (e.g., 10.99)', validators=[DataRequired()]) 
    description = StringField('Description', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[URL(),Optional()])
    image_file = FileField('OR Upload Image', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!'),
        Optional()
    ])
    submit = SubmitField('Add Product')

class UpdateProfileForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    # Optional() means they can leave it blank if they don't want to change it
    password = PasswordField("New Password (Optional)", validators=[Optional()]) 
    submit = SubmitField("Update Profile")

cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRETS')
)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app=Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY",'8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URI","sqlite:///Product.db")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

mail = Mail(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


wishlist_table = db.Table('wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

#Database
class Product(db.Model):
    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(250))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(500))
    image_url: Mapped[str] = mapped_column(String(250))
    reviews = db.relationship('Review', backref='product', cascade="all, delete")

    images = db.relationship('ProductImage', backref='product', lazy=True)
    def get_rating(self):
        if not self.reviews:
            return 0
        total_stars = sum([review.rating for review in self.reviews])
        return round(total_stars / len(self.reviews), 1)
    
    def get_watermarked_image(self):
        if not self.image_url or "cloudinary" not in self.image_url:
            return self.image_url
        
        try:
            if "/upload/" not in self.image_url:
                return self.image_url
                
            parts = self.image_url.split("/upload/", 1)
            transformation = "w_800/l_text:Arial_50_bold:FAKE%20SHOP,co_rgb:FFFFFF,o_40,g_south_east,x_20,y_20/"
            return f"{parts[0]}/upload/{transformation}{parts[1]}"
        except:
            return self.image_url  # Fallback to original

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True) # New
    password = db.Column(db.String(100))

    is_deleted = db.Column(db.Boolean, default=False)

    # Relationship: One User has Many Orders
    orders = db.relationship('Order', backref='customer')
    reviews = db.relationship('Review', backref='author')

    wishlist = db.relationship('Product', secondary=wishlist_table, backref='wished_by')

class SearchTerm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(100)) # e.g., "iphone"
    count = db.Column(db.Integer, default=1) # How many times searched?
    last_searched = db.Column(db.String(20)) # Timestamp

class Coupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)
    discount = db.Column(db.Integer, nullable=False) # e.g., 10 for 10%
    active = db.Column(db.Boolean, default=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key: Links to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String(20)) # Storing simple string for now (e.g., "2025-01-05")
    total_price = db.Column(db.Integer) # Stored in Cents
    # Default status is 'Pending' when created
    status = db.Column(db.String(50), default="Pending")
    # Relationship: One Order has Many Items
    items = db.relationship('OrderItem', backref='order')

    discount_amount = db.Column(db.Integer, default=0)


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Keys: Links to Order AND Product
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    
    quantity = db.Column(db.Integer)
    price_at_purchase = db.Column(db.Integer) # CRITICAL: Snapshot the price!

    product = db.relationship('Product')
    # price = db.Column(db.Integer)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer) # 1 to 5 stars
    text = db.Column(db.String(1000))
    
    # Foreign Keys
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Optional: Timestamp (Good for sorting)
    date_posted = db.Column(db.String(20)) # e.g. "2025-01-06"



# with app.app_context():
#     db.create_all()

def send_reset_email(user):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    # Token expires in 1800 seconds (30 minutes)
    token = s.dumps(user.email, salt='password-reset-salt')
    
    link = url_for('reset_token', token=token, _external=True)
    
    msg = Message('Password Reset Request', 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    
    msg.body = f'''To reset your password, visit the following link:
{link}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

def send_order_confirmation_email_messege(user, order):
    msg = Message(f'Order Confirmation - #{order.id}', 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    
    # 1. Build the receipt text
    # We loop through the order items to list them
    items_list = ""
    for item in order.items:
        items_list += f"- {item.product.title}: ${'%.2f' % (item.product.price / 100)} x {item.quantity}\n"
        
    msg.body = f'''Hello {user.name},

Thank you for your order! Here is your receipt:

Order ID: {order.id}
--------------------------------------
{items_list}
--------------------------------------
Total Paid: ${'%.2f' % (order.total_price / 100)}

Your items will be shipped shortly.
Thank you for shopping with The Fake Shop!
'''
    # 2. Send it (Async is better, but this works for now)
    mail.send(msg)

def send_order_confirmation_email_pdf(user, order):
    # 1. Setup the Email
    msg = Message(f'Invoice - Order #{order.id}', 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    
    msg.body = f"Hello {user.name},\n\nThank you for your purchase. Please find your invoice attached.\n\nBest,\nThe Fake Shop Team"

    # 2. Generate PDF from HTML
    # We render the HTML template with the order data
    html_content = render_template('invoice.html', order=order, user=user)
    
    # We create a memory buffer to hold the PDF data (instead of saving a file to disk)
    pdf_buffer = BytesIO()
    
    # Convert HTML -> PDF
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)
    
    # 3. Attach PDF if generation succeeded
    # if not pisa_status.err:
    #     print(f"⚠️ PDF GENERATION ERROR: {pisa_status.err}")
        # Go back to the start of the file in memory
    pdf_buffer.seek(0)
        
        # Attach it: (Filename, MimeType, Data)
    msg.attach(f"Invoice_{order.id}.pdf", "application/pdf", pdf_buffer.read())
        
    mail.send(msg)


def send_shipped_email(user, order):
    msg = Message(f'Your Order #{order.id} has Shipped!', 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    
    msg.body = f'''Hello {user.name},

Great news! Your order has been processed and is on its way to you.

Order ID: {order.id}
Status: SHIPPED
Date Shipped: {datetime.now().strftime('%Y-%m-%d')}

You will receive your items shortly.
Thank you for shopping with The Fake Shop!
'''
    mail.send(msg)

def send_cancel_email(user, order_id, total_price):
    msg = Message(f'Order #{order_id} Cancelled', 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[user.email])
    
    msg.body = f'''Hello {user.name},

Your order has been cancelled as requested.

Order ID: {order_id}
Refund Amount: ${'%.2f' % (total_price / 100)}

The refund will be processed within 3-5 business days.
Thank you for shopping with The Fake Shop!
'''
    mail.send(msg)

def send_admin_alert(order):
    # 1. Get the Admin User (ID #1)
    admin = db.session.get(User, 1)
    
    msg = Message(f'💰 NEW ORDER: #{order.id} - ${"%.2f" % (order.total_price / 100)}', 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[admin.email]) # Sends to YOU
    
    msg.body = f'''You just made a sale!
    
Order ID: {order.id}
Customer: {order.customer.name} ({order.customer.email})
Total: ${"%.2f" % (order.total_price / 100)}
Date: {order.date}

Items:
'''
    for item in order.items:
        msg.body += f"- {item.product.title} (x{item.quantity})\n"
        
    msg.body += "\nLogin to your dashboard to ship this order."
    
    mail.send(msg)

# This runs before EVERY template is rendered
@app.context_processor
def inject_pending_orders():
    pending_count = 0
    # Only check DB if user is logged in and is the Admin
    if current_user.is_authenticated and current_user.id == 1:
        # Count orders where status is NOT 'Shipped' and NOT 'Cancelled'
        pending_count = db.session.query(Order).filter(
            Order.status == 'Pending'
        ).count()
    
    # This variable 'pending_orders_count' is now available in ALL html files
    return dict(pending_orders_count=pending_count)

#HomePage
@app.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    sort_option = request.args.get('sort', '')
    per_page = 12
    
    # --- NEW: THE SPY LOGIC ---
    if search_query:
        # 1. Clean the input (Lowercase to match "Shoe" with "shoe")
        clean_term = search_query.strip().lower()
        
        if clean_term:
            # 2. Check if term exists
            # We use a separate DB session query to check existence
            existing_term = db.session.execute(db.select(SearchTerm).where(SearchTerm.term == clean_term)).scalar()
            
            if existing_term:
                existing_term.count += 1
                existing_term.last_searched = datetime.now().strftime('%Y-%m-%d')
            else:
                new_term = SearchTerm(term=clean_term, last_searched=datetime.now().strftime('%Y-%m-%d'))
                db.session.add(new_term)
                
            # 3. Commit (Save silently without slowing down the user)
            db.session.commit()
    
    if search_query:
        stmt = db.select(Product).where(Product.title.like(f'%{search_query}%'))
    else:
        stmt = db.select(Product)
    
    if sort_option == 'price_low':
        stmt = stmt.order_by(Product.price.asc())
    elif sort_option == 'price_high':
        stmt = stmt.order_by(Product.price.desc())
    elif sort_option == 'newest':
        stmt = stmt.order_by(Product.id.desc())
    elif sort_option == 'oldest':
        stmt = stmt.order_by(Product.id.asc())
    else:
        stmt = stmt.order_by(Product.title)
    
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    return render_template("index.html", pagination=pagination, current_sort=sort_option, search_query=search_query)

# @app.route('/add_deleted_flag')
# def add_deleted_flag():
#     try:
#         # Add the column with a default of 0 (False)
#         db.session.execute(text("ALTER TABLE user ADD COLUMN is_deleted BOOLEAN DEFAULT 0"))
#         db.session.commit()
#         return "Database updated! You can delete this route now."
#     except Exception as e:
#         return f"Error (Column might already exist): {e}"

# @app.route('/init_coupons')
# def init_coupons():
#     try:
#         # 1. Create Coupon Table
#         db.create_all()
        
#         # 2. Add column to existing Order table
#         db.session.execute(text("ALTER TABLE 'order' ADD COLUMN discount_amount INTEGER DEFAULT 0"))
        
#         # 3. Create a test coupon
#         if not Coupon.query.filter_by(code="SAVE20").first():
#             db.session.add(Coupon(code="SAVE20", discount=20))
            
#         db.session.commit()
#         return "Coupons system initialized! 'SAVE20' is now valid."
#     except Exception as e:
#         return f"Database updated (or column already existed): {e}"


@app.route('/delete_account')
@login_required
def delete_account():
    # 1. Soft Delete: Mark them as deleted
    current_user.is_deleted = True
    
    db.session.commit()
    
    # 2. Log them out immediately
    logout_user()
    
    flash("Your account has been deleted. We are sorry to see you go.", "info")
    return redirect(url_for('home'))

#RegistrationPage
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        
        # Check if user already exists
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        
        if user:
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        # HASHING THE PASSWORD (SALTING)
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Log them in immediately
        login_user(new_user)
        
        return redirect(url_for('home'))
        
    return render_template("register.html", form=form)

#LoginPage
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        # Find user by email
        result = db.session.execute(db.select(User).where(User.email == email))
        user = result.scalar()
        
        # Check stored hash against entered password
        if not user:
            flash("That email does not exist, please try again.","warning")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.',"warning")
            return redirect(url_for('login'))
        elif user.is_deleted:
            flash("This account has been deleted. Contact support to restore it.", "danger")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
            
    return render_template("login.html", form=form)


#Add_product page only for admin
@app.route('/add_product', methods=['GET', 'POST'])
@admin_only
def add_product():
    form = AddProductForm()
    
    if form.validate_on_submit():
        # 1. Convert Price to Cents (Handling the math)
        price_in_cents = int(float(form.price.data) * 100)
        final_url=None
        if form.image_file.data:
            upload_result = cloudinary.uploader.upload(form.image_file.data)
            final_url = upload_result.get('secure_url')
            
        # PRIORITY 2: Did they paste a URL?
        elif form.image_url.data:
            final_url = form.image_url.data

        # SAFETY CHECK: Did they do neither?
        if not final_url:
            flash("You must provide either an Image File OR an Image URL!","warning")
            return render_template('add_product.html', form=form)
        # 2. Create the new Product
        new_product = Product(
            title=form.title.data,
            price=price_in_cents,
            description=form.description.data,
            image_url=final_url
            # We are defaulting stock to Infinite for now
        )
        
        # 3. Save to DB
        db.session.add(new_product)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('add_product.html', form=form)

#For admin only
@app.route('/admin/orders')
@admin_only  
def admin_orders():
    # Fetch all orders, sorted by newest first (reverse ID order)
    all_orders = db.session.execute(db.select(Order).order_by(Order.id.desc())).scalars().all()
    return render_template('admin_orders.html', orders=all_orders)

#For admin to manage order
@app.route('/admin/ship-order/<int:order_id>')
@admin_only
def ship_order(order_id):
    order = db.get_or_404(Order, order_id)
    
    if order:
        if order.status == 'Cancelled':
            flash(f"Cannot ship Order #{order.id} because it was cancelled by the user.", "danger")
            return redirect(url_for('admin_orders'))
        
        order.status = "Shipped" # Change the status
        db.session.commit()
        # flash(f"Order #{order.id} has been marked as Shipped!")
        if order.customer:
            try:
                send_shipped_email(order.customer, order)
                flash(f"Order #{order.id} marked as Shipped and email sent to {order.customer.email}.", "success")
            except Exception as e:
                flash(f"Order marked as Shipped, but email failed: {e}", "warning")
        else:
            flash(f"Order #{order.id} marked as Shipped (Customer user is deleted, no email sent).", "warning")
        
    else:
        flash("Order not found.", "danger")
        
    return redirect(url_for('admin_orders'))

@app.route('/wishlist/toggle/<int:product_id>')
@login_required
def toggle_wishlist(product_id):
    product = db.session.get(Product, product_id)
    
    if not product:
        return redirect(url_for('home'))

    # If already in wishlist, remove it. If not, add it.
    if product in current_user.wishlist:
        current_user.wishlist.remove(product)
        flash(f"Removed {product.title} from wishlist.", "info")
        db.session.commit()
        return redirect(url_for('my_wishlist'))
    else:
        current_user.wishlist.append(product)
        flash(f"Added {product.title} to wishlist!", "success")
        db.session.commit()
        return redirect(url_for('home') or request.referrer)

@app.route('/wishlist')
@login_required
def my_wishlist():
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    wishlist_ids = [product.id for product in current_user.wishlist]
    stmt = db.select(Product).where(Product.id.in_(wishlist_ids))
    
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)
    return render_template("index.html", pagination=pagination, current_sort='', search_query='')

@app.route('/admin/dashboard')
@admin_only
def admin_dashboard():
    # 1. KPI: Total Revenue (Sum of all orders)
    # scalar() gets a single number instead of a list
    total_revenue_cents = db.session.query(func.sum(Order.total_price)).filter(Order.status != 'Cancelled').scalar() or 0
    total_revenue = total_revenue_cents / 100
    
    # 2. KPI: Total Orders (Count valid orders)
    total_orders = Order.query.filter(Order.status != 'Cancelled').count()
    
    # 3. KPI: Average Order Value (AOV)
    avg_order_value = (total_revenue / total_orders) if total_orders > 0 else 0
    
    # 4. CHART DATA: Revenue over Time
    # We group by 'date' and sum the total_price for that day
    daily_sales = db.session.query(
        Order.date, func.sum(Order.total_price)
    ).filter(Order.status != 'Cancelled').group_by(Order.date).order_by(Order.date.asc()).all()
    
    # Separate into two lists for the Chart (X-axis and Y-axis)
    dates = []
    sales = []
    
    for day in daily_sales:
        dates.append(day[0])          # e.g., "2026-01-08"
        sales.append(day[1] / 100)    # e.g., 150.00
    
    top_searches = db.session.execute(
        db.select(SearchTerm).order_by(SearchTerm.count.desc()).limit(5)
    ).scalars().all()

    # We use json.dumps to turn Python lists into JavaScript Arrays
    return render_template('admin_dashboard.html', 
                           revenue=total_revenue, 
                           orders=total_orders, 
                           avg_order=avg_order_value,
                           dates=json.dumps(dates),
                           sales=json.dumps(sales),
                           top_searches=top_searches)

# Customer order page
@app.route('/my-orders')
@login_required
def my_orders():
    # Only show orders for the CURRENT user
    orders = current_user.orders 
    return render_template('my_orders.html', orders=orders)

#Seeing product detail
@app.route('/product/<int:product_id>',methods=["GET","POST"])
def product_detail(product_id):
    # Fetch the single product
    product = db.get_or_404(Product, product_id)
    
    # Safety check: If ID doesn't exist, go home
    if not product:
        return redirect(url_for('home'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login to leave a review!")
            return redirect(url_for('login'))
            
        new_review = Review(
            rating=int(form.rating.data),
            text=form.text.data,
            product_id=product.id,
            user_id=current_user.id,
            date_posted=datetime.now().strftime("%Y-%m-%d")
        )
        
        db.session.add(new_review)
        db.session.commit()
        flash("Review added successfully!","success")
        return redirect(url_for('product_detail', product_id=product.id))
    return render_template('product_detail.html', product=product,form=form)

#Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#Edit product for admin only
@app.route('/edit-product/<int:product_id>', methods=["GET", "POST"])
@admin_only
def edit_product(product_id):
    product = db.get_or_404(Product, product_id)
    
    # If using the same form class, we populate it with the object data
    form = AddProductForm(obj=product)
    
    if form.validate_on_submit():
        # 1. Update the fields
        product.title = form.title.data
        product.description = form.description.data

        if form.image_file.data:
            # Case A: They uploaded a new file
            upload_result = cloudinary.uploader.upload(form.image_file.data)
            product.image_url = upload_result.get('secure_url')
        elif form.image_url.data and form.image_url.data != product.image_url:
            # Case B: They pasted a new URL
            product.image_url = form.image_url.data
        
        # 2. Handle Price Conversion (Dollars -> Cents)
        product.price = int(float(form.price.data) * 100)
        
        # 3. Commit
        db.session.commit()
        return redirect(url_for('home'))

    # --- PRE-POPULATION LOGIC (For GET Request) ---
    # We manually set the price because the DB has cents (1000), 
    # but the form needs dollars (10.00).
    form.price.data = product.price / 100
    form.submit.label.text="Edit Product"
    # We pass 'is_edit=True' so the template knows to change the title
    return render_template('add_product.html', form=form, is_edit=True)

#Add something to the cart
@app.route("/add/<int:product_id>")
@login_required
def add_to_cart(product_id): # Accept the ID as an argument
    if "cart" not in session:
        session["cart"] = {}
    
    cart = session["cart"]
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    session["cart"] = cart
    
    return redirect(url_for('home'))

#Go to cart
@app.route("/cart")
@login_required
def view_cart():
    cart=session.get('cart',{})
    cart_items=[]
    grand_total=0

    if cart:
        product_ids = [int(key) for key in cart.keys() if key and key.isdigit()]
        products=Product.query.filter(Product.id.in_(product_ids)).all()

        for product in products:
            quantity=cart[str(product.id)]
            subtotal=product.price*quantity
            grand_total+=subtotal

            cart_items.append({
                'id':product.id,
                'title':product.title,
                'price':product.price,
                'quantity':quantity,
                'subtotal':subtotal
            })
    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total)

#Delete product for admin only
@app.route('/delete-product/<int:product_id>')
@admin_only
def delete_product(product_id):
    # 1. Find the product
    product_to_delete = db.get_or_404(Product, product_id)
    
    # 2. If it exists, delete it
    if product_to_delete:
        try:
            db.session.delete(product_to_delete)
            db.session.commit()
            flash("Product Deleted Successfully","success")
        except Exception as e:
            # This happens if the product is already linked to an Order
            flash(f"Error deleting product: {e}","error")
            # Optional: You could flash a message here saying "Cannot delete sold items!"
            
    return redirect(url_for('home'))

@app.route('/apply_coupon', methods=['POST'])
@login_required
def apply_coupon():
    code = request.form.get('code')
    
    # 1. Look up the coupon (Case Insensitive)
    coupon = Coupon.query.filter(func.lower(Coupon.code) == func.lower(code)).first()
    
    if coupon and coupon.active:
        # 2. Save to Session (The "Backpack")
        session['coupon_code'] = coupon.code
        session['coupon_percent'] = coupon.discount
        flash(f"Success! {coupon.discount}% discount applied.", "success")
    else:
        flash("Invalid or expired coupon code.", "danger")
        
    return redirect(url_for('view_cart'))

# --- ADMIN COUPON MANAGER ---

@app.route('/admin/coupons', methods=['GET', 'POST'])
@admin_only
def admin_coupons():
    form = CouponForm()
    
    # 1. Handle New Coupon Creation
    if form.validate_on_submit():
        # Check if code already exists
        existing = Coupon.query.filter_by(code=form.code.data.upper()).first()
        if existing:
            flash(f"Code '{existing.code}' already exists!", "warning")
        else:
            new_coupon = Coupon(
                code=form.code.data.upper(), # Always uppercase
                discount=form.discount.data
            )
            db.session.add(new_coupon)
            db.session.commit()
            flash(f"Coupon {new_coupon.code} created successfully!", "success")
        return redirect(url_for('admin_coupons'))

    # 2. Show Existing Coupons
    coupons = Coupon.query.all()
    return render_template('admin_coupons.html', form=form, coupons=coupons)

@app.route('/admin/delete-coupon/<int:coupon_id>')
@admin_only
def delete_coupon(coupon_id):
    coupon = db.session.get(Coupon, coupon_id)
    if coupon:
        db.session.delete(coupon)
        db.session.commit()
        flash("Coupon deleted.", "info")
    return redirect(url_for('admin_coupons'))

#Proceed to checkout
@app.route('/checkout')
@login_required
def checkout():
    # 1. Get the cart
    cart = session.get('cart', {})
    if not cart:
        return "Cart is empty", 400
    
    raw_total = 0
    # (Do your loop to calculate raw_total first, but DON'T save items yet)
    # NOTE: You already have a loop in your code. We just need the number first.
    temp_items = []
    for p_id, qty in cart.items():
        if p_id and p_id.isdigit():
            prod = db.session.get(Product, int(p_id))
            if prod:
                raw_total += (prod.price * qty)
                temp_items.append({'product': prod, 'qty': qty})
    # --- 2. Apply Discount ---
    discount_percent = session.get('coupon_percent', 0)
    discount_amount = 0
    
    if discount_percent > 0:
        # Math: (Total * Percent) / 100
        discount_amount = int(raw_total * (discount_percent / 100))
    
    final_total = raw_total - discount_amount

    # 2. Create the Order Record (Hardcoded to User #1 for now)
    new_order = Order(user_id=current_user.id, date=datetime.now().strftime("%Y-%m-%d"), total_price=final_total,discount_amount=discount_amount)

    db.session.add(new_order)
    db.session.commit()

    for item in temp_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item['product'].id,
            quantity=item['qty'],
            price_at_purchase=item['product'].price
        )
        db.session.add(order_item)
    # We must add the order to the session to generate an ID
    db.session.commit() # Now new_order.id exists!
    session.pop('cart', None)
    session.pop('coupon_code', None)     # <--- RESET
    session.pop('coupon_percent', None)
    flash(f'Order placed! You saved ${"%.2f" % (discount_amount/100)}.', 'success')
    try:
        send_order_confirmation_email_messege(current_user,new_order)
        send_admin_alert(new_order)
        flash("Messege has been sent successfully","success")
    except:
        flash(f"Email failed to send: {e}","warning")

    sleep(10)
    try:
        send_order_confirmation_email_pdf(current_user, new_order)
        flash("PDF Invoice has been sent successfully","success")
    except Exception as e:
        # Don't crash the app if email fails (e.g., wifi blip)
        flash(f"Pdf Invoice failed to send: {e}","warning")

    # 5. CLEAR THE CART (The Backpack is empty)
    # session.pop('cart',None)
    flash('Order placed successfully! Check your email for the receipt.', 'success')
    return render_template('success.html', order_id=new_order.id)

@app.route("/product/<int:product_id>/add_image", methods=["POST"])
@admin_only
def add_product_image(product_id):
    product = db.get_or_404(Product, product_id)
    
    if not product:
        flash("Product not found", "danger")
        return redirect(url_for('home'))

    # 1. CHECK FOR FILE
    file = request.files.get('file')
    
    if file and file.filename != "":
        try:
            # 2. UPLOAD TO CLOUDINARY (Same logic as add_product)
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result['secure_url']
            
            # 3. SAVE URL TO DB
            new_image = ProductImage(image_url=image_url, product=product)
            db.session.add(new_image)
            db.session.commit()
            flash("Extra image uploaded successfully!", "success")
            
        except Exception as e:
            flash(f"Upload failed: {e}", "danger")
    else:
        flash("No file selected.", "warning")
    
    return redirect(url_for('product_detail', product_id=product.id))

@app.route("/delete_image/<int:image_id>")
@admin_only
def delete_product_image(image_id):
    img = db.get_or_404(ProductImage, image_id)
    if img:
        product_id = img.product_id
        db.session.delete(img)
        db.session.commit()
        flash("Image removed.", "info")
        return redirect(url_for('product_detail', product_id=product_id))
    return redirect(url_for('home'))

#Remove an item from cart
@app.route('/remove/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    # 1. Get the cart
    cart = session.get('cart', {})
    
    # 2. Convert ID to string (because JSON keys are strings)
    product_id_str = str(product_id)
    
    # 3. Check if it exists, then remove it
    # .pop(key, None) removes the key if it exists, and does nothing if it doesn't.
    # It prevents the app from crashing if the user clicks remove twice.
    cart.pop(product_id_str, None)
    
    # 4. Save the update back to the session
    session['cart'] = cart
    
    # 5. Refresh the cart page
    return redirect(url_for('view_cart'))

#Go to my profile
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # 1. Update basic info
        current_user.name = form.name.data
        current_user.email = form.email.data
        
        # 2. Update password ONLY if they typed something new
        if form.password.data:
            hashed_pw = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            current_user.password = hashed_pw
            
        db.session.commit()
        # flash("Your profile has been updated!")
        return redirect(url_for('home'))

    # 3. Pre-populate the form with current data (The "GET" request)
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    return render_template('profile.html', form=form)

# --- ROUTE 1: REQUEST RESET (User types email) ---
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            send_reset_email(user)
            
        # Security Best Practice: Always say "If that email exists..." 
        # so hackers can't fish for valid email addresses.
        flash('If an account with that email exists, an email has been sent with instructions.', 'info')
        return redirect(url_for('login'))
        
    return render_template('reset_request.html')

# --- ROUTE 2: PERFORM RESET (User clicks link) ---
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=1800)
    except SignatureExpired:
        flash('The token is expired! Please try again.', 'warning')
        return redirect(url_for('reset_request'))
    except:
        flash('Invalid token.', 'warning')
        return redirect(url_for('reset_request'))
        
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(request.url) # Reload the page
            
        # Update Password
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(
            password, 
            method='pbkdf2:sha256', 
            salt_length=8
        )
        db.session.commit()
        
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('reset_token.html')


@app.route('/admin/export_csv')
@admin_only
def export_csv():
    # 1. Query all orders
    orders = Order.query.order_by(Order.id.desc()).all()
    
    # 2. Setup CSV
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Order ID', 'Date', 'Customer Name', 'Email', 'Items', 'Total Price ($)', 'Status'])
    
    # 3. Loop through orders
    for order in orders:
        # A. Format Items (Safe Check)
        items_list = []
        for item in order.items:
            p_title = item.product.title if item.product else "Deleted Product"
            items_list.append(f"{p_title} (x{item.quantity})")
        items_str = "; ".join(items_list)
        
        # B. Handle Ghost Users (Safe Check)
        if order.customer:
            c_name = order.customer.name
            c_email = order.customer.email
        else:
            c_name = "Deleted User"
            c_email = "N/A"

        # C. Handle Ghost Dates (THE FIX)
        # If order.date is empty, print "Unknown Date" instead of blank
        date_str = order.date if order.date else "Unknown Date"

        # D. Write Row
        cw.writerow([
            order.id,
            date_str,     # <--- Uses the safe variable
            c_name,
            c_email,
            items_str,
            "%.2f" % (order.total_price / 100),
            order.status  # <--- Changed "Paid" to actual status (Pending/Shipped)
        ])
        
    # 4. Return File
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=orders_export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route('/order/cancel/<int:order_id>')
@login_required
def cancel_order(order_id):
    order = db.session.get(Order, order_id)
    
    # 1. Security Checks
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('my_orders'))
        
    if order.user_id != current_user.id:
        flash("You do not have permission to cancel this order.", "danger")
        return redirect(url_for('my_orders'))

    # 2. Status Check (CRITICAL)
    # Don't let them cancel if you already shipped it!
    if order.status == 'Shipped':
        flash("This order has already been shipped and cannot be cancelled.", "warning")
        return redirect(url_for('my_orders'))
        
    if order.status == 'Cancelled':
        flash("This order is already cancelled.", "info")
        return redirect(url_for('my_orders'))

    # 3. Soft Cancel (Update Status instead of Delete)
    try:
        order.status = "Cancelled"
        db.session.commit()
        
        # 4. Send Email
        # (Pass the refund amount so the email knows what to say)
        send_cancel_email(current_user, order.id, order.total_price)
        
        flash(f"Order #{order.id} has been cancelled.", "success")
        
    except Exception as e:
        db.session.rollback()
        flash("Could not cancel order. Error: " + str(e), "danger")

    return redirect(url_for('my_orders'))

if __name__=="__main__":
    app.run(debug=True)
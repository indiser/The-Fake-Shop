<div align="center">

# 🛒 The Fake Shop

### A Full-Stack E-Commerce Platform Built with Flask

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Features](#-features) • [Demo](#-demo) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## 📋 Overview

**The Fake Shop** is a modern, feature-rich e-commerce web application that demonstrates full-stack development capabilities. Built with Flask and SQLAlchemy, it provides a complete shopping experience with user authentication, product management, shopping cart functionality, order processing, customer reviews, and advanced admin analytics.

This project showcases proficiency in:
- Backend development with Python/Flask
- Database design and ORM implementation with SQLAlchemy 2.0
- User authentication and authorization with Flask-Login
- RESTful routing and session management
- Responsive frontend design with Bootstrap 5.3
- Cloud image storage with Cloudinary
- Email notifications with Flask-Mail
- Data visualization with Chart.js
- CSV export functionality
- Security best practices

---

## ✨ Features

### 🔐 User Management
- **Secure Authentication**: Password hashing with PBKDF2-SHA256 and 8-byte salt
- **User Registration & Login**: Complete user account system with Flask-Login
- **Role-Based Access Control**: Admin and customer user roles with different permissions
- **Session Management**: Secure session handling for cart and user state
- **Duplicate Prevention**: Email uniqueness validation during registration

### 🛍️ Shopping Experience
- **Product Catalog**: Paginated product browsing (12 items per page)
- **Advanced Search**: Real-time product search with query persistence across pages
- **Product Sorting**: Sort by price (low/high), newest, oldest arrivals
- **Product Details**: Comprehensive product pages with multi-image carousel and breadcrumb navigation
- **Shopping Cart**: Session-based cart with add/remove functionality and quantity tracking
- **Checkout System**: Complete order processing with price snapshots and email confirmation
- **Wishlist**: Save favorite products for later (customer-only feature)
- **Price Display**: Consistent formatting (stored in cents, displayed in dollars)
- **Empty States**: User-friendly messages when cart or search results are empty
- **Image Watermarking**: Cloudinary-powered automatic watermark on product images

### ⭐ Reviews & Ratings
- **Customer Reviews**: Authenticated users can write detailed product reviews
- **Star Ratings**: 5-star rating system with dropdown selection and visual star display
- **Average Ratings**: Dynamic calculation and display of product ratings on catalog
- **Review Management**: Timestamped reviews with author attribution
- **Review Display**: Shows review count and prevents admin from reviewing products
- **No Reviews State**: Encourages first review when product has no ratings

### 👨💼 Admin Dashboard
- **Analytics Dashboard**: Real-time KPIs (Total Revenue, Total Orders, Average Order Value)
- **Sales Chart**: Interactive line chart showing revenue trends over time (Chart.js)
- **Product Management**: Full CRUD operations with Cloudinary image upload or URL support
- **Multi-Image Gallery**: Upload additional product images with carousel display
- **Order Management**: View all customer orders with customer details and email
- **Order Status Tracking**: One-click status updates (Pending → Shipped → Cancelled)
- **CSV Export**: Download all orders as spreadsheet with customer and product details
- **Email Automation**: Automatic emails for order confirmation, shipping, and cancellation
- **Admin-Only Routes**: Protected routes with custom `@admin_only` decorator (403 error)
- **Admin Identification**: First registered user (ID #1) automatically becomes admin
- **Cascade Delete**: Safe product deletion with review cascade handling
- **Edit Pre-population**: Product edit form auto-fills with existing data

### 🎨 User Interface
- **Responsive Design**: Mobile-first Bootstrap 5.3 implementation with card-based layout
- **Dark Mode**: Toggle between light and dark themes with localStorage persistence (🌙/☀️ button)
- **Smooth Animations**: Card lift on hover (translateY -10px), button press effects, and image zoom (scale 1.05)
- **Intuitive Navigation**: Clean navbar with integrated search bar, wishlist icon, and dropdown menu
- **Flash Messages**: Categorized user feedback (success, warning, danger, info) with dismissible alerts
- **Visual Feedback**: Status badges (⏳ Pending/🚚 Shipped/❌ Cancelled), star ratings, and empty state messages
- **Image Handling**: Consistent aspect ratio (4:3) with object-fit for uniform product cards
- **Image Carousel**: Multi-image product gallery with navigation controls
- **Breadcrumb Navigation**: Easy navigation on product detail pages
- **Dropdown Menus**: Context-aware user menu (different for admin vs customer)

---

## 🎥 Demo

### Customer View
- Browse products with pagination, search, and sorting
- View detailed product information with multi-image carousel and reviews
- Add items to cart and complete checkout with email confirmation
- Save products to wishlist for later
- Track order history and status
- Cancel pending orders before shipment
- Update profile information and password
- Leave reviews and ratings on products
- Reset forgotten password via email

### Admin View
- View executive dashboard with revenue analytics and sales charts
- Add, edit, and delete products with Cloudinary image upload
- Upload multiple images per product for gallery
- View all customer orders with customer information
- Update order status with one click (triggers email notifications)
- Export all orders to CSV for reporting
- Manage inventory and product catalog
- Cannot leave reviews (admin-only restriction)

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0+
- **ORM**: SQLAlchemy 2.0+ with Flask-SQLAlchemy 3.1+
- **Authentication**: Flask-Login 0.6+ with Werkzeug password hashing
- **Forms**: Flask-WTF 1.2+ with WTForms 3.1+ validation
- **Email**: Flask-Mail 0.9+ with Gmail SMTP integration
- **Cloud Storage**: Cloudinary 1.36+ for image hosting and transformation
- **Token Security**: itsdangerous 2.1+ for password reset tokens
- **Database**: SQLite (development) / PostgreSQL-ready (production)
- **Environment**: python-dotenv 1.0+ for configuration

### Frontend
- **UI Framework**: Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js for data visualization
- **Template Engine**: Jinja2
- **JavaScript**: Vanilla JS for theme toggle, confirmations, and interactions
- **CSS**: Custom animations and transitions
- **Image Carousel**: Bootstrap 5 carousel component

### Security
- **Password Hashing**: PBKDF2-SHA256 with 8-byte salt via Werkzeug
- **CSRF Protection**: Flask-WTF CSRF tokens on all forms
- **Session Security**: Secure session cookies with secret key
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **Authorization**: Custom `@admin_only` and `@login_required` decorators
- **Token-Based Reset**: Time-limited password reset tokens (30 min expiry)
- **Email Validation**: WTForms email validator
- **File Upload Security**: FileAllowed validator for image uploads

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/fake-market.git
cd fake-market
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

**Dependencies installed:**
- Flask 3.0.0 - Web framework
- Flask-SQLAlchemy 3.1.1 - Database ORM
- Flask-Login 0.6.3 - User session management
- Flask-WTF 1.2.1 - Form handling and CSRF protection
- WTForms 3.1.1 - Form validation
- Flask-Mail 0.9.1 - Email sending
- python-dotenv 1.0.0 - Environment variable management
- Werkzeug 3.0.1 - Password hashing utilities
- cloudinary 1.36.0 - Cloud image storage and transformation
- itsdangerous 2.1.2 - Token generation for password reset
- email-validator 2.1.0 - Email format validation

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
SECRET_KEY=your-secret-key-here
DB_URI=sqlite:///Product.db
CLOUDINARY_CLOUD_NAME=your-cloudinary-cloud-name
CLOUDINARY_API_KEY=your-cloudinary-api-key
CLOUDINARY_API_SECRETS=your-cloudinary-api-secret
EMAIL_USER=your-gmail-address@gmail.com
EMAIL_PASS=your-gmail-app-password
```

**Note**: 
- For Cloudinary, sign up at [cloudinary.com](https://cloudinary.com) to get your credentials
- For Gmail, you need to generate an [App Password](https://support.google.com/accounts/answer/185833) (not your regular password)

5. **Initialize the database**
```bash
# Open server.py and uncomment the database creation lines (around line 127-128):
# with app.app_context():
#     db.create_all()
# Then run the server once to create the database, then comment them back
```

6. **Run the application**
```bash
python server.py
```

7. **Access the application**

Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🚀 Usage

### First-Time Setup

1. **Create Admin Account**: The first registered user (ID #1) automatically becomes the admin
2. **Add Products**: Login as admin and use "Add Product" to populate the store
3. **Test Shopping**: Create a customer account to test the shopping experience

### Admin Functions
- **View Dashboard**: Click "Dashboard" to see analytics and sales charts
- **Add Product**: Click "Add Product" in dropdown menu
- **Upload Images**: Use Cloudinary upload or paste image URL
- **Add Gallery Images**: Upload additional images on product detail page
- **Edit Product**: Click "✏️ Edit" on any product card
- **Delete Product**: Click "🗑️ Delete" (confirmation required)
- **Manage Orders**: Click "📦 Manage Orders" to view all orders
- **Ship Orders**: Click "Ship Order" to update status and send email
- **Export Data**: Click "Export Sales" to download CSV report

### Customer Functions
- **Browse**: Use search bar, sorting, or pagination to find products
- **Wishlist**: Click heart icon to save products for later
- **View Gallery**: Click product to see multi-image carousel
- **Add to Cart**: Click "Add to Cart" on product cards
- **Review**: Visit product detail page to leave a review with star rating
- **Checkout**: View cart and click "Proceed to Checkout" (receives email receipt)
- **Track Orders**: Click "My Orders" to view order history
- **Cancel Order**: Cancel pending orders before they ship
- **Update Profile**: Click "My Account" to change name, email, or password
- **Reset Password**: Use "Forgot Password" link on login page

---

## 📊 Database Schema

### Tables
- **User**: User accounts (id, name, email, password)
- **Product**: Product catalog (id, title, price, description, image_url)
- **ProductImage**: Additional product images (id, image_url, product_id)
- **Order**: Customer orders (id, user_id, date, total_price, status)
- **OrderItem**: Line items (id, order_id, product_id, quantity, price_at_purchase)
- **Review**: Customer reviews (id, rating, text, product_id, user_id, date_posted)
- **wishlist_table**: Many-to-many association table (user_id, product_id)

### Relationships
- User → Orders (One-to-Many) via `orders` backref
- User → Reviews (One-to-Many) via `reviews` backref
- User ↔ Products (Many-to-Many) via `wishlist` and `wished_by` (wishlist feature)
- Product → Reviews (One-to-Many) with cascade delete
- Product → ProductImages (One-to-Many) via `images` backref
- Product → OrderItems (One-to-Many)
- Order → OrderItems (One-to-Many) via `items` backref
- Order → User (Many-to-One) via `customer` backref
- Review → User (Many-to-One) via `author` backref
- Review → Product (Many-to-One) via `product` backref

### Key Design Decisions
- **Price Storage**: Stored as integers (cents) to avoid floating-point precision errors
- **Price Snapshots**: OrderItem stores `price_at_purchase` to preserve historical pricing
- **Cascade Deletes**: Product deletion automatically removes associated reviews and images
- **Status Tracking**: Orders support three states: Pending, Shipped, Cancelled
- **Soft Deletes**: Orders are cancelled (status change) rather than deleted from database
- **Image Watermarking**: Cloudinary transformation adds "FAKE SHOP" watermark dynamically
- **Token Expiry**: Password reset tokens expire after 30 minutes (1800 seconds)
- **Email Triggers**: Automated emails sent on order placement, shipment, and cancellation

---

## 🔒 Security Features

- ✅ Password hashing with salt (PBKDF2-SHA256, 8-byte salt via Werkzeug)
- ✅ CSRF protection on all forms via Flask-WTF
- ✅ SQL injection prevention via SQLAlchemy ORM parameterized queries
- ✅ Admin-only route protection with custom `@admin_only` decorator
- ✅ Login required decorators via Flask-Login (`@login_required`)
- ✅ Secure session management with secret key
- ✅ Environment variable configuration via python-dotenv (credentials not hardcoded)
- ✅ User authentication checks before sensitive operations
- ✅ Duplicate email prevention during registration
- ✅ 403 Forbidden errors for unauthorized access attempts
- ✅ Time-limited password reset tokens (30-minute expiry via itsdangerous)
- ✅ File upload validation (only jpg, png, jpeg allowed)
- ✅ Email validation via WTForms validators
- ✅ Order ownership verification (users can only cancel their own orders)
- ✅ Status-based operation restrictions (can't cancel shipped orders)

---

## 🎯 Key Highlights

### Code Quality
- **Clean Architecture**: Separation of concerns with models, forms, and routes
- **DRY Principles**: Reusable decorators (`@admin_only`) and template inheritance
- **Error Handling**: Graceful error handling with user feedback via flash messages
- **Type Hints**: SQLAlchemy 2.0 mapped columns with type annotations
- **Consistent Naming**: Clear, descriptive variable and function names

### Performance
- **Pagination**: Efficient data loading with 12 items per page using Flask-SQLAlchemy `paginate()`
- **Query Optimization**: Proper use of relationships and backref for efficient queries
- **Session-Based Cart**: Lightweight cart stored in Flask session without database overhead
- **Price Storage**: Prices stored as integers (cents) to avoid floating-point errors
- **Lazy Loading**: Reviews, orders, and images loaded on-demand via relationships
- **Image CDN**: Cloudinary CDN for fast global image delivery
- **Image Transformation**: On-the-fly image resizing and watermarking via Cloudinary
- **Lazy Image Loading**: `loading="lazy"` attribute for deferred image loading
- **Aggregate Functions**: SQLAlchemy `func.sum()` for efficient revenue calculations
- **Grouped Queries**: SQL GROUP BY for daily sales chart data

### User Experience
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop
- **Accessibility**: Semantic HTML and ARIA labels
- **Visual Feedback**: Loading states, hover effects, and animations
- **Dark Mode**: User preference persistence via localStorage
- **Empty States**: Helpful messages when no data is available
- **Confirmation Dialogs**: JavaScript confirms for destructive actions

---

## 📈 Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Product categories and filtering by category
- [ ] Inventory management with stock tracking and low-stock alerts
- [ ] Coupon/discount system with promo codes
- [ ] RESTful API for mobile apps
- [ ] Product quantity adjustment in cart (currently fixed at 1)
- [ ] Export orders to PDF invoices
- [ ] Advanced search filters (price range, rating, category)
- [ ] Product recommendations based on purchase history
- [ ] Real-time order tracking with shipping carrier integration
- [ ] Customer support chat system
- [ ] Product comparison feature
- [ ] Bulk product import via CSV
- [ ] Multi-currency support
- [ ] Social media sharing for products
- [ ] Review helpfulness voting ("Was this review helpful?")
- [ ] Admin notifications for new orders
- [ ] Automated inventory reordering
- [ ] Sales tax calculation by region
- [ ] Gift card functionality

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨💻 Author

**Your Name**

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Flask documentation and community
- Bootstrap for the UI framework
- SQLAlchemy for the excellent ORM
- All open-source contributors

---

<div align="center">

### ⭐ If you found this project helpful, please consider giving it a star!

**Built with ❤️ using Flask and Python**

</div>

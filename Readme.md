<div align="center">

# 🛒 The Fake Shop

### A Full-Stack E-Commerce Platform with Y2K Retro UI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)
[![Tailwind](https://img.shields.io/badge/Tailwind-3.0+-38bdf8.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Features](#-features) • [Tech Stack](#-tech-stack) • [Installation](#-installation) • [Screenshots](#-ui-showcase)**

---

</div>

## 📋 Overview

**The Fake Shop** is a modern, feature-rich e-commerce web application with a unique **Windows XP / Y2K-inspired retro UI**. Built with Flask and powered by SQLAlchemy 2.0, it combines nostalgic design aesthetics with modern functionality including user authentication, shopping cart, coupon system, order management, reviews, and comprehensive admin analytics.

### 🎨 Design Philosophy

This project showcases a **pixel-perfect recreation of early 2000s web design** (1999-2004 era), featuring:
- Windows XP-style beveled panels and buttons with gradient effects
- Retro color schemes with custom CSS variables for light/dark mode
- VT323 and Press Start 2P pixel fonts for authentic nostalgia
- Animated promo banners with countdown timers
- CRT scanline effects in dark mode
- Custom XP-style scrollbars and UI components

---

## ✨ Features

### 🎨 **Retro UI Design System**
- **Windows XP Aesthetics**: Authentic beveled buttons, panels, and windows with raised/sunken effects
- **Y2K Color Palette**: Carefully crafted color variables for both light and dark modes
- **Custom Pixel Fonts**: VT323 for headings, Press Start 2P for accents, Trebuchet MS for body text
- **Responsive Layout**: Mobile-first Tailwind CSS with custom retro styling
- **Dark Mode**: Toggle with localStorage persistence, includes CRT scanline effect
- **Animated Elements**: Hover effects, card lifts, button press animations, marquee scrolling banners
- **Custom Scrollbars**: Windows XP-style scrollbar recreation for webkit browsers

### 🛍️ **Shopping Experience**
- **Product Catalog**: Grid-based product browsing with pagination (12 items per page)
- **Advanced Search**: Real-time product search with query tracking and analytics
- **Smart Sorting**: Sort by price (low/high), newest arrivals, oldest first
- **Product Details**: Multi-image carousel gallery, breadcrumb navigation, customer reviews
- **Shopping Cart**: Session-based cart with quantity display, subtotal calculation, coupon support
- **Wishlist System**: Save favorite products for later (customer-only feature)
- **Promo Banner**: Time-limited promotional banner (1st-15th of each month) with live countdown timer
- **Coupon System**: Percentage-based discount codes with visual confirmation
- **Free Shipping**: Automatic free shipping on orders over $50
- **Image Watermarking**: Cloudinary-powered automatic "FAKE SHOP" watermark on product images

### 🔐 **User Management**
- **Secure Authentication**: PBKDF2-SHA256 password hashing with 8-byte salt
- **Registration & Login**: Complete user account system with Flask-Login
- **Email Validation**: Strict email provider whitelist (Gmail, Outlook, Yahoo, iCloud, ProtonMail)
- **Disposable Email Blocking**: Prevents registration with 25+ known temporary email services
- **Password Requirements**: Enforced complexity (uppercase, lowercase, number, symbol, 8+ chars)
- **Password Reset**: Time-limited token-based reset via email (30-minute expiry)
- **Profile Management**: Update name, email, password from account page
- **Soft Account Deletion**: Users can delete accounts (marked as deleted, not removed from DB)
- **Role-Based Access**: Admin (User #1) vs Customer permissions with @admin_only decorator

### ⭐ **Reviews & Ratings**
- **5-Star Rating System**: Dropdown selection with visual star display (★/☆)
- **Customer Reviews**: Authenticated users can write detailed product reviews
- **Average Ratings**: Dynamic calculation and display on product cards
- **Review Management**: Timestamped reviews with author attribution
- **Admin Restriction**: Admin users cannot leave reviews (business logic)
- **Review Display**: Shows review count and encourages first review when empty

### 💰 **Coupon System**
- **Admin Coupon Manager**: Create percentage-based discount codes (1-100% off)
- **Case-Insensitive Codes**: Uppercase storage, flexible customer input
- **Cart Integration**: Apply coupons directly in cart with visual confirmation
- **Session Persistence**: Applied coupons saved across page loads
- **Discount Calculation**: Applies to cart subtotal before shipping
- **Order History**: Tracks discount amount per order in database

### 📦 **Order Management**
- **Order Processing**: Complete checkout flow with price snapshots (prevents price manipulation)
- **Status Tracking**: Three-state system (Pending → Shipped → Cancelled)
- **Order History**: Customers view their own orders with status badges
- **Customer Cancellation**: Cancel pending orders before shipment
- **Admin Controls**: Ship orders with one click, force-cancel any order
- **Email Notifications**: Automated emails for order confirmation, shipment, cancellation
- **PDF Invoices**: Email-attached PDF invoices generated with xhtml2pdf
- **Admin Alerts**: Real-time email alerts to admin when customers place orders
- **CSV Export**: Download all orders as spreadsheet with customer and product details
- **Ghost User Handling**: Safe handling of orders from deleted user accounts

### 👨‍💼 **Admin Dashboard**
- **Executive KPIs**: Total Revenue, Total Orders, Average Order Value, Pending Order Count
- **Sales Chart**: Interactive 30-day revenue trend visualization with Chart.js
- **Product Management**: Full CRUD operations with Cloudinary image upload or URL support
- **Multi-Image Gallery**: Upload additional product images with thumbnail carousel
- **Order Management**: View all customer orders sorted by newest first
- **Quick Actions**: One-click access to orders, coupons, products, CSV export
- **Search Analytics**: Top 5 customer search terms with frequency count
- **System Info Panel**: Site status, security badges, admin session info
- **Pending Order Badge**: Real-time count of pending orders in navbar (context processor)

### 📧 **Email System**
- **Async Email Sending**: Non-blocking email dispatch using Python threading
- **Order Confirmation**: Plain text receipt with itemized breakdown
- **PDF Invoice**: Professional invoice document attached to confirmation email
- **Shipping Notification**: Email sent when admin marks order as shipped
- **Cancellation Refund**: Email with refund details when order is cancelled
- **Admin Alerts**: Instant notification to admin email for new orders
- **Password Reset**: Secure token-based reset link with 30-minute expiry
- **Gmail SMTP**: Configured for Gmail with app-specific password support

### 🎯 **User Interface Components**
- **Navigation**: Sticky header with integrated search, category tabs, dropdown menus
- **Marquee Banner**: Animated promotional messages in top utility bar
- **Flash Messages**: Categorized alerts (success/warning/danger/info) with dismiss button
- **Empty States**: User-friendly messages for empty cart, no search results, no reviews
- **Breadcrumbs**: Contextual navigation on product detail pages
- **Pagination**: XP-style pagination buttons with current page highlighting
- **Dropdown Menus**: Context-aware user menu with different options for admin vs customer
- **Modal Dialogs**: Age verification modal (Windows XP style) with localStorage persistence
- **Status Badges**: Visual indicators (⏳ Pending / 🚚 Shipped / ❌ Cancelled)
- **Trust Badges**: Security and shipping guarantee badges throughout checkout flow
- **Mobile Menu**: Hamburger menu with full-screen overlay for mobile devices

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0+ (Python web framework)
- **ORM**: SQLAlchemy 2.0+ with Flask-SQLAlchemy 3.1+
- **Authentication**: Flask-Login 0.6+ with Werkzeug password hashing (PBKDF2-SHA256)
- **Forms**: Flask-WTF 1.2+ with WTForms 3.1+ validation
- **Email**: Flask-Mail 0.9+ with Gmail SMTP integration
- **Cloud Storage**: Cloudinary 1.36+ for image hosting and transformation
- **PDF Generation**: xhtml2pdf for invoice creation
- **Token Security**: itsdangerous 2.1+ for password reset tokens
- **Email Validation**: email-validator 2.1+ for format checking
- **Database**: SQLite (development) / PostgreSQL-ready (production)
- **Environment**: python-dotenv 1.0+ for configuration

### Frontend
- **CSS Framework**: Tailwind CSS 3.0+ (via CDN)
- **Custom Styling**: 600+ lines of handcrafted CSS for retro UI components
- **Icons**: Emoji icons for universal compatibility
- **Charts**: Chart.js 4.x for sales analytics visualization
- **Template Engine**: Jinja2 (Flask default)
- **JavaScript**: Vanilla JS for theme toggle, dropdowns, image carousel, countdowns
- **Fonts**: Google Fonts (VT323, Press Start 2P) + system fonts (Trebuchet MS, Courier New)
- **Responsive Design**: CSS Grid + Flexbox with mobile-first media queries

### Security
- **Password Hashing**: PBKDF2-SHA256 with 8-byte salt (600,000 iterations via Werkzeug)
- **CSRF Protection**: Flask-WTF automatic CSRF tokens on all forms
- **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
- **Authorization**: Custom @admin_only and @login_required decorators
- **Session Security**: Secure session cookies with SECRET_KEY
- **IDOR Prevention**: Order ownership verification before viewing invoices
- **Token Expiry**: Password reset tokens expire after 30 minutes
- **File Upload Security**: FileAllowed validator (jpg, png, jpeg only)
- **Email Validation**: Format validation + disposable email blocking
- **State Machine**: Order status validation (can't cancel shipped orders)

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Setup Instructions

1. **Clone or download the repository**
```bash
git clone https://github.com/indiser/The-Fake-Shop.git
cd The-Fake-Shop
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

**Key dependencies:**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.1
Flask-Mail==0.9.1
python-dotenv==1.0.0
Werkzeug==3.0.1
cloudinary==1.36.0
itsdangerous==2.1.2
email-validator==2.1.0
xhtml2pdf==0.2.11
```

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

**Important Notes:**
- **Cloudinary**: Sign up at [cloudinary.com](https://cloudinary.com) (free tier available)
- **Gmail**: Generate an [App Password](https://support.google.com/accounts/answer/185833) (don't use regular password)
- **SECRET_KEY**: Generate a strong random key (e.g., `python -c "import secrets; print(secrets.token_hex(32))"`)

5. **Initialize the database**
```bash
python server.py
# Database will be created automatically on first run
# The tables are created via: with app.app_context(): db.create_all()
```

6. **Access the application**

Open your browser and navigate to: `http://127.0.0.1:5000`

---

## 🚀 Usage

### First-Time Setup

1. **Create Admin Account**: The first registered user (ID #1) automatically becomes the admin
2. **Add Products**: Login as admin, navigate to dropdown menu → "Add Product"
3. **Create Coupons**: Admin dropdown → "Coupons" → Create discount codes
4. **Test Shopping**: Register a second account to test the customer experience

### Admin Workflows
- **Dashboard**: Click "📊 Dashboard" in dropdown to view analytics and sales chart
- **Add Product**: Dropdown → "➕ Add Product" → Upload image or paste URL
- **Add Gallery**: On product detail page, upload additional images via "📂 Add Gallery Image" panel
- **Edit Product**: Click "✏️ Edit" button on any product card (pre-populates form with existing data)
- **Delete Product**: Click "🗑️ Delete" button (confirmation required, cascade deletes reviews)
- **Manage Orders**: Dropdown → "📦 Manage Orders" → View all customer orders
- **Ship Order**: Click "🚚 Ship Order" button (triggers email, updates status)
- **Cancel Order**: Click "❌ Cancel" button (refund email sent, status updated)
- **Manage Coupons**: Dropdown → "🏷️ Coupons" → Create/delete discount codes
- **Export Sales**: Dropdown → "📊 Export Sales CSV" → Download orders spreadsheet
- **View Shop**: Dashboard → "🏠 View Shop" (see store as customer would)

### Customer Workflows
- **Browse Products**: Use search bar, sorting dropdown, or pagination to explore catalog
- **Search Products**: Type in search bar (queries are tracked for admin analytics)
- **Add to Wishlist**: Click ❤️ icon on product cards (persistent across sessions)
- **View Product**: Click product card to see multi-image gallery, reviews, and details
- **Add to Cart**: Click "🛒 Add to Cart" button (session-based, survives page refreshes)
- **Apply Coupon**: In cart, enter code (e.g., SAVE20) → "Apply Code ▶" button
- **Checkout**: Cart → "🔒 Proceed to Checkout →" → Order confirmation + email receipt + PDF invoice
- **View Orders**: Dropdown → "📄 My Orders" → See order history with status badges
- **Download Invoice**: My Orders → Click "📄 Invoice" button (PDF download)
- **Cancel Order**: My Orders → Click "❌ Cancel" (only works if status is Pending, not Shipped)
- **Leave Review**: Product detail page → Scroll to "💬 Customer Reviews" → Fill form
- **Update Profile**: Dropdown → "👤 My Account" → Change name, email, or password
- **Reset Password**: Login page → "Forgot Password?" → Enter email → Check inbox for link
- **Delete Account**: Profile page → "Delete Account" button (soft delete, can be restored by admin)

---

## 📊 Database Schema

### Tables
| Table | Description | Key Fields |
|-------|-------------|------------|
| **User** | User accounts | id, name, email, password, is_deleted |
| **Product** | Product catalog | id, title, price (cents), description, image_url |
| **ProductImage** | Additional product images | id, image_url, product_id (FK) |
| **Order** | Customer orders | id, user_id (FK), date, total_price, status, discount_amount |
| **OrderItem** | Line items in orders | id, order_id (FK), product_id (FK), quantity, price_at_purchase |
| **Review** | Customer reviews | id, rating, text, product_id (FK), user_id (FK), date_posted |
| **Coupon** | Discount codes | id, code, discount (%), active |
| **SearchTerm** | Search analytics | id, term, count, last_searched |
| **wishlist_table** | Many-to-many association | user_id, product_id |

### Key Relationships
```
User ─────┬─ One-to-Many ──→ Order
          ├─ One-to-Many ──→ Review
          └─ Many-to-Many ─→ Product (wishlist)

Product ──┬─ One-to-Many ──→ Review (cascade delete)
          ├─ One-to-Many ──→ ProductImage
          └─ One-to-Many ──→ OrderItem

Order ────┬─ One-to-Many ──→ OrderItem
          └─ Many-to-One ──→ User (customer backref)

Review ───┬─ Many-to-One ──→ Product (product backref)
          └─ Many-to-One ──→ User (author backref)
```

### Design Decisions
- **Price Storage**: Integers (cents) to avoid floating-point precision errors (e.g., 1000 = $10.00)
- **Price Snapshots**: OrderItem.price_at_purchase preserves historical pricing (prevents price manipulation)
- **Cascade Deletes**: Product deletion automatically removes associated reviews and images
- **Status Tracking**: Orders support three states (Pending → Shipped → Cancelled)
- **Soft Deletes**: Users marked as deleted (is_deleted=True) instead of removed from DB
- **Image Watermarking**: Cloudinary transformation adds "FAKE SHOP" watermark dynamically
- **Token Expiry**: Password reset tokens expire after 30 minutes (itsdangerous max_age=1800)
- **Email Triggers**: Async email dispatch (Python threading) for order/ship/cancel events
- **Search Tracking**: SearchTerm table logs queries with count and timestamp for analytics

---

## 🔒 Security Features

| Feature | Implementation | Protection Against |
|---------|----------------|---------------------|
| **Password Hashing** | PBKDF2-SHA256, 8-byte salt, 600K iterations | Rainbow tables, brute force |
| **CSRF Protection** | Flask-WTF automatic tokens on all forms | Cross-site request forgery |
| **SQL Injection** | SQLAlchemy ORM parameterized queries | SQL injection attacks |
| **Admin-Only Routes** | Custom @admin_only decorator (403 error) | Unauthorized access |
| **Login Required** | Flask-Login @login_required decorator | Anonymous access |
| **Session Security** | SECRET_KEY signed cookies | Session hijacking |
| **Environment Variables** | python-dotenv (no hardcoded credentials) | Credential exposure |
| **Password Reset** | Time-limited tokens (30 min expiry) | Token replay attacks |
| **File Upload** | FileAllowed validator (jpg, png, jpeg only) | Malicious file upload |
| **Email Validation** | Format validation + disposable email blocking | Fake accounts |
| **IDOR Prevention** | Order ownership verification | Unauthorized data access |
| **State Machine** | Order status validation (can't cancel shipped) | Business logic bypass |
| **Password Complexity** | 8+ chars, upper, lower, number, symbol | Weak passwords |
| **Duplicate Prevention** | Email uniqueness constraint | Account duplication |

---

## 🎯 Key Highlights

### Code Quality
- **Clean Architecture**: Separation of concerns (models, forms, routes in server.py)
- **DRY Principles**: Reusable decorators (@admin_only) and template inheritance (base.html)
- **Error Handling**: Try-catch blocks with user-friendly flash messages
- **Type Hints**: SQLAlchemy 2.0 mapped columns with type annotations
- **Consistent Naming**: Descriptive variable names (e.g., price_in_cents, hash_and_salted_password)
- **Comments**: Inline documentation for complex logic and business rules
- **Validation**: Server-side validation on all forms (WTForms validators)

### Performance
- **Pagination**: Efficient data loading (12 items per page) using Flask-SQLAlchemy paginate()
- **Query Optimization**: Proper use of relationships and backref for N+1 prevention
- **Session-Based Cart**: Lightweight cart stored in Flask session (no DB writes until checkout)
- **Price Storage**: Integer math (cents) avoids floating-point errors
- **Lazy Loading**: Reviews/orders/images loaded on-demand via SQLAlchemy relationships
- **Image CDN**: Cloudinary CDN for fast global image delivery
- **On-the-Fly Transformation**: Cloudinary watermarking without pre-processing
- **Lazy Image Loading**: loading="lazy" attribute for deferred image loading
- **Aggregate Functions**: SQLAlchemy func.sum() for efficient revenue calculations
- **Grouped Queries**: SQL GROUP BY for daily sales chart data (no Python aggregation)
- **Async Email**: Non-blocking email dispatch via Python threading

### User Experience
- **Responsive Design**: Mobile-first CSS Grid + Flexbox, works on all screen sizes
- **Accessibility**: Semantic HTML5, ARIA labels, keyboard navigation support
- **Visual Feedback**: Loading states, hover effects, animations (card lift, button press)
- **Dark Mode**: User preference persistence via localStorage, toggle button in navbar
- **Empty States**: Helpful messages when cart/search results/wishlist are empty
- **Confirmation Dialogs**: JavaScript confirms for destructive actions (delete product/order)
- **Breadcrumbs**: Contextual navigation on product detail pages
- **Flash Messages**: Color-coded alerts with dismiss button (success/warning/danger/info)
- **Trust Badges**: Security and shipping guarantees throughout checkout flow
- **Sticky Elements**: Sidebar on cart page uses position: sticky for better UX

---

## 📈 Future Enhancements

### 🔥 Implemented Features
- ✅ ~~Product quantity adjustment in cart~~ **Implemented**: Quantity display with increment/decrement controls
- ✅ ~~Coupon/discount system with promo codes~~ **Implemented**: Admin coupon manager with percentage discounts
- ✅ ~~Export orders to PDF invoices~~ **Implemented**: Email-attached PDF invoices with xhtml2pdf
- ✅ ~~Multi-image product gallery~~ **Implemented**: Upload additional images with thumbnail carousel
- ✅ ~~Password reset functionality~~ **Implemented**: Token-based email reset with 30-minute expiry

### 🚀 Planned Improvements
- [ ] **Payment Gateway Integration**: Stripe/PayPal for real credit card processing
- [ ] **Product Categories**: Add category taxonomy with filtering sidebar
- [ ] **Inventory Management**: Stock tracking with low-stock alerts and "Out of Stock" badges
- [ ] **RESTful API**: JSON endpoints for mobile app integration
- [ ] **Advanced Filters**: Price range slider, rating filter, multi-select categories
- [ ] **Product Recommendations**: "You may also like" based on category/price/rating
- [ ] **Real-Time Order Tracking**: Integration with shipping carriers (FedEx/UPS APIs)
- [ ] **Live Chat Support**: Socket.io-based customer support chat system
- [ ] **Product Comparison**: Side-by-side feature comparison table (max 4 products)
- [ ] **Bulk Import/Export**: CSV bulk product upload and export
- [ ] **Multi-Currency Support**: Currency converter with real-time exchange rates
- [ ] **Social Sharing**: Open Graph meta tags + share buttons for products
- [ ] **Review Voting**: "Was this review helpful?" upvote/downvote system
- [ ] **Admin Notifications**: Real-time browser notifications for new orders (Notification API)
- [ ] **Sales Tax Calculation**: Tax rates by ZIP code/state (TaxJar API)
- [ ] **Gift Cards**: Digital gift card purchase and redemption system
- [ ] **Abandoned Cart Recovery**: Email reminders for unpurchased cart items
- [ ] **Wishlist Sharing**: Shareable wishlist links for gift registries
- [ ] **Product Bundles**: Create multi-product bundles with discounted pricing
- [ ] **Related Products**: Machine learning recommendations based on purchase history

---

## 🎨 UI Showcase

### Design System Features
- **Retro Color Palette**: CSS custom properties for light and dark modes
- **Beveled Components**: Windows XP-style 3D buttons and panels
- **Custom Scrollbars**: Webkit scrollbar styling matching XP aesthetic
- **Pixel Fonts**: VT323, Press Start 2P for headings and accents
- **Gradient Backgrounds**: Multi-stop gradients for buttons and panels
- **CRT Effect**: Scanline overlay in dark mode for authentic retro feel
- **Animated Marquee**: Promotional messages scroll in top banner
- **Countdown Timer**: Live JavaScript countdown on promo banner (1st-15th)

### Responsive Breakpoints
```css
@media (max-width: 768px)  /* Mobile: single column, hamburger menu */
@media (max-width: 1023px) /* Tablet: scaled UI elements */
@media (max-width: 419px)  /* Small mobile: stacked layouts */
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

**Contribution Guidelines:**
- Follow PEP 8 style guide for Python code
- Use semantic commit messages (feat/fix/docs/style/refactor)
- Add comments for complex business logic
- Test locally before submitting PR
- Update README if adding new features

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**

- GitHub: [@indiser](https://github.com/indiser)
- Email: indiser01@gmail.com

---

## 🙏 Acknowledgments

- **Flask Documentation**: Comprehensive guides for Flask-SQLAlchemy and Flask-Login
- **Bootstrap Icons**: Emoji icons for universal compatibility
- **Cloudinary**: Free tier for image hosting and transformation
- **Chart.js**: Beautiful sales analytics visualization
- **Google Fonts**: VT323 and Press Start 2P for retro typography
- **Windows XP Design**: Inspiration for UI components and color schemes
- **Y2K Web Aesthetics**: Early 2000s design principles and patterns
- **All open-source contributors**: Libraries and tools that made this project possible

---

<div align="center">

### ⭐ If you found this project helpful, please give it a star!

**Built with ❤️ using Flask, Python, and 2000s Nostalgia**

![Retro Badge](https://img.shields.io/badge/Aesthetic-Y2K_Retro-ff6b9d?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-00cc00?style=for-the-badge)
![Vibes](https://img.shields.io/badge/Vibes-Immaculate-ffd700?style=for-the-badge)

</div>

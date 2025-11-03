# CKW Cloud Kitchen 🍽️

A comprehensive Django-based web application for a modern cloud kitchen food ordering system. Built with Django 5.2.4, featuring user authentication, dynamic menu management, shopping cart functionality, order tracking, and customer reviews.
# For ADMIN panel control contact: sharmaakshit820@gmail.com
## 🚀 Features

### 🔐 User Management
- **Custom Authentication**: Secure user registration and login with password hashing
- **Profile Management**: Update personal details, phone number, address, and profile pictures
- **Session Management**: Persistent cart for both authenticated and guest users

### 🍜 Menu System
- **7 Food Categories**: Starters, Main Course, Biryani, Burgers, Drinks, Desserts, and Combos
- **Dynamic Menu Items**: Add, update, and manage food items with prices and descriptions
- **Availability Control**: Enable/disable menu items as needed
- **Visual Icons**: FontAwesome icons for better UI experience

### 🛒 Shopping Cart
- **Real-time Updates**: AJAX-powered cart modifications without page refresh
- **Quantity Management**: Increase/decrease item quantities
- **Persistent Storage**: Cart data survives browser sessions
- **Price Calculations**: Automatic subtotal, tax (18% GST), and delivery fee (₹40) calculations

### 📦 Order Management
- **Order Placement**: Seamless checkout process with order confirmation
- **Status Tracking**: Visual order status from pending to delivered
- **Order History**: Complete order history for users
- **Unique Order Numbers**: Auto-generated order IDs (CKW + date + random digits)

### 🎯 Promotions & Offers
- **Discount System**: Percentage-based discounts on selected items
- **Offer Management**: Activate/deactivate promotional offers
- **Dynamic Pricing**: Automatic calculation of discounted prices

### ⭐ Customer Interaction
- **Reviews & Ratings**: 1-5 star rating system with user feedback
- **Contact Forms**: Customer inquiry and support system
- **Message Management**: Admin panel for handling customer messages

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile and desktop optimized
- **Glassmorphism Effects**: Modern CSS styling with backdrop blur effects
- **Video Backgrounds**: Dynamic video backgrounds for enhanced visual appeal
- **Smooth Animations**: CSS transitions and JavaScript animations

## 🛠️ Technology Stack

- **Backend**: Django 5.2.4 with Python
- **Database**: SQLite3 (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: FontAwesome, Boxicons
- **Media Handling**: Django's file upload system for images

## 📁 Project Structure

```
CKW/
├── CKW/                    # Main Django project
│   ├── settings.py        # Django settings and configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI application
├── cloud_kitchen/         # Main Django app
│   ├── models.py         # Database models (9 models)
│   ├── views.py          # View functions (14+ functions)
│   ├── urls.py           # App URL patterns
│   ├── admin.py          # Admin panel configuration
│   ├── apps.py           # App configuration
│   ├── templates/        # HTML templates (18 files)
│   ├── static/           # CSS, JS, images, videos
│   └── migrations/       # Database migrations
├── profile_pics/          # User uploaded profile pictures
├── db.sqlite3            # SQLite database
└── manage.py             # Django management commands
```

## 🗄️ Database Schema

### Core Models
1. **User**: Custom user authentication with profile pictures
2. **Category**: 7 predefined food categories
3. **FoodItem**: Menu items with pricing and availability
4. **Cart/CartItem**: Shopping cart system
5. **Order**: Order management with status tracking
6. **Offer**: Promotional discount system
7. **ContactMessage**: Customer support messages
8. **Review**: User feedback and ratings

### Key Relationships
- User ↔ Cart (One-to-One)
- User ↔ Orders (One-to-Many)
- Category ↔ FoodItem (One-to-Many)
- Cart ↔ CartItem (One-to-Many)
- FoodItem ↔ CartItem/Offer (One-to-Many)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed
- pip package manager
- Virtualenv (optional but recommended)

### Installation & Setup

1. **Clone/Download the project**
   ```bash
   # Navigate to the project directory containing manage.py
   cd path/to/CKW-project
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment

   # For Windows:
   venv\Scripts\activate

   # For macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   # Install Django
   pip install django

   # Install Pillow for image handling (required for profile pictures)
   pip install pillow
   ```

4. **Database setup**
   ```bash
   # Run database migrations
   python manage.py migrate
   ```

5. **Create admin user**
   ```bash
   # Create superuser for admin access
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   # Start the Django development server
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

### Deactivating Virtual Environment
```bash
# When done working, deactivate the virtual environment
deactivate
```

### Sample Data Setup
- Create categories and food items through the admin panel
- Add sample menu items to populate the application
- Create user accounts for testing

## 🎯 Usage

### For Customers
1. **Register/Login**: Create account or sign in
2. **Browse Menu**: Explore different food categories
3. **Add to Cart**: Select items and modify quantities
4. **Checkout**: Place orders with delivery details
5. **Track Orders**: Monitor order status in real-time
6. **Leave Reviews**: Rate and review the service

### For Administrators
1. **Admin Panel**: Access Django admin at `/admin/`
2. **Manage Menu**: Add/edit food items and categories
3. **Handle Orders**: Update order statuses
4. **View Messages**: Respond to customer inquiries
5. **Monitor Reviews**: Read customer feedback

## 🔧 Key Features Deep Dive

### Authentication System
- Custom user model with email and phone support
- Password hashing using Django's built-in system
- Session-based cart for guest users
- Profile picture upload functionality

### Cart & Ordering
- AJAX-powered cart operations (no page refresh)
- Automatic price calculations including GST and delivery
- Order number generation (CKW + date + random digits)
- Order status workflow: pending → confirmed → preparing → ready → delivered

### Menu Management
- Hierarchical category system
- Dynamic pricing and availability
- FontAwesome icon integration
- Easy admin management through Django admin

## 🎨 Styling & UI

### CSS Architecture
- **11 Custom CSS files** for different sections
- Glassmorphism effects with backdrop-filter
- Responsive grid and flexbox layouts
- Smooth hover animations and transitions

### Visual Elements
- Video backgrounds (BG1.mp4, BG2.mp4)
- Professional color scheme
- Icon-based navigation
- Mobile-first responsive design

## 🔒 Security Features

- CSRF protection on all forms
- Password hashing and validation
- Session management
- SQL injection prevention through Django ORM
- XSS protection with template escaping

## 📱 Responsive Design

- Mobile-optimized layouts
- Touch-friendly interface elements
- Adaptive navigation menus
- Optimized for various screen sizes

## 🔄 Future Enhancements

- Payment gateway integration
- Real-time order notifications
- Delivery tracking with maps
- Loyalty program implementation
- Mobile app development
- Multi-language support
## NOTE: sign in/log in using google and apple is still in dev.
## 📞 Support

For questions or support regarding the CKW Cloud Kitchen project, please use the contact form within the application or reach out through GitHub issues.
mail: sharmaakshit820@gmail.com

---

**Built with ❤️ using Django** | **Version**: 1.0 | **Django**: 5.2.4

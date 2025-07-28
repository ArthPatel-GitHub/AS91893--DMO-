# app.py

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os # Import os module to handle file paths

# Initialize the Flask application
app = Flask(__name__)

# --- Database Configuration (Requirement: Database Linking) ---
# Get the absolute path to the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLite database file path
# This will create a 'site.db' file in your project's root directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Disable tracking modifications to save memory

# Initialize the database object
db = SQLAlchemy(app)

# --- Define Database Models (Tables) ---
# Convention: Database Model Definition
# Each class represents a table in our database.
# This will store information about different 'Destinations' or 'Highlights'.

class Destination(db.Model):
    # __tablename__ = 'destinations' # Optional: if you want a different table name

    id = db.Column(db.Integer, primary_key=True) # Unique ID for each entry
    title = db.Column(db.String(100), nullable=False) # Name of the destination/highlight
    description = db.Column(db.Text, nullable=False) # A longer description
    image_url = db.Column(db.String(200), nullable=True) # URL for an image (optional)
    category = db.Column(db.String(50), nullable=True) # E.g., 'Culture', 'Nature', 'History'

    # This method is for how the object is represented when printed (useful for debugging)
    def __repr__(self):
        return f"Destination('{self.title}', '{self.category}')"


# --- Routing ---
# This is the main route for the homepage
@app.route('/')
def home():
    # --- Retrieving Data from Database ---
    # Retrieve all destinations from the database
    # This demonstrates the 'database linking' requirement
    destinations = Destination.query.all()
    return render_template('index.html', destinations=destinations)

# --- Running the Flask App ---
if __name__ == '__main__':
    # Convention: Create Database Tables
    # This block ensures that the database tables are created before the app runs.
    # You only need to run this once, or whenever you modify your models.
    with app.app_context():
        db.create_all()
        # You can also add some initial data here if the database is empty
        # Example: Check if any destinations exist, if not, add some
        if not Destination.query.first():
            print("Database is empty. Adding initial data...")
            destination1 = Destination(
                title='Vibrant Festivals',
                description='Experience the colorful celebrations that light up India\'s calendar, from Diwali to Holi.',
                image_url='https://via.placeholder.com/300x200?text=Festival',
                category='Culture'
            )
            destination2 = Destination(
                title='Rich Traditions',
                description='Discover the ancient customs and diverse heritage that define Indian society.',
                image_url='https://via.placeholder.com/300x200?text=Tradition',
                category='Culture'
            )
            destination3 = Destination(
                title='Diverse Arts',
                description='Explore classical dance forms, intricate music, and beautiful craftsmanship.',
                image_url='https://via.placeholder.com/300x200?text=Art',
                category='Culture'
            )
            # Add these to the session
            db.session.add(destination1)
            db.session.add(destination2)
            db.session.add(destination3)
            # Commit the changes to the database
            db.session.commit()
            print("Initial data added.")

    app.run(debug=True)
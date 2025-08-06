# app.py

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SERVER_NAME'] = 'localhost:5000'
app.config['SECRET_KEY'] = 'your-very-secret-key-that-you-should-change'

db = SQLAlchemy(app)

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Destination('{self.title}', '{self.category}')"

class CarouselImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"CarouselImage('{self.image_url}')"

@app.route('/')
def home():
    destinations = Destination.query.filter(Destination.category != 'Hero').all()
    hero_image = Destination.query.filter_by(category='Hero').first()
    carousel_images = CarouselImage.query.all()
    return render_template('index.html', destinations=destinations, hero_image=hero_image, carousel_images=carousel_images)

@app.route('/culture')
def culture():
    destinations = Destination.query.all()
    return render_template('culture.html', destinations=destinations)

@app.route('/cuisine')
def cuisine():
    carousel_images = CarouselImage.query.all()
    return render_template('cuisine.html', carousel_images=carousel_images)

@app.route('/history')
def history():
    destinations = Destination.query.all()
    return render_template('history.html', destinations=destinations)

@app.route('/nature')
def nature():
    destinations = Destination.query.all()
    return render_template('nature.html', destinations=destinations)

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Destination.query.first():
            print("Database is empty. Adding initial data...")
            
            # This is where hero_photo is defined
            hero_photo = Destination(
                title='Hero Section',
                description='High-resolution photo for the main banner.',
                image_url=url_for('static', filename='images/hero-image.jpg'),
                category='Hero'
            )
            
            # --- Culture Entries (4 total) ---
            destination1 = Destination(
                title='Vibrant Festivals',
                description="Experience the colorful celebrations that light up India's calendar, from Diwali to Holi.",
                image_url=url_for('static', filename='images/festival.jpg'),
                category='Culture'
            )
            destination2 = Destination(
                title='Rich Traditions',
                description='Discover the ancient customs and diverse heritage that define Indian society.',
                image_url=url_for('static', filename='images/tradition.jpg'),
                category='Culture'
            )
            destination3 = Destination(
                title='Diverse Arts',
                description='Explore classical dance forms, intricate music, and beautiful craftsmanship.',
                image_url=url_for('static', filename='images/art.jpg'),
                category='Culture'
            )
            destination_new = Destination(
                title='Spiritual Journeys',
                description='Find peace and enlightenment in India’s countless temples and sacred sites.',
                image_url=url_for('static', filename='images/spiritual.jpg'),
                category='Culture'
            )

            # --- History Entries (4 total) ---
            history_highlight1 = Destination(
                title='Ancient Forts & Palaces',
                description='Explore the majestic forts and opulent palaces that tell a tale of India\'s royal past.',
                image_url=url_for('static', filename='images/history.jpg'),
                category='History'
            )
            history_highlight2 = Destination(
                title='The Taj Mahal',
                description='The iconic monument of love, a masterpiece of Mughal architecture and one of the new wonders of the world.',
                image_url=url_for('static', filename='images/taj-mahal.jpg'),
                category='History'
            )
            history_highlight3 = Destination(
                title='Historical City Tours',
                description='Walk through the vibrant lanes of ancient cities like Delhi and Jaipur, each narrating a unique historical saga.',
                image_url=url_for('static', filename='images/city-tour.jpg'),
                category='History'
            )
            history_highlight4 = Destination(
                title='Architectural Ruins',
                description='Uncover the secrets of a bygone era by visiting the impressive and intricate ruins of ancient empires.',
                image_url=url_for('static', filename='images/ruins.jpg'),
                category='History'
            )

            # --- Nature Entries (4 total) ---
            nature_highlight1 = Destination(
                title='Himalayan Landscapes',
                description='Discover the breathtaking beauty of the Himalayas, from snowy peaks to lush valleys.',
                image_url=url_for('static', filename='images/nature.jpg'),
                category='Nature'
            )
            nature_highlight2 = Destination(
                title='Tropical Backwaters',
                description='Experience the serene beauty of Kerala\'s backwaters on a traditional houseboat journey.',
                image_url=url_for('static', filename='images/backwaters.jpg'),
                category='Nature'
            )
            nature_highlight3 = Destination(
                title='Wildlife Sanctuaries',
                description='Get up close with India\'s diverse wildlife, including tigers, elephants, and rare bird species.',
                image_url=url_for('static', filename='images/wildlife.jpg'),
                category='Nature'
            )
            nature_highlight4 = Destination(
                title='Desert Wonders',
                description='Explore the vast and stunning Thar Desert on a camel safari, witnessing golden sand dunes and vibrant culture.',
                image_url=url_for('static', filename='images/desert.jpg'),
                category='Nature'
            )
            
            # --- Cuisine Entries (3 total) ---
            cuisine_photo1 = CarouselImage(
                image_url=url_for('static', filename='images/cuisine1.jpg'),
                caption='A taste of North Indian cuisine.'
            )
            cuisine_photo2 = CarouselImage(
                image_url=url_for('static', filename='images/cuisine2.jpg'),
                caption='Spicy and flavorful South Indian dishes.'
            )
            cuisine_photo3 = CarouselImage(
                image_url=url_for('static', filename='images/cuisine3.jpg'),
                caption='Delicious and traditional Indian sweets.'
            )

            db.session.add(hero_photo)
            db.session.add(destination1)
            db.session.add(destination2)
            db.session.add(destination3)
            db.session.add(destination_new)
            db.session.add(history_highlight1)
            db.session.add(history_highlight2)
            db.session.add(history_highlight3)
            db.session.add(history_highlight4)
            db.session.add(nature_highlight1)
            db.session.add(nature_highlight2)
            db.session.add(nature_highlight3)
            db.session.add(nature_highlight4)
            db.session.add(cuisine_photo1)
            db.session.add(cuisine_photo2)
            db.session.add(cuisine_photo3)
            db.session.commit()
            print("Initial data added.")

    app.run(debug=True)
# app.py
from flask import Flask, render_template, url_for, g
from flask_sqlalchemy import SQLAlchemy
import os

# Create the Flask application instance
app = Flask(__name__)

# Get the base directory of the application
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the server name and a secret key
app.config['SERVER_NAME'] = 'localhost:5000'
app.config['SECRET_KEY'] = 'your-very-secret-key-that-you-should-change'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the database models
class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    sub_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Destination('{self.title}', '{self.category}')"

class CategoryHero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"CategoryHero('{self.category}', '{self.title}')"

# Get categories before each request
@app.before_request
def get_categories():
    categories_data = Destination.query.with_entities(Destination.category).filter(Destination.category.in_(['Culture', 'Cuisine', 'History', 'Nature'])).distinct().all()
    g.categories = [c[0] for c in categories_data]

# The home page route
@app.route('/')
def home():
    hero_image = Destination.query.filter_by(category='Hero').first()
    culture_highlights = Destination.query.filter_by(category='Culture').all()
    history_highlights = Destination.query.filter_by(category='History').limit(4).all()
    nature_highlights = Destination.query.filter_by(category='Nature').limit(4).all()
    featured_highlights = Destination.query.filter(Destination.sub_category.isnot(None)).limit(6).all()
    return render_template('index.html', hero_image=hero_image, culture_highlights=culture_highlights, history_highlights=history_highlights, nature_highlights=nature_highlights, featured_highlights=featured_highlights)

# Refactored routes for Culture, History, and Nature
@app.route('/culture')
def culture():
    items = Destination.query.filter_by(category='Culture').all()
    hero = CategoryHero.query.filter_by(category='Culture').first()
    return render_template('sub_category_page.html', items=items, hero=hero, category='culture')

@app.route('/history')
def history():
    items = Destination.query.filter_by(category='History').all()
    hero = CategoryHero.query.filter_by(category='History').first()
    return render_template('sub_category_page.html', items=items, hero=hero, category='history')

@app.route('/nature')
def nature():
    items = Destination.query.filter_by(category='Nature').all()
    hero = CategoryHero.query.filter_by(category='Nature').first()
    return render_template('sub_category_page.html', items=items, hero=hero, category='nature')

@app.route('/cuisine')
def cuisine():
    items = Destination.query.filter(Destination.category == 'Cuisine',
                                                  Destination.sub_category.isnot(None)).group_by(Destination.sub_category).all()
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    return render_template('sub_category_page.html', items=items, hero=hero, category='cuisine')

# The new, crucial route that creates a dynamic page for each item
@app.route('/details/<string:title>')
def details(title):
    item = Destination.query.filter_by(title=title).first_or_404()
    all_related_items = Destination.query.filter_by(category=item.category).all()
    return render_template('details.html', item=item, all_related_items=all_related_items)


# --- CUISINE SUBPAGE ROUTES ---
@app.route('/cuisine/north-indian')
def north_indian_page():
    items = Destination.query.filter_by(sub_category='North Indian').all()
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    return render_template('cuisine_subpage.html', items=items, hero=hero, page_title='North Indian Cuisine')

@app.route('/cuisine/south-indian')
def south_indian_page():
    items = Destination.query.filter_by(sub_category='South Indian').all()
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    return render_template('cuisine_subpage.html', items=items, hero=hero, page_title='South Indian Cuisine')

@app.route('/cuisine/sweets')
def indian_sweets_page():
    items = Destination.query.filter_by(sub_category='Sweets').all()
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    return render_template('cuisine_subpage.html', items=items, hero=hero, page_title='Indian Sweets')

@app.route('/cuisine/thali-meals')
def thali_meals_page():
    items = Destination.query.filter_by(sub_category='Thali Meals').all()
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    return render_template('cuisine_subpage.html', items=items, hero=hero, page_title='Thali Meals')

@app.route('/cuisine/spices')
def spices_page():
    items = Destination.query.filter_by(sub_category='Spices').all()
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    return render_template('cuisine_subpage.html', items=items, hero=hero, page_title='Spices of India')

# The plan and about routes
@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Main block to run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Check if the database is empty before populating it
        if not Destination.query.first():
            print("Database is empty. Adding initial data...")
            
            hero_photo = Destination(
                title='Hero Section',
                description='High-resolution photo for the main banner.',
                image_url=url_for('static', filename='images/hero-image.jpg'),
                category='Hero'
            )
            
            # --- New hero photos for each category page ---
            culture_hero = CategoryHero(
                category='Culture',
                title='Vibrant Culture & Traditions',
                subtitle='Explore the deep-rooted customs and diverse heritage that define India.',
                image_url=url_for('static', filename='images/culture-hero.jpg')
            )
            cuisine_hero = CategoryHero(
                category='Cuisine',
                title='A Culinary Journey',
                subtitle='Explore the incredible diversity of India\'s regional cuisines.',
                image_url=url_for('static', filename='images/cuisine-hero.jpg')
            )
            history_hero = CategoryHero(
                category='History',
                title='India\'s Majestic Past',
                subtitle='Explore the majestic forts, palaces, and ancient ruins that tell India\'s story.',
                image_url=url_for('static', filename='images/history-hero.jpg')
            )
            nature_hero = CategoryHero(
                category='Nature',
                title='Breathtaking Nature & Wildlife',
                subtitle='From the Himalayan peaks to tropical backwaters, discover India\'s natural beauty.',
                image_url=url_for('static', filename='images/nature-hero.jpg')
            )
            
            # --- Culture Destinations ---
            festival1 = Destination(
                title='Holi',
                description="The festival of colors, Holi, is a joyous celebration of spring, friendship, and the triumph of good over evil.",
                image_url=url_for('static', filename='images/holi.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            festival2 = Destination(
                title='Diwali',
                description="Known as the festival of lights, Diwali symbolizes the spiritual victory of light over darkness and good over evil.",
                image_url=url_for('static', filename='images/diwali.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            festival3 = Destination(
                title='Durga Puja',
                description="A grand festival celebrating the goddess Durga, marking her victory over the buffalo demon Mahishasura.",
                image_url=url_for('static', filename='images/durga-puja.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            festival4 = Destination(
                title='Pushkar Camel Fair',
                description="A mesmerizing cultural spectacle in Rajasthan, bringing together thousands of camels, traders, and tourists.",
                image_url=url_for('static', filename='images/pushkar.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            
            tradition1 = Destination(
                title='Yoga & Meditation',
                description="The ancient science of Yoga and meditation is a cornerstone of Indian philosophy, promoting physical and mental well-being.",
                image_url=url_for('static', filename='images/yoga.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            tradition2 = Destination(
                title='Ayurveda',
                description="An ancient system of medicine and life philosophy that emphasizes holistic healing through diet, herbs, and lifestyle.",
                image_url=url_for('static', filename='images/ayurveda.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            tradition3 = Destination(
                title='Indian Wedding',
                description="Indian weddings are elaborate, multi-day celebrations filled with rich rituals, vibrant colors, and immense joy.",
                image_url=url_for('static', filename='images/wedding.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            tradition4 = Destination(
                title='Cuisine Traditions',
                description="From family recipes to regional specialities, Indian cuisine is a cherished tradition passed down through generations.",
                image_url=url_for('static', filename='images/cuisine-tradition.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )

            art1 = Destination(
                title='Classical Dances',
                description='Experience the beauty and grace of classical Indian dance forms like Bharatanatyam and Kathak.',
                image_url=url_for('static', filename='images/dance.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            art2 = Destination(
                title='Textile Craftsmanship',
                description='Discover the intricate art of Indian textiles, from silk weaving to vibrant block prints.',
                image_url=url_for('static', filename='images/textile.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            art3 = Destination(
                title='Indian Music',
                description='Get lost in the soulful melodies of classical Indian music, from the sitar to tabla.',
                image_url=url_for('static', filename='images/music.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            art4 = Destination(
                title='Art & Architecture',
                description='Marvel at the stunning blend of art and architecture in India’s ancient temples and monuments.',
                image_url=url_for('static', filename='images/architecture.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            
            # --- History Destinations ---
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
            
            # --- Nature Destinations ---
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
            
            # --- Cuisine Destinations ---
            cuisine1 = Destination(
                title='Indian Sweets',
                description='Indulge in a variety of traditional Indian desserts and sweets from different regions.',
                image_url=url_for('static', filename='images/sweets.jpg'),
                category='Cuisine',
                sub_category='Sweets'
            )
            cuisine2 = Destination(
                title='North Indian Dishes',
                description='Explore the rich and creamy curries, breads, and tandoori dishes of North India.',
                image_url=url_for('static', filename='images/north-indian.jpg'),
                category='Cuisine',
                sub_category='North Indian'
            )
            cuisine3 = Destination(
                title='South Indian Dishes',
                description='Discover the flavorful and spicy dishes, dosas, and idlis from South India.',
                image_url=url_for('static', filename='images/south-indian.jpg'),
                category='Cuisine',
                sub_category='South Indian'
            )
            cuisine4 = Destination(
                title='Indian Street Food',
                description='Savor the vibrant and diverse flavors of India\'s popular street food, from chaat to pakoras.',
                image_url=url_for('static', filename='images/street-food.jpg'),
                category='Cuisine',
                sub_category='Street Food'
            )
            cuisine5 = Destination(
                title='Thali Meals',
                description='Experience a complete and balanced meal on a single plate, featuring a variety of regional dishes.',
                image_url=url_for('static', filename='images/thali.jpg'),
                category='Cuisine',
                sub_category='Thali Meals'
            )
            cuisine6 = Destination(
                title='Spices of India',
                description='Learn about the aromatic spices that are the heart and soul of Indian cooking.',
                image_url=url_for('static', filename='images/spices.jpg'),
                category='Cuisine',
                sub_category='Spices'
            )
            
            db.session.add(hero_photo)
            db.session.add(culture_hero)
            db.session.add(cuisine_hero)
            db.session.add(history_hero)
            db.session.add(nature_hero)
            db.session.add(festival1)
            db.session.add(festival2)
            db.session.add(festival3)
            db.session.add(festival4)
            db.session.add(tradition1)
            db.session.add(tradition2)
            db.session.add(tradition3)
            db.session.add(tradition4)
            db.session.add(art1)
            db.session.add(art2)
            db.session.add(art3)
            db.session.add(art4)
            db.session.add(history_highlight1)
            db.session.add(history_highlight2)
            db.session.add(history_highlight3)
            db.session.add(history_highlight4)
            db.session.add(nature_highlight1)
            db.session.add(nature_highlight2)
            db.session.add(nature_highlight3)
            db.session.add(nature_highlight4)
            db.session.add(cuisine1)
            db.session.add(cuisine2)
            db.session.add(cuisine3)
            db.session.add(cuisine4)
            db.session.add(cuisine5)
            db.session.add(cuisine6)
            
            db.session.commit()
            print("Initial data added.")
            
    app.run(debug=True)
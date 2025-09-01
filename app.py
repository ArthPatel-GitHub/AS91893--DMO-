# app.py
# Flask web application for exploring Indian culture, cuisine, history, and nature
# This application uses Flask-SQLAlchemy for database operations and serves as a travel/cultural guide

# Import necessary Flask modules and extensions
from flask import Flask, render_template, url_for, g
from flask_sqlalchemy import SQLAlchemy

import os

# Create the Flask application instance
# This is the core of our web application
app = Flask(__name__, static_url_path='/static/images')

# Configuration Section
# ===================

# Get the base directory of the application
# This ensures the database path is relative to the app location
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the SQLite database
# SQLite is a lightweight database perfect for small to medium applications
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
# Disable modification tracking to save resources (not needed for this app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with our Flask app
# This creates the database connection and ORM functionality
db = SQLAlchemy(app)

# Database Models
# ===============

class Destination(db.Model):
    """
    Main model for storing destination/content information.
    This model is flexible and stores various types of content:
    - Cultural destinations (festivals, traditions, arts)
    - Historical sites and information
    - Natural attractions
    - Cuisine information
    - Hero images for pages
    """
    
    # Primary key - unique identifier for each destination
    id = db.Column(db.Integer, primary_key=True)
    
    # Title of the destination/content (required field)
    title = db.Column(db.String(100), nullable=False)
    
    # Short description for cards and previews (required field)
    description = db.Column(db.Text, nullable=False)
    
    # URL path to the associated image (optional)
    image_url = db.Column(db.String(200), nullable=True)
    
    # Main category: Culture, History, Nature, Cuisine, Hero, About
    category = db.Column(db.String(50), nullable=True)
    
    # Subcategory for more specific grouping (e.g., 'North Indian' under Cuisine)
    sub_category = db.Column(db.String(50), nullable=True)
    
    # Detailed description for individual destination pages (optional)
    long_description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """String representation of the Destination object for debugging"""
        return f"Destination('{self.title}', '{self.category}')"


class CategoryHero(db.Model):
    """
    Model for storing hero images and content for category pages.
    Each category (Culture, History, Nature, Cuisine) has its own hero section.
    """
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    
    # Category name - must be unique (each category has one hero)
    category = db.Column(db.String(50), nullable=False, unique=True)
    
    # Main title for the hero section
    title = db.Column(db.String(100), nullable=False)
    
    # Subtitle/tagline for additional context (optional)
    subtitle = db.Column(db.String(200), nullable=True)
    
    # Hero image URL (required for visual impact)
    image_url = db.Column(db.String(200), nullable=False)
    
    # Detailed description for the category (optional)
    long_description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        """String representation of the CategoryHero object for debugging"""
        return f"CategoryHero('{self.category}', '{self.title}')"


# Request Context Processors
# ==========================

@app.before_request
def get_categories():
    """
    Function that runs before each request to populate global categories.
    This makes categories available in all templates via the 'g' object.
    Only includes main navigation categories: Culture, Cuisine, History, Nature
    """
    # Query distinct categories from the database
    categories_data = Destination.query.with_entities(Destination.category).filter(
        Destination.category.in_(['Culture', 'Cuisine', 'History', 'Nature'])
    ).distinct().all()
    
    # Extract category names from tuples and store in Flask's 'g' object
    # 'g' is available throughout the request lifecycle and in templates
    g.categories = [c[0] for c in categories_data]


# Route Handlers
# ==============

@app.route('/')
def home():
    """
    Home page route handler.
    Displays hero image and highlights from different categories.
    This is the main landing page that showcases the best content.
    """
    # Get the main hero image for the homepage banner
    hero_image = Destination.query.filter_by(category='Hero').first()
    
    # Get all culture highlights (festivals, traditions, arts)
    culture_highlights = Destination.query.filter_by(category='Culture').all()
    
    # Get limited number of history highlights for the homepage preview
    history_highlights = Destination.query.filter_by(category='History').limit(4).all()
    
    # Get limited number of nature highlights for the homepage preview
    nature_highlights = Destination.query.filter_by(category='Nature').limit(4).all()
    
    # Get featured highlights - items with subcategories (6 items max)
    featured_highlights = Destination.query.filter(Destination.sub_category.isnot(None)).limit(6).all()
    
    # Render the homepage template with all the gathered data
    return render_template('index.html', 
                         hero_image=hero_image, 
                         culture_highlights=culture_highlights, 
                         history_highlights=history_highlights, 
                         nature_highlights=nature_highlights, 
                         featured_highlights=featured_highlights)


@app.route('/about')
def about():
    """
    About Us page route handler.
    Renders the About Us page with a hero image from the database.
    """
    # Get the hero image specifically for the About page
    about_hero = Destination.query.filter_by(category='About').first()
    
    # Render the about template with the hero image
    return render_template('about.html', about_hero=about_hero)


@app.route('/privacy')
def privacy():
    """
    Privacy Policy page route handler.
    Renders a static privacy policy page.
    """
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    """
    Terms of Use page route handler.
    Renders a static terms of use page.
    """
    return render_template('terms.html')


# Category Page Routes
# ===================
# These routes handle the main category pages using a shared template

@app.route('/culture')
def culture():
    """
    Culture category page route handler.
    Displays all cultural destinations (festivals, traditions, arts).
    """
    # Get all destinations in the Culture category
    items = Destination.query.filter_by(category='Culture').all()
    
    # Get the hero content for the Culture category page
    hero = CategoryHero.query.filter_by(category='Culture').first()
    
    # Use the shared sub_category_page.html template
    return render_template('sub_category_page.html', 
                         items=items, 
                         hero=hero, 
                         category='culture')


@app.route('/history')
def history():
    """
    History category page route handler.
    Displays all historical destinations and information.
    """
    # Get all destinations in the History category
    items = Destination.query.filter_by(category='History').all()
    
    # Get the hero content for the History category page
    hero = CategoryHero.query.filter_by(category='History').first()
    
    # Use the shared sub_category_page.html template
    return render_template('sub_category_page.html', 
                         items=items, 
                         hero=hero, 
                         category='history')


@app.route('/nature')
def nature():
    """
    Nature category page route handler.
    Displays all nature and wildlife destinations.
    """
    # Get all destinations in the Nature category
    items = Destination.query.filter_by(category='Nature').all()
    
    # Get the hero content for the Nature category page
    hero = CategoryHero.query.filter_by(category='Nature').first()
    
    # Use the shared sub_category_page.html template
    return render_template('sub_category_page.html', 
                         items=items, 
                         hero=hero, 
                         category='nature')


@app.route('/cuisine')
def cuisine():
    """
    Cuisine category page route handler.
    Displays cuisine subcategories (grouped by sub_category).
    Note: This shows one item per subcategory, not all cuisine items.
    """
    # Get one representative item from each cuisine subcategory
    # This creates a "menu" of cuisine types rather than showing all items
    items = Destination.query.filter(
        Destination.category == 'Cuisine', 
        Destination.sub_category.isnot(None)
    ).group_by(Destination.sub_category).all()
    
    # Get the hero content for the Cuisine category page
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the shared sub_category_page.html template
    return render_template('sub_category_page.html', 
                         items=items, 
                         hero=hero, 
                         category='cuisine')


# Dynamic Detail Page Route
# =========================

@app.route('/details/<string:title>')
def details(title):
    """
    Dynamic details page route handler.
    Creates individual pages for each destination based on title.
    This is the crucial route that allows each item to have its own page.
    
    Args:
        title (str): The title of the destination (from URL path)
    
    Returns:
        Rendered details.html template or 404 if not found
    """
    # Find the specific item by title, return 404 if not found
    item = Destination.query.filter_by(title=title).first_or_404()
    
    # Get all related items in the same category for "Related Content" section
    all_related_items = Destination.query.filter_by(category=item.category).all()
    
    # Render the details page with the item and related items
    return render_template('details.html', 
                         item=item, 
                         all_related_items=all_related_items)


# Cuisine Subcategory Routes
# ==========================
# These routes handle specific cuisine subcategories

@app.route('/cuisine/north-indian')
def north_indian_page():
    """
    North Indian cuisine subcategory page.
    Displays all North Indian dishes and information.
    """
    # Get all items in the North Indian subcategory
    items = Destination.query.filter_by(sub_category='North Indian').all()
    
    # Use the main cuisine hero for consistency
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the cuisine-specific template
    return render_template('cuisine_subpage.html', 
                         items=items, 
                         hero=hero, 
                         page_title='North Indian Cuisine')


@app.route('/cuisine/south-indian')
def south_indian_page():
    """
    South Indian cuisine subcategory page.
    Displays all South Indian dishes and information.
    """
    # Get all items in the South Indian subcategory
    items = Destination.query.filter_by(sub_category='South Indian').all()
    
    # Use the main cuisine hero for consistency
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the cuisine-specific template
    return render_template('cuisine_subpage.html', 
                         items=items, 
                         hero=hero, 
                         page_title='South Indian Cuisine')


@app.route('/cuisine/sweets')
def indian_sweets_page():
    """
    Indian sweets subcategory page.
    Displays all traditional Indian desserts and sweets.
    """
    # Get all items in the Sweets subcategory
    items = Destination.query.filter_by(sub_category='Sweets').all()
    
    # Use the main cuisine hero for consistency
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the cuisine-specific template
    return render_template('cuisine_subpage.html', 
                         items=items, 
                         hero=hero, 
                         page_title='Indian Sweets')


@app.route('/cuisine/thali-meals')
def thali_meals_page():
    """
    Thali meals subcategory page.
    Displays information about traditional Indian thali meals.
    """
    # Get all items in the Thali Meals subcategory
    items = Destination.query.filter_by(sub_category='Thali Meals').all()
    
    # Use the main cuisine hero for consistency
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the cuisine-specific template
    return render_template('cuisine_subpage.html', 
                         items=items, 
                         hero=hero, 
                         page_title='Thali Meals')


@app.route('/cuisine/spices')
def spices_page():
    """
    Spices subcategory page.
    Displays information about Indian spices and their uses.
    """
    # Get all items in the Spices subcategory
    items = Destination.query.filter_by(sub_category='Spices').all()
    
    # Use the main cuisine hero for consistency
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the cuisine-specific template
    return render_template('cuisine_subpage.html', 
                         items=items, 
                         hero=hero, 
                         page_title='Spices of India')


@app.route('/cuisine/street-food')
def street_food_page():
    """
    Street food subcategory page.
    Displays information about Indian street food varieties.
    """
    # Get all items in the Street Food subcategory
    items = Destination.query.filter_by(sub_category='Street Food').all()
    
    # Use the main cuisine hero for consistency
    hero = CategoryHero.query.filter_by(category='Cuisine').first()
    
    # Use the cuisine-specific template
    return render_template('cuisine_subpage.html', 
                         items=items, 
                         hero=hero, 
                         page_title='Street Food of India')


# Application Initialization and Data Seeding
# ===========================================

# Main block to run the application
if __name__ == '__main__':
    # Create application context for database operations
    with app.app_context():
        # Create all database tables based on our models
        db.create_all()
        
        # Check if the database is empty before populating it
        # This prevents duplicate data on subsequent runs
        if not Destination.query.first():
            print("Database is empty. Adding initial data...")
            
            # HERO IMAGES
            # ===========
            
            # Main homepage hero image
            hero_photo = Destination(
                title='Discover India',
                description='High-resolution photo for the main banner.',
                image_url=url_for('static', filename='images/hero-image.jpg'),
                category='Hero',
                long_description="Explore the beauty of India. The country is well known for its majestic landscapes, captivating wildlife, and rich cultural heritage."
            )

            # About page hero image
            about_hero = Destination(
                title='Our Story',
                description='A photo for the About Us page.',
                image_url=url_for('static', filename='images/about-us-hero.jpg'),
                category='About',
                long_description="A hero image for the About Us page."
            )
            
            # CATEGORY HERO IMAGES
            # ===================
            # These provide hero sections for each main category page
            
            # Culture category hero
            culture_hero = CategoryHero(
                category='Culture',
                title='Vibrant Culture & Traditions',
                subtitle='Explore the deep-rooted customs and diverse heritage that define India.',
                image_url=url_for('static', filename='images/culture-hero.jpg'),
                long_description="India is a mosaic of rich cultural traditions, a land where every festival tells a story and every art form carries centuries of history. From the vibrant festivals of Holi and Diwali to the ancient practices of Yoga and Ayurveda, the country's heritage is a living, breathing testament to its diverse people. This cultural vibrancy is celebrated in everything from its classical dance forms to its colorful folk arts, creating an experience that is both spiritual and profoundly human."
            )
            
            # Cuisine category hero
            cuisine_hero = CategoryHero(
                category='Cuisine',
                title='A Culinary Journey',
                subtitle='Explore the incredible diversity of India\'s regional cuisines.',
                image_url=url_for('static', filename='images/cuisine-hero.jpg'),
                long_description="Indian cuisine is a vibrant and complex tapestry of flavors, reflecting the country's vast geography and diverse cultures. Each region boasts its own unique culinary identity, from the rich, creamy curries of the north to the fiery, spice-laden dishes of the south. Indian food is a celebration of spices, fresh ingredients, and age-old cooking techniques, offering a sensory experience that delights and surprises with every bite."
            )
            
            # History category hero
            history_hero = CategoryHero(
                category='History',
                title='India\'s Majestic Past',
                subtitle='Explore the majestic forts, palaces, and ancient ruins that tell India\'s story.',
                image_url=url_for('static', filename='images/history-hero.jpg'),
                long_description="India's history is a grand saga of empires, invasions, and cultural renaissances. From the ancient Indus Valley Civilization to the sprawling Mughal Empire and the British colonial era, the country's past is etched in its magnificent forts, temples, and monuments. It is a history of innovation, resilience, and a continuous quest for knowledge, leaving behind a legacy that continues to inspire and shape the modern world."
            )
            
            # Nature category hero
            nature_hero = CategoryHero(
                category='Nature',
                title='Breathtaking Nature & Wildlife',
                subtitle='From the Himalayan peaks to tropical backwaters, discover India\'s natural beauty.',
                image_url=url_for('static', filename='images/nature-hero.jpg'),
                long_description="India's landscape is as diverse as its people, offering a breathtaking range of natural wonders. The towering peaks of the Himalayas, the lush, misty forests of the Western Ghats, and the serene backwaters of Kerala provide a stunning backdrop for unique wildlife. This is a land where you can encounter majestic tigers, playful elephants, and vibrant bird species in their natural habitats, making it a paradise for nature lovers and adventurers."
            )
            
            # CULTURE DESTINATIONS
            # ===================
            # Cultural content is organized into subcategories: Festivals, Traditions, and Arts
            
            # --- FESTIVALS SUBCATEGORY ---
            
            # Holi festival information
            festival1 = Destination(
                title='Holi',
                description="The festival of colors, Holi, is a joyous celebration of spring, friendship, and the triumph of good over evil.",
                long_description="Holi is one of India's most cherished and boisterous festivals, celebrated with immense zeal and enthusiasm across the country. It marks the end of winter and the beginning of spring, symbolizing new beginnings. People gather to throw colored powders and water at one another, a tradition that signifies the playful and unifying spirit of the festival. Beyond the fun, Holi holds deep cultural significance, commemorating the triumph of good over evil through stories like that of Prahlad and Holika, making it a festival of both joy and spiritual renewal.",
                image_url=url_for('static', filename='images/holi.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            
            # Diwali festival information
            festival2 = Destination(
                title='Diwali',
                description="Known as the festival of lights, Diwali symbolizes the spiritual victory of light over darkness and good over evil.",
                long_description="Diwali, the festival of lights, is arguably the most significant celebration in India. It is a five-day festival that illuminates homes and hearts with the glow of diyas (oil lamps), fireworks, and festive decorations. It commemorates the return of Lord Rama to Ayodhya after defeating the demon king Ravana, symbolizing the victory of righteousness over evil. Families come together to perform prayers, exchange sweets and gifts, and light up their surroundings, creating an atmosphere of warmth, prosperity, and hope.",
                image_url=url_for('static', filename='images/diwali.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            
            # Durga Puja festival information
            festival3 = Destination(
                title='Durga Puja',
                description="A grand festival celebrating the goddess Durga, marking her victory over the buffalo demon Mahishasura.",
                long_description="Durga Puja is a grand, ten-day Hindu festival that pays homage to the goddess Durga. It is particularly celebrated in the eastern states of India, especially West Bengal, where it is a cultural extravaganza. Elaborate idols of Goddess Durga are worshipped in magnificent pandals (temporary structures) that are works of art in themselves. The festival signifies the victory of good over evil, with the goddess defeating the buffalo demon Mahishasura. It is a time for family gatherings, feasting, and the celebration of womanhood and divine power.",
                image_url=url_for('static', filename='images/durga-puja.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            
            # Pushkar Camel Fair information
            festival4 = Destination(
                title='Pushkar Camel Fair',
                description="A mesmerizing cultural spectacle in Rajasthan, bringing together thousands of camels, traders, and tourists.",
                long_description="The Pushkar Camel Fair is one of the most unique and spectacular events in India. Held annually in the small town of Pushkar in Rajasthan, it is a bustling five-day affair where thousands of camels, cattle, and horses are traded. Beyond the livestock trading, the fair is a massive cultural festival, featuring camel races, rural sports, and traditional music and dance performances. It offers a fascinating glimpse into the vibrant rural life of Rajasthan and its rich traditions.",
                image_url=url_for('static', filename='images/pushkar.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            
            # --- TRADITIONS SUBCATEGORY ---
            
            # Yoga and meditation information
            tradition1 = Destination(
                title='Yoga & Meditation',
                description="The ancient science of Yoga and meditation is a cornerstone of Indian philosophy, promoting physical and mental well-being.",
                long_description="Originating in ancient India, Yoga is a holistic practice that combines physical postures (asanas), breathing techniques (pranayama), and meditation. It is not just an exercise system but a way of life that seeks to harmonize the body, mind, and spirit. It has gained worldwide popularity for its benefits in reducing stress, improving flexibility, and enhancing overall health. This ancient tradition is deeply rooted in Indian philosophy and continues to be a profound path to self-discovery and inner peace.",
                image_url=url_for('static', filename='images/yoga.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            
            # Ayurveda information
            tradition2 = Destination(
                title='Ayurveda',
                description="An ancient system of medicine and life philosophy that emphasizes holistic healing through diet, herbs, and lifestyle.",
                long_description="Ayurveda, which means 'the science of life,' is one of the world's oldest holistic healing systems. Developed in India over 3,000 years ago, it is based on the belief that health and wellness depend on a delicate balance between the mind, body, and spirit. Ayurvedic treatments use a combination of diet, herbal remedies, massage, and lifestyle adjustments to restore this balance. It's a profound tradition that offers a natural and personalized approach to achieving optimal health and preventing disease.",
                image_url=url_for('static', filename='images/ayurveda.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            
            # Indian wedding traditions information
            tradition3 = Destination(
                title='Indian Wedding',
                description="Indian weddings are elaborate, multi-day celebrations filled with rich rituals, vibrant colors, and immense joy.",
                long_description="Indian weddings are much more than a single ceremony; they are a series of elaborate, multi-day celebrations that bring entire families and communities together. Each ritual, from the pre-wedding henna ceremony (Mehendi) to the vibrant main ceremony and reception, is steeped in tradition and symbolism. The celebrations are known for their stunning display of vibrant colors, intricate attire, joyous music, and delicious feasts. They are a true testament to the importance of family, community, and the sanctity of marriage in Indian culture.",
                image_url=url_for('static', filename='images/wedding.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            
            # Cuisine traditions information
            tradition4 = Destination(
                title='Cuisine Traditions',
                description="From family recipes to regional specialities, Indian cuisine is a cherished tradition passed down through generations.",
                long_description="Indian culinary traditions are a cherished part of the nation's cultural heritage. Cooking is often seen as a form of art, with recipes and techniques passed down through generations. The traditions emphasize the use of fresh, local ingredients and a meticulous balance of flavors. From the grand feasts prepared for festivals to the simple, comforting meals of daily life, Indian cuisine is an expression of hospitality, love, and a deep connection to the land and its seasons.",
                image_url=url_for('static', filename='images/cuisine-tradition.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )

            # --- ARTS SUBCATEGORY ---
            
            # Classical dance information
            art1 = Destination(
                title='Classical Dances',
                description='Experience the beauty and grace of classical Indian dance forms like Bharatanatyam and Kathak.',
                long_description="Indian classical dances are ancient art forms that combine intricate footwork, expressive gestures, and powerful storytelling. Each dance style, such as Bharatanatyam, Kathak, and Odissi, originated in a specific region and has its own unique grammar, music, and costume. These dances are not just performances but a form of spiritual expression, often narrating mythological tales and devotion to deities. They are a beautiful testament to India's rich artistic heritage.",
                image_url=url_for('static', filename='images/dance.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            
            # Textile craftsmanship information
            art2 = Destination(
                title='Textile Craftsmanship',
                description='Discover the intricate art of Indian textiles, from silk weaving to vibrant block prints.',
                long_description="India's textile craftsmanship is world-renowned for its intricacy, vibrant colors, and diversity. From the rich silks of Banaras to the intricate block prints of Rajasthan and the delicate embroidery of Kashmir, each region has developed its own unique textile traditions. These crafts are often passed down through generations of artisans, who use age-old techniques to create stunning fabrics. Indian textiles are not just clothing; they are a form of art that reflects the nation's history, culture, and regional identities.",
                image_url=url_for('static', filename='images/textile.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            
            # Indian music information
            art3 = Destination(
                title='Indian Music',
                description='Get lost in the soulful melodies of classical Indian music, from the sitar to tabla.',
                long_description="Indian music is a rich and soulful tradition with roots that stretch back thousands of years. It is broadly categorized into two major styles: North Indian Hindustani and South Indian Carnatic music. These traditions are based on the system of 'Ragas' (melodic frameworks) and 'Talas' (rhythmic cycles). From the haunting melodies of the sitar to the complex beats of the tabla, Indian music is an intricate and deeply spiritual art form that has captivated audiences around the world.",
                image_url=url_for('static', filename='images/music.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            
            # Art and architecture information
            art4 = Destination(
                title='Art & Architecture',
                description='Marvel at the stunning blend of art and architecture in India\'s ancient temples and monuments.',
                long_description="India's art and architecture are a grand reflection of its layered history and diverse cultures. From the ancient rock-cut temples of Ajanta and Ellora to the magnificent Mughal forts and palaces and the intricate carvings of Hindu temples, each architectural style tells a unique story. The buildings are not merely structures but works of art, adorned with detailed sculptures, frescoes, and paintings that bring myths and legends to life. They stand as a testament to the country's profound artistic and engineering legacy.",
                image_url=url_for('static', filename='images/architecture.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            
            # HISTORY DESTINATIONS
            # ===================
            # Historical content focuses on India's rich past and heritage sites
            
            # Ancient forts and palaces information
            history_highlight1 = Destination(
                title='Ancient Forts & Palaces',
                description='Explore the majestic forts and opulent palaces that tell a tale of India\'s royal past.',
                long_description="India's landscape is dotted with magnificent forts and opulent palaces that stand as silent witnesses to its glorious royal past. These architectural marvels, such as the Amber Fort in Jaipur and the Mysore Palace, are not just structures but epic tales of courage, power, and art. They reflect the unique blend of different architectural styles—from Rajput and Mughal to British—and offer a glimpse into the luxurious lives of the rulers who once inhabited them. Each fort and palace holds centuries of history within its walls.",
                image_url=url_for('static', filename='images/history.jpg'),
                category='History'
            )
            
            # Taj Mahal information
            history_highlight2 = Destination(
                title='The Taj Mahal',
                description='The iconic monument of love, a masterpiece of Mughal architecture and one of the new wonders of the world.',
                long_description="The Taj Mahal is an ivory-white marble mausoleum on the south bank of the Yamuna river in the Indian city of Agra. It was commissioned in 1631 by the Mughal emperor, Shah Jahan, to house the tomb of his favorite wife, Mumtaz Mahal. The Taj Mahal is widely considered the most beautiful example of Mughal architecture, a style that combines elements from Persian, Ottoman Turkish, Indian, and Islamic architectural styles. It is a symbol of eternal love and is one of the most famous and recognizable structures in the world.",
                image_url=url_for('static', filename='images/taj-mahal.jpg'),
                category='History'
            )
            
            # Historical city tours information
            history_highlight3 = Destination(
                title='Historical City Tours',
                description='Walk through the vibrant lanes of ancient cities like Delhi and Jaipur, each narrating a unique historical saga.',
                long_description="Ancient cities like Delhi and Jaipur are living museums, with every street and alley narrating a story from a bygone era. A historical city tour allows you to walk through centuries of history, from the narrow lanes of Old Delhi with its Mughal-era monuments to the majestic palaces and vibrant bazaars of the 'Pink City,' Jaipur. These tours offer a rich, immersive experience, combining the tales of emperors and battles with the colorful hustle and bustle of modern city life.",
                image_url=url_for('static', filename='images/city-tour.jpg'),
                category='History'
            )
            
            # Architectural ruins information
            history_highlight4 = Destination(
                title='Architectural Ruins',
                description='Uncover the secrets of a bygone era by visiting the impressive and intricate ruins of ancient empires.',
                long_description="India is home to countless architectural ruins that stand as testaments to the country's ancient and powerful empires. Sites like the ruins of Hampi, once the capital of the Vijayanagara Empire, or the ancient city of Nalanda, a famous center of learning, offer a profound glimpse into a lost world. These ruins are not just crumbling stones; they are living histories that invite you to imagine the lives, beliefs, and artistic brilliance of the people who built them.",
                image_url=url_for('static', filename='images/ruins.jpg'),
                category='History'
            )
            
            # NATURE DESTINATIONS
            # ==================
            # Nature content showcases India's diverse landscapes and wildlife
            
            # Himalayan landscapes information
            nature_highlight1 = Destination(
                title='Himalayan Landscapes',
                description='Discover the breathtaking beauty of the Himalayas, from snowy peaks to lush valleys.',
                long_description="The Himalayas, a majestic mountain range that forms a natural border with India, are a land of breathtaking landscapes and profound spirituality. From the towering, snow-capped peaks and serene glacial lakes to the lush green valleys and vibrant alpine meadows, the Himalayas offer an unparalleled experience for adventurers and seekers of peace. This region is home to some of the world's highest peaks, including Mount Everest, and is revered as the abode of gods, making it a place of both stunning natural beauty and deep cultural significance.",
                image_url=url_for('static', filename='images/nature.jpg'),
                category='Nature'
            )
            
            # Tropical backwaters information
            nature_highlight2 = Destination(
                title='Tropical Backwaters',
                description='Experience the serene beauty of Kerala\'s backwaters on a traditional houseboat journey.',
                long_description="The backwaters of Kerala are a unique ecosystem of interconnected canals, lakes, and lagoons, running parallel to the Arabian Sea. A journey on a traditional houseboat through these tranquil waters is a mesmerizing experience. The serene landscapes are lined with lush greenery, swaying coconut palms, and charming villages. It offers a peaceful escape and a chance to witness the unique rural life of Kerala, from fishermen at work to locals going about their daily routines, all set against a backdrop of serene natural beauty.",
                image_url=url_for('static', filename='images/backwaters.jpg'),
                category='Nature'
            )
            
            # Wildlife sanctuaries information
            nature_highlight3 = Destination(
                title='Wildlife Sanctuaries',
                description='Get up close with India\'s diverse wildlife, including tigers, elephants, and rare bird species.',
                long_description="India is home to a rich and diverse range of wildlife, protected in numerous national parks and sanctuaries. These areas are crucial for the conservation of endangered species like the Bengal tiger, Asiatic lion, and one-horned rhinoceros. A safari through places like Ranthambore or Periyar offers an exhilarating opportunity to see these animals in their natural habitats. The sanctuaries are also home to a wide variety of bird species, making them a paradise for birdwatchers and nature photographers.",
                image_url=url_for('static', filename='images/wildlife.jpg'),
                category='Nature'
            )
            
            # Desert wonders information
            nature_highlight4 = Destination(
                title='Desert Wonders',
                description='Explore the vast and stunning Thar Desert on a camel safari, witnessing golden sand dunes and vibrant culture.',
                long_description="The Thar Desert, also known as the Great Indian Desert, is a vast, arid region in the northwestern part of India. Despite its harsh climate, the desert is a land of stunning beauty and unique culture. A camel safari is the perfect way to explore its endless golden sand dunes, witness spectacular sunsets, and experience the traditional desert life of Rajasthan. The region is also home to vibrant folk music, dance, and colorful festivals, making the desert a truly enchanting and unforgettable destination.",
                image_url=url_for('static', filename='images/desert.jpg'),
                category='Nature'
            )
            
            # CUISINE DESTINATIONS
            # ===================
            # Cuisine content is organized by subcategories representing different types of food
            
            # Indian sweets information
            cuisine1 = Destination(
                title='Indian Sweets',
                description='Indulge in a variety of traditional Indian desserts and sweets from different regions.',
                long_description="Indian sweets, or 'mithai,' are an essential part of every festival, celebration, and joyous occasion. Each region has its own unique specialties, from the creamy 'Rasgullas' of Bengal to the rich, layered 'Mysore Pak' of Karnataka and the beloved 'Gulab Jamuns' found across the country. Made with ingredients like milk, sugar, ghee, and nuts, these desserts are often a beautiful blend of flavors and textures. They are not just food but a symbol of happiness, hospitality, and celebration in Indian culture.",
                image_url=url_for('static', filename='images/sweets.jpg'),
                category='Cuisine',
                sub_category='Sweets'
            )
            
            # North Indian dishes information
            cuisine2 = Destination(
                title='North Indian Dishes',
                description='Explore the rich and creamy curries, breads, and tandoori dishes of North India.',
                long_description="North Indian cuisine is celebrated for its rich, aromatic, and comforting flavors. The food is often characterized by the use of dairy products like milk, yogurt, and paneer, as well as a variety of spices. Signature dishes include creamy curries like Butter Chicken and Shahi Paneer, accompanied by a wide range of breads like Naan and Roti cooked in a Tandoor (clay oven). The cuisine is a flavorful journey that showcases a blend of tradition and regional influences, leaving a lasting impression on your palate.",
                image_url=url_for('static', filename='images/north-indian.jpg'),
                category='Cuisine',
                sub_category='North Indian'
            )
            
            # South Indian dishes information
            cuisine3 = Destination(
                title='South Indian Dishes',
                description='Discover the flavorful and spicy dishes, dosas, and idlis from South India.',
                long_description="South Indian cuisine is a delightful world of vibrant flavors and fresh ingredients. The dishes are typically lighter and often feature a generous use of coconut, tamarind, and curry leaves. You'll find a variety of rice-based preparations like the savory `Dosa` (a thin crepe) and fluffy `Idli` (steamed rice cakes), usually served with a spicy lentil stew called `Sambar` and coconut chutney. This cuisine is known for its perfect balance of tangy, spicy, and savory notes that awaken the senses.",
                image_url=url_for('static', filename='images/south-indian.jpg'),
                category='Cuisine',
                sub_category='South Indian'
            )
            
            # Indian street food information
            cuisine4 = Destination(
                title='Indian Street Food',
                description='Savor the vibrant and diverse flavors of India\'s popular street food, from chaat to pakoras.',
                long_description="Indian street food is a culinary adventure, offering a quick and flavorful glimpse into the nation's diverse culinary landscape. From the tangy and spicy `chaat` to the crispy fried `pakoras` and the satisfying `samosas`, these dishes are a feast for the senses. Each city has its own specialty, from the `vada pav` in Mumbai to the `pani puri` found everywhere, making street food a beloved part of the daily life and cultural identity of India.",
                image_url=url_for('static', filename='images/street-food.jpg'),
                category='Cuisine',
                sub_category='Street Food'
            )
            
            # Thali meals information
            cuisine5 = Destination(
                title='Thali Meals',
                description='Experience a full-course Indian meal with a variety of dishes served on a single platter.',
                long_description="A 'Thali' is a complete meal served on a single platter, offering a taste of multiple dishes from a specific region. It's a fantastic way to experience a variety of flavors, textures, and aromas in one sitting. A typical Thali includes a selection of curries, vegetables, bread, rice, yogurt, a sweet dish, and a pickle, all arranged in small bowls. This traditional style of serving food is not just a meal but a balanced, wholesome, and cultural experience.",
                image_url=url_for('static', filename='images/thali.jpg'),
                category='Cuisine',
                sub_category='Thali Meals'
            )
            
            # Spices of India information
            cuisine6 = Destination(
                title='Spices of India',
                description='Discover the heart of Indian cooking with a look at its most essential spices.',
                long_description="Indian cuisine is world-famous for its complex and aromatic use of spices. Spices are not just for flavor; they have a rich history and are often used for their medicinal properties. From the warm notes of cumin and coriander to the fiery kick of chili and the sweet aroma of cardamom, each spice plays a crucial role. The art of balancing these spices is the key to creating the distinct and layered flavors that define Indian food, making a culinary tour of India a truly aromatic experience.",
                image_url=url_for('static', filename='images/spices.jpg'),
                category='Cuisine',
                sub_category='Spices'
            )

            # DATABASE OPERATIONS
            # ==================
            # Add all the destination objects to the database session
            db.session.add_all([
                # Hero images for main pages
                hero_photo, about_hero,
                
                # Category hero objects for category pages
                culture_hero, cuisine_hero, history_hero, nature_hero,
                
                # Culture category destinations (festivals, traditions, arts)
                festival1, festival2, festival3, festival4,
                tradition1, tradition2, tradition3, tradition4,
                art1, art2, art3, art4,
                
                # History category destinations
                history_highlight1, history_highlight2, history_highlight3, history_highlight4,
                
                # Nature category destinations
                nature_highlight1, nature_highlight2, nature_highlight3, nature_highlight4,
                
                # Cuisine category destinations (different subcategories of food)
                cuisine1, cuisine2, cuisine3, cuisine4, cuisine5, cuisine6
            ])
            
            # Commit the session to save all data to the database
            # This makes all the changes permanent
            db.session.commit()
            print("Initial data added to the database.")

    # Run the Flask development server
    # debug=True enables automatic reloading and detailed error messages
    # This should be set to False in production environments
    app.run(debug=False) #For deploying on Render
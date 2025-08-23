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
    long_description = db.Column(db.Text, nullable=True) # The new column for long text

    def __repr__(self):
        return f"Destination('{self.title}', '{self.category}')"

class CategoryHero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=False)
    long_description = db.Column(db.Text, nullable=True)

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
                title='Discover India',
                description='High-resolution photo for the main banner.',
                image_url=url_for('static', filename='images/hero-image.jpg'),
                category='Hero',
                long_description="Explore the beauty of India. The country is well known for its majestic landscapes, captivating wildlife, and rich cultural heritage."
            )
            
            # --- New hero photos for each category page ---
            culture_hero = CategoryHero(
                category='Culture',
                title='Vibrant Culture & Traditions',
                subtitle='Explore the deep-rooted customs and diverse heritage that define India.',
                image_url=url_for('static', filename='images/culture-hero.jpg'),
                long_description="India is a mosaic of rich cultural traditions, a land where every festival tells a story and every art form carries centuries of history. From the vibrant festivals of Holi and Diwali to the ancient practices of Yoga and Ayurveda, the country's heritage is a living, breathing testament to its diverse people. This cultural vibrancy is celebrated in everything from its classical dance forms to its colorful folk arts, creating an experience that is both spiritual and profoundly human."
            )
            cuisine_hero = CategoryHero(
                category='Cuisine',
                title='A Culinary Journey',
                subtitle='Explore the incredible diversity of India\'s regional cuisines.',
                image_url=url_for('static', filename='images/cuisine-hero.jpg'),
                long_description="Indian cuisine is a vibrant and complex tapestry of flavors, reflecting the country's vast geography and diverse cultures. Each region boasts its own unique culinary identity, from the rich, creamy curries of the north to the fiery, spice-laden dishes of the south. Indian food is a celebration of spices, fresh ingredients, and age-old cooking techniques, offering a sensory experience that delights and surprises with every bite."
            )
            history_hero = CategoryHero(
                category='History',
                title='India\'s Majestic Past',
                subtitle='Explore the majestic forts, palaces, and ancient ruins that tell India\'s story.',
                image_url=url_for('static', filename='images/history-hero.jpg'),
                long_description="India's history is a grand saga of empires, invasions, and cultural renaissances. From the ancient Indus Valley Civilization to the sprawling Mughal Empire and the British colonial era, the country's past is etched in its magnificent forts, temples, and monuments. It is a history of innovation, resilience, and a continuous quest for knowledge, leaving behind a legacy that continues to inspire and shape the modern world."
            )
            nature_hero = CategoryHero(
                category='Nature',
                title='Breathtaking Nature & Wildlife',
                subtitle='From the Himalayan peaks to tropical backwaters, discover India\'s natural beauty.',
                image_url=url_for('static', filename='images/nature-hero.jpg'),
                long_description="India’s landscape is as diverse as its people, offering a breathtaking range of natural wonders. The towering peaks of the Himalayas, the lush, misty forests of the Western Ghats, and the serene backwaters of Kerala provide a stunning backdrop for unique wildlife. This is a land where you can encounter majestic tigers, playful elephants, and vibrant bird species in their natural habitats, making it a paradise for nature lovers and adventurers."
            )
            
            # --- Culture Destinations ---
            festival1 = Destination(
                title='Holi',
                description="The festival of colors, Holi, is a joyous celebration of spring, friendship, and the triumph of good over evil.",
                long_description="Holi is one of India's most cherished and boisterous festivals, celebrated with immense zeal and enthusiasm across the country. It marks the end of winter and the beginning of spring, symbolizing new beginnings. People gather to throw colored powders and water at one another, a tradition that signifies the playful and unifying spirit of the festival. Beyond the fun, Holi holds deep cultural significance, commemorating the triumph of good over evil through stories like that of Prahlad and Holika, making it a festival of both joy and spiritual renewal.",
                image_url=url_for('static', filename='images/holi.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            festival2 = Destination(
                title='Diwali',
                description="Known as the festival of lights, Diwali symbolizes the spiritual victory of light over darkness and good over evil.",
                long_description="Diwali, the festival of lights, is arguably the most significant celebration in India. It is a five-day festival that illuminates homes and hearts with the glow of diyas (oil lamps), fireworks, and festive decorations. It commemorates the return of Lord Rama to Ayodhya after defeating the demon king Ravana, symbolizing the victory of righteousness over evil. Families come together to perform prayers, exchange sweets and gifts, and light up their surroundings, creating an atmosphere of warmth, prosperity, and hope.",
                image_url=url_for('static', filename='images/diwali.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            festival3 = Destination(
                title='Durga Puja',
                description="A grand festival celebrating the goddess Durga, marking her victory over the buffalo demon Mahishasura.",
                long_description="Durga Puja is a grand, ten-day Hindu festival that pays homage to the goddess Durga. It is particularly celebrated in the eastern states of India, especially West Bengal, where it is a cultural extravaganza. Elaborate idols of Goddess Durga are worshipped in magnificent pandals (temporary structures) that are works of art in themselves. The festival signifies the victory of good over evil, with the goddess defeating the buffalo demon Mahishasura. It is a time for family gatherings, feasting, and the celebration of womanhood and divine power.",
                image_url=url_for('static', filename='images/durga-puja.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            festival4 = Destination(
                title='Pushkar Camel Fair',
                description="A mesmerizing cultural spectacle in Rajasthan, bringing together thousands of camels, traders, and tourists.",
                long_description="The Pushkar Camel Fair is one of the most unique and spectacular events in India. Held annually in the small town of Pushkar in Rajasthan, it is a bustling five-day affair where thousands of camels, cattle, and horses are traded. Beyond the livestock trading, the fair is a massive cultural festival, featuring camel races, rural sports, and traditional music and dance performances. It offers a fascinating glimpse into the vibrant rural life of Rajasthan and its rich traditions.",
                image_url=url_for('static', filename='images/pushkar.jpg'),
                category='Culture',
                sub_category='Vibrant Festivals'
            )
            
            tradition1 = Destination(
                title='Yoga & Meditation',
                description="The ancient science of Yoga and meditation is a cornerstone of Indian philosophy, promoting physical and mental well-being.",
                long_description="Originating in ancient India, Yoga is a holistic practice that combines physical postures (asanas), breathing techniques (pranayama), and meditation. It is not just an exercise system but a way of life that seeks to harmonize the body, mind, and spirit. It has gained worldwide popularity for its benefits in reducing stress, improving flexibility, and enhancing overall health. This ancient tradition is deeply rooted in Indian philosophy and continues to be a profound path to self-discovery and inner peace.",
                image_url=url_for('static', filename='images/yoga.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            tradition2 = Destination(
                title='Ayurveda',
                description="An ancient system of medicine and life philosophy that emphasizes holistic healing through diet, herbs, and lifestyle.",
                long_description="Ayurveda, which means 'the science of life,' is one of the world's oldest holistic healing systems. Developed in India over 3,000 years ago, it is based on the belief that health and wellness depend on a delicate balance between the mind, body, and spirit. Ayurvedic treatments use a combination of diet, herbal remedies, massage, and lifestyle adjustments to restore this balance. It's a profound tradition that offers a natural and personalized approach to achieving optimal health and preventing disease.",
                image_url=url_for('static', filename='images/ayurveda.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            tradition3 = Destination(
                title='Indian Wedding',
                description="Indian weddings are elaborate, multi-day celebrations filled with rich rituals, vibrant colors, and immense joy.",
                long_description="Indian weddings are much more than a single ceremony; they are a series of elaborate, multi-day celebrations that bring entire families and communities together. Each ritual, from the pre-wedding henna ceremony (Mehendi) to the vibrant main ceremony and reception, is steeped in tradition and symbolism. The celebrations are known for their stunning display of vibrant colors, intricate attire, joyous music, and delicious feasts. They are a true testament to the importance of family, community, and the sanctity of marriage in Indian culture.",
                image_url=url_for('static', filename='images/wedding.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )
            tradition4 = Destination(
                title='Cuisine Traditions',
                description="From family recipes to regional specialities, Indian cuisine is a cherished tradition passed down through generations.",
                long_description="Indian culinary traditions are a cherished part of the nation's cultural heritage. Cooking is often seen as a form of art, with recipes and techniques passed down through generations. The traditions emphasize the use of fresh, local ingredients and a meticulous balance of flavors. From the grand feasts prepared for festivals to the simple, comforting meals of daily life, Indian cuisine is an expression of hospitality, love, and a deep connection to the land and its seasons.",
                image_url=url_for('static', filename='images/cuisine-tradition.jpg'),
                category='Culture',
                sub_category='Rich Traditions'
            )

            art1 = Destination(
                title='Classical Dances',
                description='Experience the beauty and grace of classical Indian dance forms like Bharatanatyam and Kathak.',
                long_description="Indian classical dances are ancient art forms that combine intricate footwork, expressive gestures, and powerful storytelling. Each dance style, such as Bharatanatyam, Kathak, and Odissi, originated in a specific region and has its own unique grammar, music, and costume. These dances are not just performances but a form of spiritual expression, often narrating mythological tales and devotion to deities. They are a beautiful testament to India's rich artistic heritage.",
                image_url=url_for('static', filename='images/dance.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            art2 = Destination(
                title='Textile Craftsmanship',
                description='Discover the intricate art of Indian textiles, from silk weaving to vibrant block prints.',
                long_description="India's textile craftsmanship is world-renowned for its intricacy, vibrant colors, and diversity. From the rich silks of Banaras to the intricate block prints of Rajasthan and the delicate embroidery of Kashmir, each region has developed its own unique textile traditions. These crafts are often passed down through generations of artisans, who use age-old techniques to create stunning fabrics. Indian textiles are not just clothing; they are a form of art that reflects the nation's history, culture, and regional identities.",
                image_url=url_for('static', filename='images/textile.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            art3 = Destination(
                title='Indian Music',
                description='Get lost in the soulful melodies of classical Indian music, from the sitar to tabla.',
                long_description="Indian music is a rich and soulful tradition with roots that stretch back thousands of years. It is broadly categorized into two major styles: North Indian Hindustani and South Indian Carnatic music. These traditions are based on the system of 'Ragas' (melodic frameworks) and 'Talas' (rhythmic cycles). From the haunting melodies of the sitar to the complex beats of the tabla, Indian music is an intricate and deeply spiritual art form that has captivated audiences around the world.",
                image_url=url_for('static', filename='images/music.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            art4 = Destination(
                title='Art & Architecture',
                description='Marvel at the stunning blend of art and architecture in India’s ancient temples and monuments.',
                long_description="India's art and architecture are a grand reflection of its layered history and diverse cultures. From the ancient rock-cut temples of Ajanta and Ellora to the magnificent Mughal forts and palaces and the intricate carvings of Hindu temples, each architectural style tells a unique story. The buildings are not merely structures but works of art, adorned with detailed sculptures, frescoes, and paintings that bring myths and legends to life. They stand as a testament to the country's profound artistic and engineering legacy.",
                image_url=url_for('static', filename='images/architecture.jpg'),
                category='Culture',
                sub_category='Diverse Arts'
            )
            
            # --- History Destinations ---
            history_highlight1 = Destination(
                title='Ancient Forts & Palaces',
                description='Explore the majestic forts and opulent palaces that tell a tale of India\'s royal past.',
                long_description="India's landscape is dotted with magnificent forts and opulent palaces that stand as silent witnesses to its glorious royal past. These architectural marvels, such as the Amber Fort in Jaipur and the Mysore Palace, are not just structures but epic tales of courage, power, and art. They reflect the unique blend of different architectural styles—from Rajput and Mughal to British—and offer a glimpse into the luxurious lives of the rulers who once inhabited them. Each fort and palace holds centuries of history within its walls.",
                image_url=url_for('static', filename='images/history.jpg'),
                category='History'
            )
            history_highlight2 = Destination(
                title='The Taj Mahal',
                description='The iconic monument of love, a masterpiece of Mughal architecture and one of the new wonders of the world.',
                long_description="The Taj Mahal is an ivory-white marble mausoleum on the south bank of the Yamuna river in the Indian city of Agra. It was commissioned in 1631 by the Mughal emperor, Shah Jahan, to house the tomb of his favorite wife, Mumtaz Mahal. The Taj Mahal is widely considered the most beautiful example of Mughal architecture, a style that combines elements from Persian, Ottoman Turkish, Indian, and Islamic architectural styles. It is a symbol of eternal love and is one of the most famous and recognizable structures in the world.",
                image_url=url_for('static', filename='images/taj-mahal.jpg'),
                category='History'
            )
            history_highlight3 = Destination(
                title='Historical City Tours',
                description='Walk through the vibrant lanes of ancient cities like Delhi and Jaipur, each narrating a unique historical saga.',
                long_description="Ancient cities like Delhi and Jaipur are living museums, with every street and alley narrating a story from a bygone era. A historical city tour allows you to walk through centuries of history, from the narrow lanes of Old Delhi with its Mughal-era monuments to the majestic palaces and vibrant bazaars of the 'Pink City,' Jaipur. These tours offer a rich, immersive experience, combining the tales of emperors and battles with the colorful hustle and bustle of modern city life.",
                image_url=url_for('static', filename='images/city-tour.jpg'),
                category='History'
            )
            history_highlight4 = Destination(
                title='Architectural Ruins',
                description='Uncover the secrets of a bygone era by visiting the impressive and intricate ruins of ancient empires.',
                long_description="India is home to countless architectural ruins that stand as testaments to the country's ancient and powerful empires. Sites like the ruins of Hampi, once the capital of the Vijayanagara Empire, or the ancient city of Nalanda, a famous center of learning, offer a profound glimpse into a lost world. These ruins are not just crumbling stones; they are living histories that invite you to imagine the lives, beliefs, and artistic brilliance of the people who built them.",
                image_url=url_for('static', filename='images/ruins.jpg'),
                category='History'
            )
            
            # --- Nature Destinations ---
            nature_highlight1 = Destination(
                title='Himalayan Landscapes',
                description='Discover the breathtaking beauty of the Himalayas, from snowy peaks to lush valleys.',
                long_description="The Himalayas, a majestic mountain range that forms a natural border with India, are a land of breathtaking landscapes and profound spirituality. From the towering, snow-capped peaks and serene glacial lakes to the lush green valleys and vibrant alpine meadows, the Himalayas offer an unparalleled experience for adventurers and seekers of peace. This region is home to some of the world's highest peaks, including Mount Everest, and is revered as the abode of gods, making it a place of both stunning natural beauty and deep cultural significance.",
                image_url=url_for('static', filename='images/nature.jpg'),
                category='Nature'
            )
            nature_highlight2 = Destination(
                title='Tropical Backwaters',
                description='Experience the serene beauty of Kerala\'s backwaters on a traditional houseboat journey.',
                long_description="The backwaters of Kerala are a unique ecosystem of interconnected canals, lakes, and lagoons, running parallel to the Arabian Sea. A journey on a traditional houseboat through these tranquil waters is a mesmerizing experience. The serene landscapes are lined with lush greenery, swaying coconut palms, and charming villages. It offers a peaceful escape and a chance to witness the unique rural life of Kerala, from fishermen at work to locals going about their daily routines, all set against a backdrop of serene natural beauty.",
                image_url=url_for('static', filename='images/backwaters.jpg'),
                category='Nature'
            )
            nature_highlight3 = Destination(
                title='Wildlife Sanctuaries',
                description='Get up close with India\'s diverse wildlife, including tigers, elephants, and rare bird species.',
                long_description="India is home to a rich and diverse range of wildlife, protected in numerous national parks and sanctuaries. These areas are crucial for the conservation of endangered species like the Bengal tiger, Asiatic lion, and one-horned rhinoceros. A safari through places like Ranthambore or Periyar offers an exhilarating opportunity to see these animals in their natural habitats. The sanctuaries are also home to a wide variety of bird species, making them a paradise for birdwatchers and nature photographers.",
                image_url=url_for('static', filename='images/wildlife.jpg'),
                category='Nature'
            )
            nature_highlight4 = Destination(
                title='Desert Wonders',
                description='Explore the vast and stunning Thar Desert on a camel safari, witnessing golden sand dunes and vibrant culture.',
                long_description="The Thar Desert, also known as the Great Indian Desert, is a vast, arid region in the northwestern part of India. Despite its harsh climate, the desert is a land of stunning beauty and unique culture. A camel safari is the perfect way to explore its endless golden sand dunes, witness spectacular sunsets, and experience the traditional desert life of Rajasthan. The region is also home to vibrant folk music, dance, and colorful festivals, making the desert a truly enchanting and unforgettable destination.",
                image_url=url_for('static', filename='images/desert.jpg'),
                category='Nature'
            )
            
            # --- Cuisine Destinations ---
            cuisine1 = Destination(
                title='Indian Sweets',
                description='Indulge in a variety of traditional Indian desserts and sweets from different regions.',
                long_description="Indian sweets, or 'mithai,' are an essential part of every festival, celebration, and joyous occasion. Each region has its own unique specialties, from the creamy 'Rasgullas' of Bengal to the rich, layered 'Mysore Pak' of Karnataka and the beloved 'Gulab Jamuns' found across the country. Made with ingredients like milk, sugar, ghee, and nuts, these desserts are often a beautiful blend of flavors and textures. They are not just food but a symbol of happiness, hospitality, and celebration in Indian culture.",
                image_url=url_for('static', filename='images/sweets.jpg'),
                category='Cuisine',
                sub_category='Sweets'
            )
            cuisine2 = Destination(
                title='North Indian Dishes',
                description='Explore the rich and creamy curries, breads, and tandoori dishes of North India.',
                long_description="North Indian cuisine is celebrated for its rich, aromatic, and comforting flavors. The food is often characterized by the use of dairy products like milk, yogurt, and paneer, as well as a variety of spices. Signature dishes include creamy curries like Butter Chicken and Shahi Paneer, accompanied by a wide range of breads like Naan and Roti cooked in a Tandoor (clay oven). The cuisine is a flavorful journey that showcases a blend of tradition and regional influences, leaving a lasting impression on your palate.",
                image_url=url_for('static', filename='images/north-indian.jpg'),
                category='Cuisine',
                sub_category='North Indian'
            )
            cuisine3 = Destination(
                title='South Indian Dishes',
                description='Discover the flavorful and spicy dishes, dosas, and idlis from South India.',
                long_description="South Indian cuisine is a delightful world of vibrant flavors and fresh ingredients. The dishes are typically lighter and often feature a generous use of coconut, tamarind, and curry leaves. You'll find a variety of rice-based preparations like the savory `Dosa` (a thin crepe) and fluffy `Idli` (steamed rice cakes), usually served with a spicy lentil stew called `Sambar` and coconut chutney. This cuisine is known for its perfect balance of tangy, spicy, and savory notes that awaken the senses.",
                image_url=url_for('static', filename='images/south-indian.jpg'),
                category='Cuisine',
                sub_category='South Indian'
            )
            cuisine4 = Destination(
                title='Indian Street Food',
                description='Savor the vibrant and diverse flavors of India\'s popular street food, from chaat to pakoras.',
                long_description="Indian street food is a culinary adventure, offering a quick and flavorful glimpse into the country's diverse tastes. From the tangy and spicy `Chaat` (a savory snack) to crispy `Samosas` and fried `Pakoras`, every street corner offers a new and exciting dish. The street food culture is a vibrant part of daily life, where vendors prepare fresh, delicious snacks on the spot. It's an experience that is as much about the bustling atmosphere as it is about the incredible flavors.",
                image_url=url_for('static', filename='images/street-food.jpg'),
                category='Cuisine',
                sub_category='Street Food'
            )
            cuisine5 = Destination(
                title='Thali Meals',
                description='Experience a complete and balanced meal on a single plate, featuring a variety of regional dishes.',
                long_description="A `Thali` is a traditional Indian meal composed of a variety of dishes served on a single platter. The concept is to offer a balanced meal with all six tastes—sweet, salty, bitter, sour, astringent, and spicy—on one plate. A typical Thali includes a selection of curries, lentils, vegetables, rice, and bread, often accompanied by yogurt, a sweet dish, and a pickle. It's a culinary tour of a region's flavors, providing a complete and wholesome dining experience.",
                image_url=url_for('static', filename='images/thali.jpg'),
                category='Cuisine',
                sub_category='Thali Meals'
            )
            cuisine6 = Destination(
                title='Spices of India',
                description='Learn about the aromatic spices that are the heart and soul of Indian cooking.',
                long_description="Spices are the heart and soul of Indian cooking, giving the cuisine its unique and complex flavors. India is known as the 'land of spices,' with a wide variety of spices like turmeric, cumin, cardamom, and cloves being cultivated and used for centuries. These spices not only enhance the taste of food but also have significant medicinal and health benefits. The art of blending and roasting these spices to create a perfect `masala` is a skill passed down through generations, making every dish a masterpiece of flavor.",
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
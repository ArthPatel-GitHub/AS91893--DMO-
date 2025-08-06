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
    sub_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Destination('{self.title}', '{self.category}')"

class CarouselImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(200), nullable=False)
    caption = db.Column(db.String(100), nullable=True)
    sub_category = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"CarouselImage('{self.image_url}')"

@app.route('/')
def home():
    destinations = Destination.query.filter(Destination.category != 'Hero').all()
    hero_image = Destination.query.filter_by(category='Hero').first()
    
    culture_carousel_images = CarouselImage.query.filter_by(sub_category='Culture Carousel').all()
    history_carousel_images = CarouselImage.query.filter_by(sub_category='History Carousel').all()
    nature_carousel_images = CarouselImage.query.filter_by(sub_category='Nature Carousel').all()
    
    return render_template('index.html', destinations=destinations, hero_image=hero_image, 
                           culture_carousel_images=culture_carousel_images,
                           history_carousel_images=history_carousel_images,
                           nature_carousel_images=nature_carousel_images)

@app.route('/culture')
def culture():
    destinations = Destination.query.filter_by(category='Culture').all()
    vibrant_festivals_images = CarouselImage.query.filter_by(sub_category='Vibrant Festivals').all()
    rich_traditions_images = CarouselImage.query.filter_by(sub_category='Rich Traditions').all()
    diverse_arts_images = CarouselImage.query.filter_by(sub_category='Diverse Arts').all()
    return render_template('culture.html', 
                           destinations=destinations, 
                           vibrant_festivals_images=vibrant_festivals_images,
                           rich_traditions_images=rich_traditions_images,
                           diverse_arts_images=diverse_arts_images)

@app.route('/cuisine')
def cuisine():
    carousel_images = CarouselImage.query.filter(CarouselImage.sub_category==None).all()
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

@app.route('/details/<string:title>')
def details(title):
    item = Destination.query.filter_by(title=title).first_or_404()
    related_items = Destination.query.filter_by(sub_category=item.sub_category).all()
    return render_template('details.html', item=item, related_items=related_items)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not Destination.query.first():
            print("Database is empty. Adding initial data...")
            
            hero_photo = Destination(
                title='Hero Section',
                description='High-resolution photo for the main banner.',
                image_url=url_for('static', filename='images/hero-image.jpg'),
                category='Hero'
            )
            
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
            
            festivals_img1 = CarouselImage(image_url=url_for('static', filename='images/festivals-carousel-1.jpg'), caption='Holi, the festival of colours.', sub_category='Vibrant Festivals')
            festivals_img2 = CarouselImage(image_url=url_for('static', filename='images/festivals-carousel-2.jpg'), caption='Diwali, the festival of lights.', sub_category='Vibrant Festivals')
            festivals_img3 = CarouselImage(image_url=url_for('static', filename='images/festivals-carousel-3.jpg'), caption='Pushkar Camel Fair.', sub_category='Vibrant Festivals')

            traditions_img1 = CarouselImage(image_url=url_for('static', filename='images/traditions-carousel-1.jpg'), caption='Ayurvedic wellness practices.', sub_category='Rich Traditions')
            traditions_img2 = CarouselImage(image_url=url_for('static', filename='images/traditions-carousel-2.jpg'), caption='Traditional Indian wedding.', sub_category='Rich Traditions')
            traditions_img3 = CarouselImage(image_url=url_for('static', filename='images/traditions-carousel-3.jpg'), caption='Yoga & Meditation.', sub_category='Rich Traditions')

            arts_img1 = CarouselImage(image_url=url_for('static', filename='images/arts-carousel-1.jpg'), caption='Classical Indian dance.', sub_category='Diverse Arts')
            arts_img2 = CarouselImage(image_url=url_for('static', filename='images/arts-carousel-2.jpg'), caption='Textile craftsmanship.', sub_category='Diverse Arts')
            arts_img3 = CarouselImage(image_url=url_for('static', filename='images/arts-carousel-3.jpg'), caption='Indian classical music.', sub_category='Diverse Arts')
            
            # --- New carousel images for homepage categories ---
            culture_carousel_img1 = CarouselImage(image_url=url_for('static', filename='images/culture-hero.jpg'), caption='Celebrating the festival of colors.', sub_category='Culture Carousel')
            culture_carousel_img2 = CarouselImage(image_url=url_for('static', filename='images/diwali.jpg'), caption='Lights and celebration.', sub_category='Culture Carousel')
            culture_carousel_img3 = CarouselImage(image_url=url_for('static', filename='images/wedding.jpg'), caption='A traditional Indian wedding.', sub_category='Culture Carousel')
            
            history_carousel_img1 = CarouselImage(image_url=url_for('static', filename='images/history-hero.jpg'), caption='Majestic forts and palaces.', sub_category='History Carousel')
            history_carousel_img2 = CarouselImage(image_url=url_for('static', filename='images/taj-mahal.jpg'), caption='The iconic Taj Mahal.', sub_category='History Carousel')
            history_carousel_img3 = CarouselImage(image_url=url_for('static', filename='images/ruins.jpg'), caption='Ancient ruins and architecture.', sub_category='History Carousel')
            
            nature_carousel_img1 = CarouselImage(image_url=url_for('static', filename='images/nature-hero.jpg'), caption='The beauty of the Himalayas.', sub_category='Nature Carousel')
            nature_carousel_img2 = CarouselImage(image_url=url_for('static', filename='images/backwaters.jpg'), caption='Serene tropical backwaters.', sub_category='Nature Carousel')
            nature_carousel_img3 = CarouselImage(image_url=url_for('static', filename='images/wildlife.jpg'), caption='India\'s diverse wildlife.', sub_category='Nature Carousel')
            
            db.session.add(hero_photo)
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
            db.session.add(cuisine_photo1)
            db.session.add(cuisine_photo2)
            db.session.add(cuisine_photo3)
            
            db.session.add(festivals_img1)
            db.session.add(festivals_img2)
            db.session.add(festivals_img3)
            db.session.add(traditions_img1)
            db.session.add(traditions_img2)
            db.session.add(traditions_img3)
            db.session.add(arts_img1)
            db.session.add(arts_img2)
            db.session.add(arts_img3)

            db.session.add(culture_carousel_img1)
            db.session.add(culture_carousel_img2)
            db.session.add(culture_carousel_img3)
            db.session.add(history_carousel_img1)
            db.session.add(history_carousel_img2)
            db.session.add(history_carousel_img3)
            db.session.add(nature_carousel_img1)
            db.session.add(nature_carousel_img2)
            db.session.add(nature_carousel_img3)

            db.session.commit()
            print("Initial data added.")
            
    app.run(debug=True)
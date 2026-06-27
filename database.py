import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'am_trader.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            image_filename TEXT,
            is_bestseller INTEGER DEFAULT 0,
            unit TEXT DEFAULT '100g'
        );

        CREATE TABLE IF NOT EXISTS enquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT,
            product_interest TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()

    # Seed products only if table is empty
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:
        products = [
            # (name, category, description, image_filename, is_bestseller, unit)
            (
                'Premium Black Tea',
                'Tea',
                'Rich, full-bodied Assam black tea with a bold malty flavour. Perfect for a classic morning brew with milk.',
                'Tea.jpg',
                1,
                '250g'
            ),
            (
                'Green Tea',
                'Tea',
                'Hand-picked premium green tea leaves with a delicate, grassy aroma and antioxidant-rich benefits.',
                'Green Tea.jpg',
                1,
                '100g'
            ),
            (
                'Black Pepper',
                'Spice',
                'Whole black peppercorns with a sharp, pungent aroma. Freshly ground to elevate every dish.',
                'Black Papper.jpg',
                1,
                '200g'
            ),
            (
                'Black Salt (Kala Namak)',
                'Spice',
                'Natural volcanic black salt with a distinctive sulphurous aroma, used in chutneys, chaats, and ayurvedic recipes.',
                'Black Salt.jpg',
                0,
                '250g'
            ),
            (
                'Aamchur Powder',
                'Spice',
                'Sun-dried raw mango powder with a tangy, fruity sourness – the secret ingredient for authentic Indian street food.',
                'Aamchur Powder.jpg',
                0,
                '100g'
            ),
            (
                'Coriander Powder',
                'Spice',
                'Freshly ground coriander seeds with a warm, citrusy flavour. A staple spice in Indian, Middle Eastern, and Mexican cuisine.',
                'Coriandar Powder.jpg',
                0,
                '200g'
            ),
            (
                'Cumin Powder',
                'Spice',
                'Stone-ground cumin with an earthy, nutty aroma that forms the backbone of countless spice blends and curries.',
                'Cumin Powder.jpg',
                1,
                '100g'
            ),
            (
                'Garam Masala',
                'Spice',
                'A warm, aromatic blend of whole spices – cinnamon, cardamom, cloves, and more – slow-roasted and ground in-house.',
                'Garam Masala.jpg',
                1,
                '100g'
            ),
            (
                'Red Chilli Powder',
                'Spice',
                'Vibrant, fiery red chilli powder made from sun-dried Kashmiri and Byadgi chillies. Adds colour and heat.',
                'Red Chilli Powder.jpg',
                0,
                '200g'
            ),
            (
                'Turmeric Powder',
                'Spice',
                'Pure, high-curcumin turmeric root powder with an intense golden colour and earthy, slightly bitter taste.',
                'Turmeric Powder.jpg',
                1,
                '200g'
            ),
        ]

        cursor.executemany(
            "INSERT INTO products (name, category, description, image_filename, is_bestseller, unit) VALUES (?, ?, ?, ?, ?, ?)",
            products
        )
        conn.commit()
        print(f"[OK] Seeded {len(products)} products.")
    else:
        print(f"[INFO] Database already has {count} products. Skipping seed.")

    conn.close()
    print("[OK] Database initialized successfully.")

if __name__ == '__main__':
    init_db()

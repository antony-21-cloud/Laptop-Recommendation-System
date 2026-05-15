from app import app, db
from models import Laptop

def seed_database():
    with app.app_context():
        # Clear existing laptops to avoid duplicates
        db.session.query(Laptop).delete()


        laptops = [
            # Ryzen 7 Machines (High Performance)
            # We map model/processor/ram into 'name' and 'specs'
            Laptop(
                name="HP EliteBook 845 G8", 
                processor_type="Ryzen 7",
                specs="Ryzen 7, 16GB RAM, 512GB SSD", 
                price=85000, 
                seller_id=1  # Every laptop needs a seller ID from your User table
            ),
            Laptop(
                name="Lenovo Legion 5", 
                processor_type="Ryzen 7",
                specs="Ryzen 7, 16GB RAM, 1TB SSD", 
                price=125000, 
                seller_id=1
            ),
            Laptop(
                name="MacBook Air M2", 
                processor_type="M2",
                specs="M2 Chip, 8GB RAM, 256GB SSD", 
                price=135000, 
                seller_id=1
            ),
            Laptop(                 
                name="ASUS ROG Zephyrus G14",
                processor_type="Ryzen 7",
                specs="Ryzen 7, 16GB RAM, 1TB SSD",
                price=150000,
                seller_id=1
            ),
            Laptop(
                name="Dell XPS 15",
                processor_type="Core i7",
                specs="Core i7, 16GB RAM, 512GB SSD",
                price=140000,
                seller_id=1
            ),
            Laptop(
                name="Dell Latitude 5420",
                processor_type="Core i7",
                specs="Core i7, 16GB RAM, 512GB SSD",
                price=75000,
                seller_id=1
            ),
            Laptop(
                name="HP Pavilion 15",
                processor_type="Core i5",
                specs="Core i5, 8GB RAM, 256GB SSD",
                price=55000,
                seller_id=1
            ),
            Laptop(
                name="Microsoft Surface Laptop 4",
                processor_type="Core i7",
                specs="Core i7, 16GB RAM, 512GB SSD",
                price=110000,
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkPad E15",
                processor_type="Core i5",
                specs="Core i5, 8GB RAM, 256GB SSD",
                price=60000,
                seller_id=1
            ),
            Laptop(
                name="Acer Aspire 5",
                processor_type="Core i3",
                specs="Core i3, 8GB RAM, 256GB SSD",
                price=40000,
                seller_id=1
            ),
            # MacBooks (M-Series)
            Laptop(
                name="MacBook Air M2",
                processor_type="M2",
                specs="M2 Chip, 8GB RAM, 256GB SSD",
                price=135000,
                seller_id=1
            ),
            Laptop(
                name="MacBook Pro M3",
                processor_type="M3",
                specs="M3 Chip, 18GB RAM, 512GB SSD",
                price=260000,
                seller_id=1
            ),

            # Budget Friendly (Kenya Market Favorites)
            Laptop(
                name="Lenovo IdeaPad 3",
                processor_type="Core i3",
                specs="Core i3, 4GB RAM, 1TB HDD",
                price=35000,
                seller_id=1
            ),
            Laptop(
                name="HP 250 G8",
                processor_type="Core i3",
                specs="Core i3, 8GB RAM, 256GB SSD",
                price=42000,
                seller_id=1
            ),

            # Add 10 more to reach the 20 mark
            Laptop(
                name="Acer Swift 3",
                processor_type="Ryzen 5",
                specs="Ryzen 5, 8GB RAM, 512GB SSD",
                price=62000,
                seller_id=1
            ),
            Laptop(
                name="HP Victus 16",
                processor_type="Ryzen 7",
                specs="Ryzen 7, 16GB RAM, 512GB SSD",
                price=105000,
                seller_id=1
            ),
            Laptop(
                name="Dell XPS 13",
                processor_type="Core i7",
                specs="Core i7, 16GB RAM, 512GB SSD",
                price=145000,
                seller_id=1
            ),
            Laptop(
                name="Huawei MateBook D15",
                processor_type="Core i5",
                specs="Core i5, 8GB RAM, 512GB SSD",
                price=68000,
                seller_id=1
            ),
            Laptop(
                name="Samsung Galaxy Book 3",
                processor_type="Core i7",
                specs="Core i7, 16GB RAM, 1TB SSD",
                price=130000,
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkPad X1 Carbon",
                processor_type="Core i7",
                specs="Core i7, 16GB RAM, 512GB SSD",
                price=160000,
                seller_id=1
            ),
            Laptop(
                name="HP Envy x360",
                processor_type="Ryzen 5",
                specs="Ryzen 5, 12GB RAM, 512GB SSD",
                price=88000,
                seller_id=1
            ),
            Laptop(
                name="ASUS Vivobook 15",
                processor_type="Core i5",
                specs="Core i5, 8GB RAM, 512GB SSD",
                price=58000,
                seller_id=1
            ),
                        Laptop(
                name="HP EliteBook 845 G8", 
                processor_type="Ryzen 7",
                specs="Ryzen 7, 16GB RAM, 512GB SSD", 
                price=85000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo Legion 5", 
                processor_type="Ryzen 7",
                specs="Ryzen 7, 16GB RAM, 1TB SSD", 
                price=125000, 
                seller_id=1
            ),
            Laptop(
                name="MacBook Air M2", 
                processor_type="M2",
                specs="Apple M2, 8GB RAM, 256GB SSD", 
                price=145000, 
                seller_id=1
            ),
            Laptop(
                name="Dell XPS 13 9315", 
                processor_type="Core i7",
                specs="i7-1250U, 16GB RAM, 512GB SSD", 
                price=165000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS ROG Zephyrus G14", 
                processor_type="Ryzen 9",
                specs="Ryzen 9, 32GB RAM, 1TB SSD, RTX 3060", 
                price=195000, 
                seller_id=1
            ),
            Laptop(
                name="HP Pavilion 15", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 512GB SSD", 
                price=68000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Swift 3", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 5500U, 8GB RAM, 256GB SSD", 
                price=55000, 
                seller_id=1
            ),
            Laptop(
                name="Microsoft Surface Laptop 5", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 256GB SSD", 
                price=135000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkPad X1 Carbon Gen 10", 
                processor_type="Core i7",
                specs="i7-1260P, 16GB RAM, 512GB SSD", 
                price=210000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Katana GF66", 
                processor_type="Core i7",
                specs="i7-12700H, 16GB RAM, 512GB SSD, RTX 3050Ti", 
                price=115000, 
                seller_id=1
            ),
            Laptop(
                name="Apple MacBook Pro 14", 
                processor_type="M2 Pro",
                specs="M2 Pro, 16GB RAM, 512GB SSD", 
                price=280000, 
                seller_id=1
            ),
            Laptop(
                name="HP Victus 16", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 5600H, 16GB RAM, 512GB SSD, RTX 3050", 
                price=95000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Inspiron 15 3520", 
                processor_type="Core i3",
                specs="i3-1215U, 8GB RAM, 256GB SSD", 
                price=48000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Vivobook 16X", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 5800H, 12GB RAM, 512GB SSD", 
                price=78000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Nitro 5", 
                processor_type="Core i5",
                specs="i5-12500H, 16GB RAM, 512GB SSD, RTX 3050", 
                price=105000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo IdeaPad Slim 3", 
                processor_type="Ryzen 3",
                specs="Ryzen 3 5300U, 8GB RAM, 256GB SSD", 
                price=42000, 
                seller_id=1
            ),
            Laptop(
                name="Samsung Galaxy Book 3", 
                processor_type="Core i7",
                specs="i7-1355U, 16GB RAM, 512GB SSD", 
                price=155000, 
                seller_id=1
            ),
            Laptop(
                name="Razer Blade 15", 
                processor_type="Core i7",
                specs="i7-12800H, 16GB RAM, 1TB SSD, RTX 3070Ti", 
                price=320000, 
                seller_id=1
            ),
            Laptop(
                name="Gigabyte G5", 
                processor_type="Core i5",
                specs="i5-12500H, 8GB RAM, 512GB SSD, RTX 4050", 
                price=110000, 
                seller_id=1
            ),
            Laptop(
                name="LG Gram 17", 
                processor_type="Core i7",
                specs="i7-1360P, 16GB RAM, 1TB SSD", 
                price=185000, 
                seller_id=1
            ),
            Laptop(
                name="HP Envy x360", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 7530U, 16GB RAM, 512GB SSD, Touch", 
                price=92000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Vostro 3420", 
                processor_type="Core i5",
                specs="i5-1135G7, 8GB RAM, 512GB SSD", 
                price=64000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Zenbook 14", 
                processor_type="Core i7",
                specs="i7-1360P, 16GB RAM, 512GB SSD, OLED", 
                price=142000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo Yoga 7i", 
                processor_type="Core i5",
                specs="i5-1335U, 16GB RAM, 512GB SSD, Touch", 
                price=118000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Aspire 5", 
                processor_type="Core i5",
                specs="i5-1335U, 16GB RAM, 512GB SSD", 
                price=72000, 
                seller_id=1
            ),
            Laptop(
                name="Huawei MateBook D15", 
                processor_type="Core i5",
                specs="i5-1135G7, 8GB RAM, 512GB SSD", 
                price=67000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Precision 3571", 
                processor_type="Core i7",
                specs="i7-12700H, 32GB RAM, 1TB SSD, RTX A1000", 
                price=245000, 
                seller_id=1
            ),
            Laptop(
                name="HP ProBook 450 G9", 
                processor_type="Core i7",
                specs="i7-1255U, 16GB RAM, 512GB SSD", 
                price=108000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo LOQ 15", 
                processor_type="Core i5",
                specs="i5-13420H, 16GB RAM, 512GB SSD, RTX 3050", 
                price=112000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Prestige 14", 
                processor_type="Core i7",
                specs="i7-1260P, 16GB RAM, 512GB SSD", 
                price=128000, 
                seller_id=1
            ),
            Laptop(
                name="Apple MacBook Air M1", 
                processor_type="M1",
                specs="Apple M1, 8GB RAM, 256GB SSD", 
                price=115000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS TUF Gaming F15", 
                processor_type="Core i7",
                specs="i7-12700H, 16GB RAM, 512GB SSD, RTX 4060", 
                price=148000, 
                seller_id=1
            ),
            Laptop(
                name="HP Omen 16", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 6800H, 16GB RAM, 1TB SSD, RTX 3060", 
                price=155000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkPad E14", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 5625U, 8GB RAM, 256GB SSD", 
                price=74000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Latitude 5430", 
                processor_type="Core i5",
                specs="i5-1235U, 16GB RAM, 512GB SSD", 
                price=118000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Predator Helios 300", 
                processor_type="Core i7",
                specs="i7-12700H, 16GB RAM, 1TB SSD, RTX 3070", 
                price=175000, 
                seller_id=1
            ),
            Laptop(
                name="Microsoft Surface Pro 9", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 256GB SSD, Tablet", 
                price=125000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Vivobook Go 15", 
                processor_type="Ryzen 3",
                specs="Ryzen 3 7320U, 8GB RAM, 256GB SSD", 
                price=45000, 
                seller_id=1
            ),
            Laptop(
                name="HP EliteBook 640 G9", 
                processor_type="Core i5",
                specs="i5-1235U, 16GB RAM, 512GB SSD", 
                price=95000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo Legion Pro 7i", 
                processor_type="Core i9",
                specs="i9-13900HX, 32GB RAM, 2TB SSD, RTX 4080", 
                price=420000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Modern 15", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 7530U, 16GB RAM, 512GB SSD", 
                price=71000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Alienware m15 R7", 
                processor_type="Core i7",
                specs="i7-12700H, 16GB RAM, 512GB SSD, RTX 3060", 
                price=215000, 
                seller_id=1
            ),
            Laptop(
                name="Apple MacBook Pro 16", 
                processor_type="M2 Max",
                specs="M2 Max, 32GB RAM, 1TB SSD", 
                price=450000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS ExpertBook B1", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 512GB SSD", 
                price=82000, 
                seller_id=1
            ),
            Laptop(
                name="HP 250 G9", 
                processor_type="Core i3",
                specs="i3-1215U, 8GB RAM, 512GB SSD", 
                price=49000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo IdeaPad Gaming 3", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 6600H, 8GB RAM, 512GB SSD, RTX 3050", 
                price=98000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Swift Edge", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 6800U, 16GB RAM, 1TB SSD, 4K OLED", 
                price=158000, 
                seller_id=1
            ),
            Laptop(
                name="Dell XPS 15 9530", 
                processor_type="Core i9",
                specs="i9-13900H, 32GB RAM, 1TB SSD, RTX 4070", 
                price=360000, 
                seller_id=1
            ),
            Laptop(
                name="Gigabyte Aero 16", 
                processor_type="Core i7",
                specs="i7-13700H, 16GB RAM, 1TB SSD, OLED", 
                price=230000, 
                seller_id=1
            ),
            Laptop(
                name="Huawei MateBook X Pro", 
                processor_type="Core i7",
                specs="i7-1260P, 16GB RAM, 1TB SSD, Touch", 
                price=210000, 
                seller_id=1
            ),
            Laptop(
                name="HP Chromebook 14", 
                processor_type="Celeron",
                specs="Celeron N4500, 4GB RAM, 64GB eMMC", 
                price=28000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo IdeaPad Flex 5", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 5700U, 16GB RAM, 512GB SSD, Touch", 
                price=89000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS ROG Strix G16", 
                processor_type="Core i7",
                specs="i7-13650HX, 16GB RAM, 512GB SSD, RTX 4050", 
                price=165000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Inspiron 14 7430", 
                processor_type="Core i5",
                specs="i5-1335U, 8GB RAM, 512GB SSD, 2-in-1", 
                price=105000, 
                seller_id=1
            ),
            Laptop(
                name="Acer TravelMate P2", 
                processor_type="Core i5",
                specs="i5-1135G7, 8GB RAM, 512GB SSD", 
                price=62000, 
                seller_id=1
            ),
            Laptop(
                name="Samsung Galaxy Book 3 Ultra", 
                processor_type="Core i9",
                specs="i9-13900H, 32GB RAM, 1TB SSD, RTX 4070", 
                price=380000, 
                seller_id=1
            ),
            Laptop(
                name="HP Pavilion Plus 14", 
                processor_type="Core i7",
                specs="i7-12700H, 16GB RAM, 512GB SSD, OLED", 
                price=118000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkPad T14 Gen 3", 
                processor_type="Core i5",
                specs="i5-1240P, 16GB RAM, 512GB SSD", 
                price=135000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Stealth 15", 
                processor_type="Core i7",
                specs="i7-13620H, 16GB RAM, 1TB SSD, RTX 4060", 
                price=185000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Vivobook S 14", 
                processor_type="Core i5",
                specs="i5-12500H, 8GB RAM, 512GB SSD", 
                price=85000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Latitude 7430", 
                processor_type="Core i7",
                specs="i7-1265U, 16GB RAM, 512GB SSD", 
                price=158000, 
                seller_id=1
            ),
            Laptop(
                name="HP Spectre x360 14", 
                processor_type="Core i7",
                specs="i7-1355U, 16GB RAM, 1TB SSD, Touch", 
                price=205000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Aspire 3", 
                processor_type="Ryzen 3",
                specs="Ryzen 3 7320U, 8GB RAM, 512GB SSD", 
                price=46000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkBook 15 G4", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 512GB SSD", 
                price=78000, 
                seller_id=1
            ),
            Laptop(
                name="Apple MacBook Air M2 15", 
                processor_type="M2",
                specs="M2, 16GB RAM, 512GB SSD", 
                price=210000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Zenbook S 13", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 6800U, 16GB RAM, 512GB SSD, OLED", 
                price=145000, 
                seller_id=1
            ),
            Laptop(
                name="Dell G15 5530", 
                processor_type="Core i7",
                specs="i7-13650HX, 16GB RAM, 512GB SSD, RTX 4060", 
                price=142000, 
                seller_id=1
            ),
            Laptop(
                name="HP Victus 15", 
                processor_type="Core i5",
                specs="i5-12450H, 8GB RAM, 512GB SSD, GTX 1650", 
                price=88000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Cyborg 15", 
                processor_type="Core i7",
                specs="i7-12650H, 8GB RAM, 512GB SSD, RTX 4050", 
                price=125000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Nitro 16", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 7840HS, 16GB RAM, 512GB SSD, RTX 4060", 
                price=149000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo IdeaPad Slim 5", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 7530U, 16GB RAM, 512GB SSD", 
                price=82000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Precision 5570", 
                processor_type="Core i7",
                specs="i7-12800H, 32GB RAM, 1TB SSD, RTX A2000", 
                price=310000, 
                seller_id=1
            ),
            Laptop(
                name="HP EliteBook 860 G9", 
                processor_type="Core i7",
                specs="i7-1255U, 16GB RAM, 1TB SSD", 
                price=138000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS ROG Flow X13", 
                processor_type="Ryzen 9",
                specs="Ryzen 9 7940HS, 16GB RAM, 1TB SSD, RTX 4050", 
                price=240000, 
                seller_id=1
            ),
            Laptop(
                name="Microsoft Surface Go 3", 
                processor_type="Pentium Gold",
                specs="Pentium 6500Y, 8GB RAM, 128GB SSD", 
                price=65000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo V15 G3", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 512GB SSD", 
                price=66000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Swift Go 14", 
                processor_type="Core i5",
                specs="i5-1335U, 16GB RAM, 512GB SSD, OLED", 
                price=112000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Vostro 3510", 
                processor_type="Core i3",
                specs="i3-1115G4, 8GB RAM, 256GB SSD", 
                price=44000, 
                seller_id=1
            ),
            Laptop(
                name="HP ProBook 440 G8", 
                processor_type="Core i5",
                specs="i5-1135G7, 8GB RAM, 512GB SSD", 
                price=79000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo Yoga 9i", 
                processor_type="Core i7",
                specs="i7-1360P, 16GB RAM, 1TB SSD, 4K Touch", 
                price=215000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Vivobook 15", 
                processor_type="Core i7",
                specs="i7-1255U, 16GB RAM, 512GB SSD", 
                price=95000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Pulse GL66", 
                processor_type="Core i7",
                specs="i7-12700H, 16GB RAM, 512GB SSD, RTX 3060", 
                price=145000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Aspire Vero", 
                processor_type="Core i5",
                specs="i5-1235U, 12GB RAM, 512GB SSD", 
                price=78000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Inspiron 16 5630", 
                processor_type="Core i7",
                specs="i7-1360P, 16GB RAM, 1TB SSD", 
                price=135000, 
                seller_id=1
            ),
            Laptop(
                name="HP Laptop 15s", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 5500U, 8GB RAM, 512GB SSD", 
                price=62000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo Legion Slim 5", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 7840HS, 16GB RAM, 512GB SSD, RTX 4060", 
                price=155000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Zenbook Pro 14", 
                processor_type="Core i9",
                specs="i9-13900H, 32GB RAM, 1TB SSD, RTX 4070", 
                price=340000, 
                seller_id=1
            ),
            Laptop(
                name="Dell Latitude 3420", 
                processor_type="Core i5",
                specs="i5-1135G7, 8GB RAM, 256GB SSD", 
                price=72000, 
                seller_id=1
            ),
            Laptop(
                name="HP Pavilion Aero 13", 
                processor_type="Ryzen 5",
                specs="Ryzen 5 7535U, 16GB RAM, 512GB SSD", 
                price=94000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo IdeaPad 1", 
                processor_type="Ryzen 3",
                specs="Ryzen 3 7320U, 4GB RAM, 128GB SSD", 
                price=38000, 
                seller_id=1
            ),
            Laptop(
                name="MSI Titan GT77", 
                processor_type="Core i9",
                specs="i9-13980HX, 64GB RAM, 2TB SSD, RTX 4090", 
                price=650000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Swift X", 
                processor_type="Ryzen 7",
                specs="Ryzen 7 5800U, 16GB RAM, 512GB SSD, RTX 3050Ti", 
                price=125000, 
                seller_id=1
            ),
            Laptop(
                name="Dell XPS 17 9730", 
                processor_type="Core i7",
                specs="i7-13700H, 32GB RAM, 1TB SSD, RTX 4070", 
                price=395000, 
                seller_id=1
            ),
            Laptop(
                name="ASUS Chromebook Plus", 
                processor_type="Core i3",
                specs="i3-1215U, 8GB RAM, 128GB SSD", 
                price=58000, 
                seller_id=1
            ),
            Laptop(
                name="HP Envy 17", 
                processor_type="Core i7",
                specs="i7-13700H, 16GB RAM, 512GB SSD", 
                price=145000, 
                seller_id=1
            ),
            Laptop(
                name="Lenovo ThinkPad P15", 
                processor_type="Core i7",
                specs="i7-11800H, 32GB RAM, 1TB SSD, RTX A2000", 
                price=285000, 
                seller_id=1
            ),
            Laptop(
                name="Gigabyte Aorus 15", 
                processor_type="Core i7",
                specs="i7-13700H, 16GB RAM, 1TB SSD, RTX 4060", 
                price=188000, 
                seller_id=1
            ),
            Laptop(
                name="Microsoft Surface Laptop Go 3", 
                processor_type="Core i5",
                specs="i5-1235U, 8GB RAM, 256GB SSD", 
                price=98000, 
                seller_id=1
            ),
            Laptop(
                name="Acer Nitro V 15", 
                processor_type="Core i5",
                specs="i5-13420H, 8GB RAM, 512GB SSD, RTX 2050", 
                price=92000, 
                seller_id=1
            ),
            Laptop(
                name="Samsung Galaxy Book 2 Pro", 
                processor_type="Core i5",
                specs="i5-1240P, 8GB RAM, 512GB SSD", 
                price=110000, 
                seller_id=1
            ),
            Laptop(
                name="Apple MacBook Air M1",
                processor_type="M1",
                specs="M1 Chip, 8GB RAM, 256GB SSD",
                price=95000,
                seller_id=1
            )
        ]

        db.session.bulk_save_objects(laptops)
        db.session.commit()
        print("Success: Laptops added!")

if __name__ == "__main__":
    seed_database()
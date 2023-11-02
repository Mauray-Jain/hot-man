tables = {}

tables["menu"] = (
    "create table `menu`("
    "   `id` int(5) primary key auto_increment,"
    "   `name` varchar(100) not null,"
    "   `category` varchar(20) not null,"
    "   `rate` int(5) not null,"
    "   `quantity_available` int(7) not null"
    ")"
)

menu = [
    ("Paneer Tikka", "Starters", 160, 200),
    ("Dahi Kebab", "Starters", 110, 200),
    ("Hara Bhara Kebab", "Starters", 110, 200),
    ("Masala Chap Tikka", "Starters", 110, 200),
    ("French Fries", "Starters", 130, 200),
    ("Veg Seekh Kebab", "Starters", 130, 200),
    ("Tandoori Aloo", "Starters", 110, 200),
    ("Platter", "Starters", 350, 200),
    ("Pav Bhaji", "Starters", 180, 300),
    ("Vada Pav", "Starters", 100, 200),
    ("Burger", "Starters", 70, 200),

    ("Shahi Paneer", "Subji", 220, 400),
    ("Palak Paneer", "Subji", 200, 300),
    ("Paneer Lababdar", "Subji", 220, 400),
    ("Kadhai Paneer", "Subji", 200, 300),
    ("Paneer Do Pyaza", "Subji", 220, 300),
    ("Paneer Butter Masala", "Subji", 220, 300),
    ("Chhole", "Subji", 180, 300),
    ("Dal Makhni", "Subji", 200, 400),
    ("Maa ki Dal", "Subji", 200, 300),
    ("Dal Tadka", "Subji", 180, 300),
    ("Dum Aaloo", "Subji", 180, 300),

    ("Idli Sambhar", "South Indian", 180, 300),
    ("Masala Dosa", "South Indian", 170, 300),
    ("Sada Dosa", "South Indian", 160, 300),
    ("Uttapam", "South Indian", 180, 300),
    ("Rasam", "South Indian", 80, 100),
    ("Vada", "South Indian", 100, 300),

    ("Out of Stock since COVID", "Chinese", 300, 100),
    ("Chowmein", "Chinese", 150, 300),
    ("Chilli Potato", "Chinese", 170, 300),
    ("Chilli Paneer", "Chinese", 220, 300),
    ("Manchurian", "Chinese", 150, 300),
    ("Steamed Momos", "Chinese", 70, 300),
    ("Tandoori Momos", "Chinese", 70, 300),
    ("Fried Momos", "Chinese", 70, 300),
    ("Paneer Momos", "Chinese", 70, 300),
    ("Steamed Momos", "Chinese", 70, 300),
    ("Steamed Momos", "Chinese", 70, 300),

    ("Rice", "Rice", 100, 300),
    ("Fried Rice", "Rice", 150, 300),
    ("Pulao", "Rice", 180, 300),
    ("Veg Biryani", "Rice", 200, 300),
    ("Chhole Rice", "Rice", 150, 300),

    ("Double Cheese Pizza", "Italian", 250, 300),
    ("Margherita Pizza", "Italian", 200, 300),
    ("Cherry Tomato Pizza", "Italian", 220, 300),
    ("White Pasta", "Italian", 200, 300),
    ("Red Pasta", "Italian", 200, 300),

    ("Rumali Roti", "Breads", 40, 300),
    ("Missi Roti", "Breads", 40, 300),
    ("Tandoori Roti", "Breads", 40, 300),
    ("Aaloo Parantha", "Breads", 60, 300),
    ("Lachha Parantha", "Breads", 60, 300),
    ("Butter Roti", "Breads", 50, 400),
    ("Paneer Parantha", "Breads", 90, 300),
    ("Stuffed Kulcha", "Breads", 90, 300),
]

tables["cart"] = ()

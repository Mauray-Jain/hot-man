tables = {}

tables["menu"] = (
    "create table `menu`("
    "   `id` int(5) primary key auto_increment,"
    "   `name` varchar(20) not null,"
    "   `category` varchar(20) not null,"
    "   `rate` int(5) not null,"
    "   `quantity_available` int(7) not null"
    ")"
)

tables["cart"] = ()

tables["orders"] = ()

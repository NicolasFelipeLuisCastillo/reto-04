#Base class for menu items
class MenuItem:
    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price
    
    def set_name(self, name: str) -> None:
        self._name = name

    def set_price(self, price: float) -> None:
        self._price = price

    def calculate_total(self) -> float:
        return self.price

    def __str__(self) -> str:
        return f"{self._name} : ${self.calculate_total()}"

#Beverage subclass
class Beverage(MenuItem):
    def __init__(self, name: str, price: float, size: str) -> None:
        super().__init__(name, price)
        self._size = size

    def get_size(self) -> str:
        return self._size
    
    def set_size(self, size: str) -> None:
        self._size = size

    def calculate_total(self) -> float:
        if self._size.lower() == "big":
            return self._price * 1.2 #20% extra for big size
        elif self._size.lower() == "normal":
            return self._price
        elif self._size.lower() == "small": 
            return self._price * 0.8 # 20% discount for small size

#Appetizer subclass
class Appetizer(MenuItem):
    def __init__(self, name: str, price: float, is_shared: bool) -> None:
        super().__init__(name, price)
        self._is_shared = is_shared

    def get_is_shared(self) -> bool:
        return self._is_shared
    
    def set_is_shared(self, is_shared: bool) -> None:
        self._is_shared = is_shared

    def calculate_total(self) -> float:
        if self._is_shared:
            return self._price * 0.9 # 10% discount for shared appetizers
        return self._price

#MainCourse subclass
class MainCourse(MenuItem):
    def __init__(self, name: str, price: float, side_dish: str) -> None:
        super().__init__(name, price)
        self._side_dish = side_dish

    def calculate_total(self) -> float:
        if self._side_dish.lower() in ["fries", "special salada"]:
            return self._price + 3.0 # Extra cost for special side dishes
        return self._price
    
    def get_side_dish(self) -> str:
        return self._side_dish
    
    def set_side_dish(self, side_dish: str) -> None:
        self._side_dish = side_dish

class Order:
    def __init__(self) -> None:
        self.items: list = []

    def add_item(self, item: MenuItem) -> None:
        self.items.append(item)

    def calculate_total(self) -> float:
        total = 0
        has_main_course: bool = False

        for item in self.items:
            if isinstance(item, MainCourse): #Check if the item is an instance of MainCourse
                has_main_course = True
                break

        for item in self.items:
            total_item = item.calculate_total()
            if has_main_course and isinstance(item, Beverage): #Check if the item is a beverage
                total_item *= 0.9 #10% of discount on beverages

            total += item.calculate_total()
        return total

    def apply_discount(self) -> float:
        total = self.calculate_total()
        if len(self.items) >= 3:
            return total * 0.9 # 10% discount for orders with 3 or more items
        return total

    def __str__(self) -> str:
        text = "--- Pedido ---\n"
        for item in self.items:
            text += f"{item}\n"
        text += f"Total: ${self.apply_discount()}\n"
        return text
    
class Payment:
    def pay(self, amount: float):
        raise NotImplementedError("Subclasses must implement pay()")


class CardPayment(Payment):
    def __init__(self, card_number: str, cvv: int):
        super().__init__()
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float):
        print(f"Paying ${amount:.2f} with card ending in {self.card_number[-4:]}")


class CashPayment(Payment):
    def __init__(self, cash_given: float):
        super().__init__()
        self.cash_given = cash_given

    def pay(self, amount: float):
        if self.cash_given >= amount:
            print(f"Cash payment made. Change: ${self.cash_given - amount:.2f}")
        else:
            print(f"Insufficient funds. Missing ${amount - self.cash_given:.2f}")
# Create menu
menu = [
    Beverage("Coca-Cola", 5.0, "big"),
    Beverage("Orange juice", 4.0, "normal"),
    Beverage("Mineral water", 2.0, "small"),
    Appetizer("Nachos with cheese", 7.0, True),
    Appetizer("Onion rings", 6.0, False),
    Appetizer("Garlic bread", 4.5, True),
    MainCourse("Hamburger", 12.0, "fries"),
    MainCourse("Margherita pizza", 14.0, "special salad"),
    MainCourse("Bolognese pasta", 11.0, "salad"),
    MainCourse("Grilled chicken", 10.0, "rice")
    ]

# Create an order and add items
order = Order()
order.add_item(menu[0])   # Big Coca-Cola - 20% extra
order.add_item(menu[3])   # Shared Nachos with cheese - 10% discount
order.add_item(menu[6])   # Hamburger with fries - $3 extra
order.add_item(menu[8])   # Pasta with salad - no extra cost

print(order)

# Pay
total = order.apply_discount()
pago_tarjeta = CardPayment("1234567890123456", 321)
pago_tarjeta.pay(total)

pago_efectivo = CashPayment(50)
pago_efectivo.pay(total)

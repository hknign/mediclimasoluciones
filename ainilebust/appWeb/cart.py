# cart.py

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, item, item_type):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 1, 'price': str(item.precio), 'type': item_type}
        else:
            self.cart[item_id]['quantity'] += 1
        self.save()

    def decrement(self, item):
        item_id = str(item.id)
        if self.cart[item_id]['quantity'] > 1:
            self.cart[item_id]['quantity'] -= 1
        else:
            self.remove(item)
        self.save()

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for item_id, item_data in self.cart.items():
            yield item_id, item_data

    def clear(self):
        del self.session['cart']
        self.save()


from .cart import Cart

def cart_context(request):
    cart = Cart(request)  # Inicializa el carrito
    return {'cart': cart}  # Devuelve el carrito en el contexto
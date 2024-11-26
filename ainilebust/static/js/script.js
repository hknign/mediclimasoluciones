document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search');
    const filters = document.getElementById('filtros');
    const productos = document.querySelectorAll('.producto');
    const carritoDiv = document.getElementById('carrito');
    const mostrarCarritoBtn = document.getElementById('mostrar-carrito-btn');
    const carritoPopup = document.getElementById('carrito-popup');
    const cerrarCarritoBtn = document.querySelector('.cerrar');
    let carrito = [];

    // Event Listeners
    if (searchInput) {
        searchInput.addEventListener('input', filtrarProductos);
    }

    if (filters) {
        filters.addEventListener('change', aplicarFiltros);
    }

    if (productos.length > 0) {
        productos.forEach(producto => {
            const button = producto.querySelector('button');
            if (button) {
                button.addEventListener('click', () => añadirAlCarrito(producto));
            }
        });
    }

    if (mostrarCarritoBtn) {
        mostrarCarritoBtn.addEventListener('click', mostrarCarrito);
    }

    if (cerrarCarritoBtn) {
        cerrarCarritoBtn.addEventListener('click', cerrarCarrito);
    }

    if (carritoDiv) {
        carritoDiv.addEventListener('click', manejarEventosCarrito);
    }

    // Funciones
    function filtrarProductos() {
        const query = searchInput.value.toLowerCase();
        productos.forEach(producto => {
            const titulo = producto.querySelector('h3').textContent.toLowerCase();
            producto.style.display = titulo.includes(query) ? 'block' : 'none';
        });
    }

    function aplicarFiltros() {
        const filter = filters.value;
        productos.forEach(producto => {
            producto.style.display = filter === 'todos' || producto.classList.contains(filter) ? 'block' : 'none';
        });
    }

    function añadirAlCarrito(producto) {
        const nombre = producto.dataset.nombre;
        const precio = parseFloat(producto.dataset.precio);
        const existente = carrito.find(item => item.nombre === nombre);

        if (existente) {
            existente.cantidad += 1;
        } else {
            carrito.push({ nombre, precio, cantidad: 1 });
        }

        actualizarCarrito();
    }

    function actualizarCarrito() {
        carritoDiv.innerHTML = '';
        carrito.forEach((item, index) => {
            const productoDiv = document.createElement('div');
            productoDiv.classList.add('producto-carrito');
            productoDiv.innerHTML = `
                <h3>${item.nombre}</h3>
                <p>Precio: $${item.precio.toFixed(2)}</p>
                <p>Cantidad: ${item.cantidad}</p>
                <button data-index="${index}">Eliminar</button>
            `;
            carritoDiv.appendChild(productoDiv);
        });
    }

    function manejarEventosCarrito(event) {
        if (event.target.tagName === 'BUTTON') {
            const index = event.target.dataset.index;
            if (index !== undefined) {
                carrito.splice(index, 1);
                actualizarCarrito();
            }
        }
    }

    function mostrarCarrito() {
        carritoPopup.style.display = 'block';
    }

    function cerrarCarrito() {
        carritoPopup.style.display = 'none';
    }
});document.addEventListener('DOMContentLoaded', function () {
    const btnCarrito = document.getElementById('btnCarrito');
    const carritoPopup = document.getElementById('carritoPopup');
    const closeBtn = document.querySelector('.carrito-popup .close');

    btnCarrito.addEventListener('click', function () {
        cargarCarrito();
        carritoPopup.style.display = 'block';
    });

    closeBtn.addEventListener('click', function () {
        carritoPopup.style.display = 'none';
    });

    window.addEventListener('click', function (event) {
        if (event.target === carritoPopup) {
            carritoPopup.style.display = 'none';
        }
    });
});

function cargarCarrito() {
    fetch('/carrito/')
        .then(response => response.json())
        .then(data => {
            const carritoContenido = document.getElementById('contenidoCarrito');
            const totalCarrito = document.getElementById('totalCarrito');
            carritoContenido.innerHTML = '';
            let total = 0;

            if (data.carrito_items && data.carrito_items.length > 0) {
                data.carrito_items.forEach(item => {
                    const productoDiv = document.createElement('div');
                    productoDiv.classList.add('producto-carrito');
                    productoDiv.innerHTML = `
                        <img src="${item.imagen_url || 'placeholder.jpg'}" alt="${item.nombre}" style="max-width: 80px;">
                        <div>
                            <h3>${item.nombre}</h3>
                            <p>Precio: $${item.precio}</p>
                            <p>Cantidad: ${item.cantidad}</p>
                        </div>
                        <button class="btn btn-danger" onclick="eliminarProducto(${item.id})">Eliminar</button>
                    `;
                    carritoContenido.appendChild(productoDiv);
                    total += item.precio * item.cantidad;
                });
            } else {
                carritoContenido.innerHTML = '<p>El carrito está vacío.</p>';
            }
            totalCarrito.textContent = `Total: $${total.toFixed(2)}`;
        })
        .catch(error => console.error('Error al cargar el carrito:', error));
}

function actualizarTotal() {
    fetch("{% url 'get_total_price_view' %}")  // Ajusta la URL según tu configuración
        .then(response => response.json())
        .then(data => {
            const totalElement = document.getElementById('totalCarrito');
            totalElement.textContent = `Total: $${data.total_carrito.toFixed(2)}`;
        })
        .catch(error => console.error('Error al actualizar el total:', error));
}

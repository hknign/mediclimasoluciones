document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search');
    const filters = document.getElementById('filtros');
    const productos = document.querySelectorAll('.producto');
    const carritoDiv = document.getElementById('carrito');

    if (searchInput && filters && productos.length > 0 && carritoDiv) {
        searchInput.addEventListener('input', function () {
            const query = searchInput.value.toLowerCase();
            productos.forEach(producto => {
                const titulo = producto.querySelector('h3').textContent.toLowerCase();
                if (titulo.includes(query)) {
                    producto.style.display = 'block';
                } else {
                    producto.style.display = 'none';
                }
            });
        });

        filters.addEventListener('change', function () {
            const filter = filters.value;
            productos.forEach(producto => {
                if (filter === 'todos' || producto.classList.contains(filter)) {
                    producto.style.display = 'block';
                } else {
                    producto.style.display = 'none';
                }
            });
        });

        const carrito = [];

        document.querySelectorAll('.producto button').forEach(button => {
            button.addEventListener('click', function () {
                const producto = button.parentElement;
                const nombre = producto.querySelector('h3').textContent;
                const precio = producto.querySelector('p').textContent.split(' ')[1].slice(1);

                carrito.push({ nombre, precio });
                actualizarCarrito();
            });
        });

        function actualizarCarrito() {
            carritoDiv.innerHTML = '';
            carrito.forEach(item => {
                const productoDiv = document.createElement('div');
                productoDiv.classList.add('producto-carrito');
                productoDiv.innerHTML = `
                    <h3>${item.nombre}</h3>
                    <p>Precio: $${item.precio}</p>
                    <button>Eliminar</button>
                `;
                carritoDiv.appendChild(productoDiv);
            });
        }
    } else {
        console.error('No se encontraron todos los elementos necesarios en el DOM.');
    }
});

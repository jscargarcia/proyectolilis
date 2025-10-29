// =================================
// DULCERÍA LILIS - MAIN JAVASCRIPT
// =================================

(function() {
    'use strict';

    // ========== Configuración Global ==========
    const CONFIG = {
        API_BASE_URL: '/api',
        TOAST_DURATION: 3000,
        DEBOUNCE_DELAY: 300
    };

    // ========== Utilidades ==========
    const Utils = {
        // Obtener cookie CSRF
        getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        },

        // Formatear números como moneda
        formatCurrency(amount, currency = 'CLP') {
            return new Intl.NumberFormat('es-CL', {
                style: 'currency',
                currency: currency
            }).format(amount);
        },

        // Formatear fechas
        formatDate(date, format = 'short') {
            const options = format === 'short' 
                ? { year: 'numeric', month: '2-digit', day: '2-digit' }
                : { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
            return new Intl.DateTimeFormat('es-CL', options).format(new Date(date));
        },

        // Debounce para búsquedas
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Mostrar/ocultar loader
        showLoader() {
            const loader = document.createElement('div');
            loader.id = 'global-loader';
            loader.innerHTML = '<div class="loader"></div>';
            loader.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;justify-content:center;align-items:center;z-index:9999;';
            document.body.appendChild(loader);
        },

        hideLoader() {
            const loader = document.getElementById('global-loader');
            if (loader) loader.remove();
        }
    };

    // ========== Notificaciones ==========
    const Notifications = {
        // Actualizar contadores
        async updateCounters() {
            try {
                // Actualizar carrito
                const cartResponse = await fetch(`${CONFIG.API_BASE_URL}/carrito/count/`);
                if (cartResponse.ok) {
                    const cartData = await cartResponse.json();
                    const cartBadge = document.getElementById('cartCount');
                    if (cartBadge) {
                        cartBadge.textContent = cartData.count;
                        cartBadge.style.display = cartData.count > 0 ? 'inline' : 'none';
                    }
                }

                // Actualizar notificaciones
                const notifResponse = await fetch(`${CONFIG.API_BASE_URL}/notificaciones/count/`);
                if (notifResponse.ok) {
                    const notifData = await notifResponse.json();
                    const notifBadge = document.getElementById('notificationCount');
                    if (notifBadge) {
                        notifBadge.textContent = notifData.count;
                        notifBadge.style.display = notifData.count > 0 ? 'inline' : 'none';
                    }
                }
            } catch (error) {
                console.error('Error actualizando contadores:', error);
            }
        },

        // Mostrar notificaciones
        async showNotifications() {
            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/notificaciones/`);
                if (!response.ok) throw new Error('Error al cargar notificaciones');
                
                const data = await response.json();
                
                if (data.notificaciones.length === 0) {
                    Swal.fire({
                        icon: 'info',
                        title: 'Sin notificaciones',
                        text: 'No tienes notificaciones nuevas',
                        timer: 2000,
                        showConfirmButton: false
                    });
                    return;
                }

                const notifHtml = data.notificaciones.map(notif => `
                    <div class="notification-item p-3 border-bottom">
                        <div class="d-flex align-items-start">
                            <i class="fas fa-${this.getIconByType(notif.tipo)} text-${this.getColorByType(notif.tipo)} me-2"></i>
                            <div class="flex-grow-1">
                                <strong>${notif.titulo}</strong>
                                <p class="mb-1">${notif.mensaje}</p>
                                <small class="text-muted">${notif.tiempo_relativo}</small>
                            </div>
                            ${!notif.leida ? `
                                <button class="btn btn-sm btn-outline-primary" onclick="Notifications.markAsRead(${notif.id})">
                                    <i class="fas fa-check"></i>
                                </button>
                            ` : ''}
                        </div>
                    </div>
                `).join('');

                Swal.fire({
                    title: 'Notificaciones',
                    html: `
                        <div class="notifications-list" style="max-height: 400px; overflow-y: auto;">
                            ${notifHtml}
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-sm btn-outline-danger" onclick="Notifications.clearAll()">
                                <i class="fas fa-trash"></i> Limpiar todas
                            </button>
                        </div>
                    `,
                    width: 600,
                    showConfirmButton: false,
                    showCloseButton: true
                });
            } catch (error) {
                console.error('Error:', error);
                Swal.fire('Error', 'No se pudieron cargar las notificaciones', 'error');
            }
        },

        // Marcar como leída
        async markAsRead(id) {
            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/notificaciones/marcar-leida/${id}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': Utils.getCookie('csrftoken')
                    }
                });
                
                if (response.ok) {
                    await this.updateCounters();
                    await this.showNotifications();
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },

        // Limpiar todas
        async clearAll() {
            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/notificaciones/limpiar/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': Utils.getCookie('csrftoken')
                    }
                });
                
                if (response.ok) {
                    await this.updateCounters();
                    Swal.close();
                    Swal.fire('Listo', 'Notificaciones limpiadas', 'success');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },

        getIconByType(tipo) {
            const icons = {
                'info': 'info-circle',
                'success': 'check-circle',
                'warning': 'exclamation-triangle',
                'error': 'times-circle'
            };
            return icons[tipo] || 'bell';
        },

        getColorByType(tipo) {
            const colors = {
                'info': 'info',
                'success': 'success',
                'warning': 'warning',
                'error': 'danger'
            };
            return colors[tipo] || 'secondary';
        }
    };

    // ========== Carrito ==========
    const Cart = {
        // Mostrar carrito
        async show() {
            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/carrito/`);
                if (!response.ok) throw new Error('Error al cargar carrito');
                
                const data = await response.json();
                
                if (data.items.length === 0) {
                    Swal.fire({
                        icon: 'info',
                        title: 'Carrito vacío',
                        text: 'No tienes productos en el carrito',
                        timer: 2000,
                        showConfirmButton: false
                    });
                    return;
                }

                const cartHtml = data.items.map(item => `
                    <div class="cart-item d-flex justify-content-between align-items-center p-3 border-bottom">
                        <div>
                            <strong>${item.nombre}</strong>
                            <p class="mb-0">Cantidad: ${item.cantidad} × ${Utils.formatCurrency(item.precio)}</p>
                        </div>
                        <div class="d-flex align-items-center gap-2">
                            <strong>${Utils.formatCurrency(item.subtotal)}</strong>
                            <button class="btn btn-sm btn-outline-danger" onclick="Cart.removeItem(${item.id})">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                `).join('');

                Swal.fire({
                    title: 'Carrito de Compras',
                    html: `
                        <div class="cart-list" style="max-height: 400px; overflow-y: auto;">
                            ${cartHtml}
                        </div>
                        <div class="mt-3 p-3 bg-light">
                            <h4>Total: ${Utils.formatCurrency(data.total)}</h4>
                        </div>
                        <div class="mt-3">
                            <button class="btn btn-success me-2" onclick="Cart.checkout()">
                                <i class="fas fa-shopping-bag"></i> Finalizar Compra
                            </button>
                            <button class="btn btn-outline-danger" onclick="Cart.clear()">
                                <i class="fas fa-trash"></i> Vaciar Carrito
                            </button>
                        </div>
                    `,
                    width: 700,
                    showConfirmButton: false,
                    showCloseButton: true
                });
            } catch (error) {
                console.error('Error:', error);
                Swal.fire('Error', 'No se pudo cargar el carrito', 'error');
            }
        },

        // Agregar al carrito
        async add(productId, nombre, precio, cantidad = 1) {
            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/carrito/agregar/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': Utils.getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        producto_id: productId,
                        nombre: nombre,
                        precio: precio,
                        cantidad: cantidad
                    })
                });

                const data = await response.json();
                
                if (data.success) {
                    await Notifications.updateCounters();
                    Swal.fire({
                        icon: 'success',
                        title: '¡Agregado!',
                        text: data.message,
                        timer: 2000,
                        showConfirmButton: false,
                        toast: true,
                        position: 'top-end'
                    });
                } else {
                    throw new Error(data.error || 'Error al agregar al carrito');
                }
            } catch (error) {
                console.error('Error:', error);
                Swal.fire('Error', error.message, 'error');
            }
        },

        // Eliminar item
        async removeItem(itemId) {
            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/carrito/eliminar/${itemId}/`, {
                    method: 'DELETE',
                    headers: {
                        'X-CSRFToken': Utils.getCookie('csrftoken')
                    }
                });

                if (response.ok) {
                    await Notifications.updateCounters();
                    await this.show();
                }
            } catch (error) {
                console.error('Error:', error);
            }
        },

        // Vaciar carrito
        async clear() {
            const result = await Swal.fire({
                title: '¿Vaciar carrito?',
                text: 'Se eliminarán todos los productos',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Sí, vaciar',
                cancelButtonText: 'Cancelar'
            });

            if (result.isConfirmed) {
                try {
                    const response = await fetch(`${CONFIG.API_BASE_URL}/carrito/vaciar/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': Utils.getCookie('csrftoken')
                        }
                    });

                    if (response.ok) {
                        await Notifications.updateCounters();
                        Swal.close();
                        Swal.fire('Listo', 'Carrito vaciado', 'success');
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        },

        // Finalizar compra
        checkout() {
            Swal.close();
            window.location.href = '/ventas/crear/';
        }
    };

    // ========== Confirmaciones de Eliminación ==========
    window.confirmarEliminacion = function(mensaje = '¿Está seguro de eliminar este registro?') {
        return Swal.fire({
            title: '¿Confirmar eliminación?',
            text: mensaje,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => result.isConfirmed);
    };

    // ========== Búsqueda en Tiempo Real ==========
    const Search = {
        init() {
            const searchInputs = document.querySelectorAll('[data-live-search]');
            searchInputs.forEach(input => {
                input.addEventListener('input', Utils.debounce((e) => {
                    this.performSearch(e.target);
                }, CONFIG.DEBOUNCE_DELAY));
            });
        },

        performSearch(input) {
            const query = input.value.trim();
            const targetTable = input.dataset.liveSearch;
            
            if (!targetTable) return;
            
            const table = document.querySelector(targetTable);
            if (!table) return;
            
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(query.toLowerCase()) ? '' : 'none';
            });
        }
    };

    // ========== Tooltips y Popovers Bootstrap ==========
    function initBootstrapComponents() {
        // Tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Popovers
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // ========== Inicialización ==========
    document.addEventListener('DOMContentLoaded', function() {
        // Inicializar componentes Bootstrap
        initBootstrapComponents();
        
        // Actualizar contadores cada 30 segundos
        Notifications.updateCounters();
        setInterval(() => Notifications.updateCounters(), 30000);
        
        // Inicializar búsqueda
        Search.init();
        
        // Hacer disponibles las funciones globalmente
        window.Utils = Utils;
        window.Notifications = Notifications;
        window.Cart = Cart;
        
        console.log('🍬 Dulcería Lilis - Sistema cargado correctamente');
    });

    // Exponer funciones necesarias
    window.mostrarNotificaciones = () => Notifications.showNotifications();
    window.mostrarCarrito = () => Cart.show();
    window.agregarAlCarrito = (id, nombre, precio, cantidad) => Cart.add(id, nombre, precio, cantidad);

})();

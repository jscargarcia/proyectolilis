/**
 * SISTEMA DE ALERTAS AVANZADO - DULCERÍA LILIS
 * Manejo de alertas de validación, éxito y notificaciones
 */

class AlertSystem {
    constructor() {
        this.toastContainer = null;
        this.init();
    }

    init() {
        // Crear contenedor de toasts si no existe
        if (!document.querySelector('.toast-container')) {
            this.toastContainer = document.createElement('div');
            this.toastContainer.className = 'toast-container';
            document.body.appendChild(this.toastContainer);
        } else {
            this.toastContainer = document.querySelector('.toast-container');
        }
    }

    /**
     * Mostrar alerta de éxito
     * @param {string} title - Título de la alerta
     * @param {string} message - Mensaje de la alerta
     * @param {boolean} isToast - Si debe mostrarse como toast
     */
    showSuccess(title, message, isToast = false) {
        if (isToast) {
            this.showToast('success', title, message);
        } else {
            Swal.fire({
                icon: 'success',
                title: title || '¡Éxito!',
                text: message,
                timer: 4000,
                timerProgressBar: true,
                showConfirmButton: false,
                toast: false,
                customClass: {
                    popup: 'swal2-success-popup',
                    title: 'swal2-success-title',
                    content: 'swal2-success-content'
                }
            });
        }
    }

    /**
     * Mostrar alerta de error
     * @param {string} title - Título de la alerta
     * @param {string|Array} message - Mensaje o lista de errores
     * @param {boolean} isToast - Si debe mostrarse como toast
     */
    showError(title, message, isToast = false) {
        let htmlContent = '';
        
        if (Array.isArray(message)) {
            htmlContent = '<ul class="text-left mb-0">';
            message.forEach(error => {
                htmlContent += `<li>${error}</li>`;
            });
            htmlContent += '</ul>';
        } else {
            htmlContent = message;
        }

        if (isToast) {
            this.showToast('error', title, Array.isArray(message) ? message.join('<br>') : message);
        } else {
            Swal.fire({
                icon: 'error',
                title: title || 'Error',
                html: htmlContent,
                showConfirmButton: true,
                confirmButtonText: 'Entendido',
                customClass: {
                    popup: 'swal2-error-popup',
                    title: 'swal2-error-title',
                    content: 'swal2-error-content'
                }
            });
        }
    }

    /**
     * Mostrar alerta de advertencia
     * @param {string} title - Título de la alerta
     * @param {string} message - Mensaje de la alerta
     * @param {boolean} isToast - Si debe mostrarse como toast
     */
    showWarning(title, message, isToast = false) {
        if (isToast) {
            this.showToast('warning', title, message);
        } else {
            Swal.fire({
                icon: 'warning',
                title: title || 'Advertencia',
                text: message,
                timer: 5000,
                timerProgressBar: true,
                showConfirmButton: true,
                confirmButtonText: 'OK',
                customClass: {
                    popup: 'swal2-warning-popup',
                    title: 'swal2-warning-title',
                    content: 'swal2-warning-content'
                }
            });
        }
    }

    /**
     * Mostrar alerta de información
     * @param {string} title - Título de la alerta
     * @param {string} message - Mensaje de la alerta
     * @param {boolean} isToast - Si debe mostrarse como toast
     */
    showInfo(title, message, isToast = false) {
        if (isToast) {
            this.showToast('info', title, message);
        } else {
            Swal.fire({
                icon: 'info',
                title: title || 'Información',
                text: message,
                timer: 4000,
                timerProgressBar: true,
                showConfirmButton: false,
                customClass: {
                    popup: 'swal2-info-popup',
                    title: 'swal2-info-title',
                    content: 'swal2-info-content'
                }
            });
        }
    }

    /**
     * Mostrar toast notification
     * @param {string} type - Tipo de alerta (success, error, warning, info)
     * @param {string} title - Título de la alerta
     * @param {string} message - Mensaje de la alerta
     */
    showToast(type, title, message) {
        const toast = document.createElement('div');
        toast.className = `toast-alert ${type}`;
        
        const iconMap = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        toast.innerHTML = `
            <div class="alert-content">
                <div class="alert-icon">
                    <i class="${iconMap[type]}"></i>
                </div>
                <div class="alert-body">
                    <div class="alert-title">${title}</div>
                    <div class="alert-message">${message}</div>
                </div>
                <button class="alert-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="alert-progress"></div>
        `;

        this.toastContainer.appendChild(toast);

        // Auto-remove después de 5 segundos
        setTimeout(() => {
            if (toast && toast.parentElement) {
                toast.classList.add('removing');
                setTimeout(() => {
                    if (toast && toast.parentElement) {
                        toast.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    /**
     * Confirmar acción con SweetAlert2
     * @param {Object} options - Opciones de confirmación
     */
    confirm(options = {}) {
        const defaultOptions = {
            title: '¿Estás seguro?',
            text: 'Esta acción no se puede deshacer',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, continuar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true,
            customClass: {
                confirmButton: 'swal2-confirm-btn',
                cancelButton: 'swal2-cancel-btn'
            }
        };

        return Swal.fire({ ...defaultOptions, ...options });
    }

    /**
     * Mostrar loading
     * @param {string} message - Mensaje de carga
     */
    showLoading(message = 'Procesando...') {
        Swal.fire({
            title: message,
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            willOpen: () => {
                Swal.showLoading();
            }
        });
    }

    /**
     * Cerrar loading
     */
    hideLoading() {
        Swal.close();
    }

    /**
     * Validación en tiempo real para formularios
     * @param {HTMLElement} form - Elemento del formulario
     */
    initFormValidation(form) {
        if (!form) return;

        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Validación en tiempo real
            input.addEventListener('blur', () => {
                this.validateField(input);
            });

            input.addEventListener('input', () => {
                // Limpiar validación anterior si está escribiendo
                this.clearFieldValidation(input);
            });
        });

        // Validación al enviar formulario
        form.addEventListener('submit', (e) => {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!this.validateField(input)) {
                    isValid = false;
                }
            });

            if (!isValid) {
                e.preventDefault();
                this.showError('Formulario inválido', 'Por favor corrige los errores antes de continuar');
            }
        });
    }

    /**
     * Validar campo individual
     * @param {HTMLElement} field - Campo a validar
     */
    validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const required = field.hasAttribute('required');
        let isValid = true;
        let message = '';

        // Limpiar validación anterior
        this.clearFieldValidation(field);

        // Verificar si es requerido
        if (required && !value) {
            isValid = false;
            message = 'Este campo es requerido';
        }
        // Validaciones específicas por tipo
        else if (value) {
            switch (type) {
                case 'email':
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        isValid = false;
                        message = 'Ingresa un email válido';
                    }
                    break;
                    
                case 'number':
                    const num = parseFloat(value);
                    if (isNaN(num)) {
                        isValid = false;
                        message = 'Debe ser un número válido';
                    } else if (field.hasAttribute('min') && num < parseFloat(field.min)) {
                        isValid = false;
                        message = `El valor mínimo es ${field.min}`;
                    } else if (field.hasAttribute('max') && num > parseFloat(field.max)) {
                        isValid = false;
                        message = `El valor máximo es ${field.max}`;
                    }
                    break;
                    
                case 'tel':
                    const phoneRegex = /^[\+]?[0-9\s\-\(\)]{8,}$/;
                    if (!phoneRegex.test(value)) {
                        isValid = false;
                        message = 'Ingresa un teléfono válido';
                    }
                    break;
            }

            // Validaciones personalizadas por atributos
            if (field.hasAttribute('minlength') && value.length < parseInt(field.minLength)) {
                isValid = false;
                message = `Mínimo ${field.minLength} caracteres`;
            }

            if (field.hasAttribute('maxlength') && value.length > parseInt(field.maxLength)) {
                isValid = false;
                message = `Máximo ${field.maxLength} caracteres`;
            }
        }

        // Aplicar estilos de validación
        if (isValid) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            this.showFieldError(field, message);
        }

        return isValid;
    }

    /**
     * Limpiar validación de campo
     * @param {HTMLElement} field - Campo a limpiar
     */
    clearFieldValidation(field) {
        field.classList.remove('is-valid', 'is-invalid');
        const feedback = field.parentElement.querySelector('.invalid-feedback, .valid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }

    /**
     * Mostrar error en campo específico
     * @param {HTMLElement} field - Campo con error
     * @param {string} message - Mensaje de error
     */
    showFieldError(field, message) {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        
        // Insertar después del campo
        field.parentElement.appendChild(feedback);
    }

    /**
     * Mostrar estado de carga en botón
     * @param {HTMLElement} button - Botón a modificar
     * @param {boolean} loading - Si debe mostrar carga
     */
    setButtonLoading(button, loading = true) {
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
        }
    }
}

// Inicializar sistema de alertas globalmente
window.AlertSystem = new AlertSystem();

// Funciones de conveniencia globales
window.showSuccess = (title, message, isToast = false) => window.AlertSystem.showSuccess(title, message, isToast);
window.showError = (title, message, isToast = false) => window.AlertSystem.showError(title, message, isToast);
window.showWarning = (title, message, isToast = false) => window.AlertSystem.showWarning(title, message, isToast);
window.showInfo = (title, message, isToast = false) => window.AlertSystem.showInfo(title, message, isToast);
window.showConfirm = (options) => window.AlertSystem.confirm(options);
window.showLoading = (message) => window.AlertSystem.showLoading(message);
window.hideLoading = () => window.AlertSystem.hideLoading();

// Auto-inicializar validación en formularios al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 Sistema de alertas cargado');
    
    // Inicializar validación en todos los formularios con clase 'needs-validation'
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        window.AlertSystem.initFormValidation(form);
    });
    
    // Mejorar mensajes de Django existentes
    if (typeof Swal !== 'undefined') {
        console.log('✅ SweetAlert2 disponible para alertas mejoradas');
    }
});
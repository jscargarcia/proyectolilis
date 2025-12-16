/**
 * Validaciones Globales de Formularios
 * Sistema de Gestión - Dulcería Lilis
 * 
 * Este archivo contiene validaciones JavaScript para todos los formularios del sistema
 * Previene el ingreso de números negativos y símbolos +/- en campos numéricos
 */

document.addEventListener('DOMContentLoaded', function() {
    
    /**
     * Función para validar y limpiar campos numéricos
     * Elimina los caracteres + y - del input
     */
    function validateNumericInput(input) {
        // Remover signos + y -
        input.value = input.value.replace(/[+-]/g, '');
        
        // Si el valor es negativo después de la validación, establecer en 0
        if (parseFloat(input.value) < 0) {
            input.value = '0';
        }
    }
    
    /**
     * Aplicar validación a todos los campos numéricos
     */
    function applyNumericValidations() {
        // Seleccionar todos los inputs de tipo number
        const numericInputs = document.querySelectorAll('input[type="number"]');
        
        numericInputs.forEach(function(input) {
            // Establecer min="0" si no está definido y no tiene un min específico
            if (!input.hasAttribute('min')) {
                input.setAttribute('min', '0');
            }
            
            // Validación en tiempo real mientras el usuario escribe
            input.addEventListener('input', function(e) {
                validateNumericInput(e.target);
            });
            
            // Validación cuando el campo pierde el foco
            input.addEventListener('blur', function(e) {
                validateNumericInput(e.target);
                
                // Si está vacío y es requerido, establecer valor mínimo
                if (e.target.value === '' && e.target.hasAttribute('required')) {
                    const min = parseFloat(e.target.getAttribute('min')) || 0;
                    e.target.value = min;
                }
            });
            
            // Prevenir pegado de valores negativos o con signos
            input.addEventListener('paste', function(e) {
                setTimeout(function() {
                    validateNumericInput(e.target);
                }, 10);
            });
            
            // Prevenir el uso de las teclas + y -
            input.addEventListener('keydown', function(e) {
                // Códigos de tecla para + (187, 107) y - (189, 109)
                if (e.keyCode === 187 || e.keyCode === 107 || 
                    e.keyCode === 189 || e.keyCode === 109 ||
                    e.key === '+' || e.key === '-') {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }
    
    /**
     * Validación adicional antes del envío del formulario
     */
    function validateFormSubmit() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                const numericInputs = form.querySelectorAll('input[type="number"]');
                let hasErrors = false;
                
                numericInputs.forEach(function(input) {
                    const value = parseFloat(input.value);
                    const min = parseFloat(input.getAttribute('min')) || 0;
                    
                    // Verificar si hay valor negativo
                    if (!isNaN(value) && value < min) {
                        input.value = min;
                        input.classList.add('is-invalid');
                        hasErrors = true;
                        
                        // Mostrar mensaje de error
                        let errorDiv = input.parentElement.querySelector('.invalid-feedback');
                        if (!errorDiv) {
                            errorDiv = document.createElement('div');
                            errorDiv.className = 'invalid-feedback';
                            input.parentElement.appendChild(errorDiv);
                        }
                        errorDiv.textContent = `El valor mínimo permitido es ${min}`;
                        errorDiv.style.display = 'block';
                    } else {
                        input.classList.remove('is-invalid');
                        const errorDiv = input.parentElement.querySelector('.invalid-feedback');
                        if (errorDiv) {
                            errorDiv.style.display = 'none';
                        }
                    }
                });
                
                // Si hay errores, prevenir el envío y mostrar alerta
                if (hasErrors) {
                    e.preventDefault();
                    
                    // Usar SweetAlert2 si está disponible
                    if (typeof Swal !== 'undefined') {
                        Swal.fire({
                            icon: 'error',
                            title: 'Error de Validación',
                            text: 'Por favor, corrija los valores negativos en el formulario.',
                            confirmButtonText: 'Entendido'
                        });
                    } else {
                        alert('Por favor, corrija los valores negativos en el formulario.');
                    }
                    
                    return false;
                }
            });
        });
    }
    
    // Aplicar validaciones al cargar la página
    applyNumericValidations();
    validateFormSubmit();
    
    // Re-aplicar validaciones si se cargan elementos dinámicamente
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length) {
                applyNumericValidations();
            }
        });
    });
    
    // Observar cambios en el DOM
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    console.log('✅ Validaciones de formularios numéricos cargadas correctamente');
});

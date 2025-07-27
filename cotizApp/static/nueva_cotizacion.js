// --- Utilidades ---
function formatearMoneda(valor) {
    return `$${valor.toFixed(2)}`;
}
function parsearMoneda(valor) {
    return parseFloat((valor || '').toString().replace('$', '')) || 0;
}

// --- Eventos de filas ---
function asignarEventosFila(fila) {
    const cantidadInput = fila.querySelector('[name="cantidad"]');
    if (cantidadInput) {
        cantidadInput.addEventListener('change', function () {
            actualizarTotalesFila(fila);
            actualizarTotalesGenerales();
        });
    }
    const articuloSelect = fila.querySelector('[name="articulos_cotizados"]');
    if (articuloSelect) {
        articuloSelect.addEventListener('change', completarCampos);
    }
}

// --- Actualización de totales ---
function actualizarTotalesFila(fila) {
    const precioInput = fila.querySelector('[name="precio"]');
    const cantidadInput = fila.querySelector('[name="cantidad"]');
    const totalInput = fila.querySelector('[name="totalArticulo"]');
    if (!precioInput || !cantidadInput || !totalInput) return;

    const precio = parseFloat(precioInput.getAttribute('data-precio-original')) || 0;
    const cantidad = parseInt(cantidadInput.value) || 0;
    const condicionPagoEl = document.getElementById('condiciones-pago');
    const condicionPago = condicionPagoEl ? condicionPagoEl.value : '';

    let precioFinal = precio;
    if (condicionPago === "Efectivo") {
        precioFinal = precio * 0.9;
    }

    const totalCalculado = precioFinal * cantidad;
    precioInput.value = formatearMoneda(precioFinal);
    totalInput.value = formatearMoneda(totalCalculado);

    actualizarTotalesGenerales();
}

function actualizarTotalesGenerales() {
    const filas = document.querySelectorAll('.invoice-items tbody tr:not(.fila-descuento)');
    let totalGeneral = 0;
    filas.forEach(fila => {
        const total = fila.querySelector('[name="totalArticulo"]');
        totalGeneral += parsearMoneda(total?.value);
    });

    const totalInput = document.getElementById('total');
    if (totalInput) totalInput.value = formatearMoneda(totalGeneral);

    actualizarAhorroTotalDescuento();
    totalConDescuento();
    actualizarTotalEnvio();
}

// --- Autocompletado de campos ---
function completarCampos(e) {
    const fila = e.target.closest('tr');
    const select = e.target;
    const descripcion = fila.querySelector('[name="descripcion"]');
    const precio = fila.querySelector('[name="precio"]');
    const total = fila.querySelector('[name="totalArticulo"]');
    const selectedOption = select.options[select.selectedIndex];

    if (selectedOption.value) {
        descripcion.value = selectedOption.getAttribute('data-descripcion');
        const precioOriginal = parseFloat(selectedOption.getAttribute('data-precio'));
        precio.value = formatearMoneda(precioOriginal);
        precio.setAttribute('data-precio-original', precioOriginal);
        actualizarTotalesFila(fila);
    } else {
        descripcion.value = '';
        precio.value = '$0.00';
        total.value = '$0.00';
        actualizarTotalesFila(fila);
    }
    actualizarTotalesGenerales();
}

// --- Artículos ---
        function agregarArticuloNuevo() {
            const tabla = document.querySelector('.invoice-items tbody');
            const nuevaFila = document.createElement('tr');
            nuevaFila.classList.add('fila-articulo');

            // Cantidad
            const tdCantidad = document.createElement('td');
            const inputCantidad = document.createElement('input');
            inputCantidad.className = "form-control"; 
            inputCantidad.name = "cantidad";
            inputCantidad.type = "number";
            inputCantidad.value = "1";
            inputCantidad.min = 0;
            inputCantidad.max = 1000;
            tdCantidad.appendChild(inputCantidad);
            nuevaFila.appendChild(tdCantidad);

            // Artículo
            const tdSelect = document.createElement('td');
            const select = document.createElement('select');
            select.className = "form-control"; //
            select.name = "articulos_cotizados";
            const existingSelect = document.getElementById('articulo');
            if (existingSelect) {
                Array.from(existingSelect.options).forEach(option => {
                    select.appendChild(option.cloneNode(true));
                });
            }
            tdSelect.appendChild(select);
            nuevaFila.appendChild(tdSelect);

            // Descripción, Precio, Total
            ['descripcion', 'precio', 'totalArticulo'].forEach(name => {
                const td = document.createElement('td');
                const input = document.createElement('input');
                input.className = 'form-control';
                input.type = 'text';
                input.name = name;
                input.readOnly = true;
                input.placeholder = name === 'totalArticulo' ? '$0.00' : '';
                td.appendChild(input);
                nuevaFila.appendChild(td);
            });

            // Checkbox
            const tdCheckbox = document.createElement('td');
            const inputCheckbox = document.createElement('input');
            inputCheckbox.name = "articulos_seleccionados[]";
            inputCheckbox.type = "checkbox";
            inputCheckbox.className = "form-check-input";
            tdCheckbox.appendChild(inputCheckbox);
            nuevaFila.appendChild(tdCheckbox);

            // Insertar antes de descuento y el costo de envio si existen
            const filaDescuento = tabla.querySelector('.fila-descuento');
            const filaEnvio = tabla.querySelector('.fila-costo-envio');

            let referencia = null;

            if (filaDescuento && filaEnvio) {
                referencia = filaDescuento.compareDocumentPosition(filaEnvio) & Node.DOCUMENT_POSITION_FOLLOWING
                    ? filaDescuento
                    : filaEnvio;
            } else {
                referencia = filaDescuento || filaEnvio;
            }

            if (referencia) {
                tabla.insertBefore(nuevaFila, referencia);
            } else {
                tabla.appendChild(nuevaFila);
            }

            asignarEventosFila(nuevaFila);
            actualizarTotalesGenerales();
        }

        function eliminarArticulosSeleccionados() {
            const checkboxes = document.querySelectorAll('input[name="articulos_seleccionados[]"]:checked');
            checkboxes.forEach(checkbox => {
                const fila = checkbox.closest('tr');
                fila.remove();
            });
            actualizarTotalesGenerales();
        }

// --- Descuento ---
        function aplicarDescuentoNuevo() {
            const tabla = document.querySelector('.invoice-items tbody');
            if (tabla.querySelector('.fila-descuento')) return;

            const nuevaFila = document.createElement('tr');
            nuevaFila.classList.add('fila-descuento');

            // Cantidad (siempre 1, no editable)
            const tdCantidad = document.createElement('td');
            const inputCantidad = document.createElement('input');
            inputCantidad.className = "form-control";
            inputCantidad.name = "cantidad";
            inputCantidad.type = "number";
            inputCantidad.value = 1;
            inputCantidad.min = 1;
            inputCantidad.max = 1;
            inputCantidad.readOnly = true;
            tdCantidad.appendChild(inputCantidad);
            nuevaFila.appendChild(tdCantidad);

            // Texto "Descuento"
            const tdDescuento = document.createElement('td');
            tdDescuento.className = "align-middle";
            tdDescuento.textContent = "Descuento";
            nuevaFila.appendChild(tdDescuento);

            // Select % descuento
            const tdValorDescuento = document.createElement('td');
            const selectValorDescuento = document.createElement('select');
            selectValorDescuento.className = "form-control";
            selectValorDescuento.name = "descuento";
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = '% de descuento';
            selectValorDescuento.appendChild(defaultOption);
            [5, 10, 15, 20, 25, 30].forEach(porcentaje => {
                const option = document.createElement('option');
                option.value = porcentaje;
                option.textContent = `${porcentaje}%`;
                selectValorDescuento.appendChild(option);
            });
            tdValorDescuento.appendChild(selectValorDescuento);
            nuevaFila.appendChild(tdValorDescuento);

            // Texto "Ahorro total"
            const tdDescuentoTotal = document.createElement('td');
            tdDescuentoTotal.className = "align-middle";
            tdDescuentoTotal.textContent = "Ahorro total";
            nuevaFila.appendChild(tdDescuentoTotal);

            // Input ahorro total
            const tdInputAhorroTotal = document.createElement('td');
            const inputAhorroTotal = document.createElement('input');
            inputAhorroTotal.type = 'text';
            inputAhorroTotal.readOnly = true;
            inputAhorroTotal.className = 'form-control input-ahorro-total';
            inputAhorroTotal.value = '$0.00';
            tdInputAhorroTotal.appendChild(inputAhorroTotal);
            nuevaFila.appendChild(tdInputAhorroTotal);

            // Botón eliminar fila
            const tdEliminar = document.createElement('td');
            tdEliminar.className = "text-center align-middle"; 
            const btnEliminar = document.createElement('button');
            btnEliminar.type = "button";
            btnEliminar.className = "btn btn-sm btn-outline-danger"; // 
            btnEliminar.innerHTML = '<i class="fas fa-times"></i>'; // 
            btnEliminar.title = "Eliminar descuento";

            // Al eliminar la fila de descuento
            const filaDescuento = document.querySelector('.fila-descuento');
                btnEliminar.addEventListener('click', function() {
                    nuevaFila.remove(); 
                    const totalConDesc = document.querySelector('.totalConDescuento');
                    if (totalConDesc) {
                        totalConDesc.innerHTML = '';
                    }
                });
                                    

            // Me aseguro que el costo de envio siempre quede al final 
            const filaEnvio = tabla.querySelector('.fila-costo-envio'); 
            if (filaEnvio) {
                tabla.insertBefore(nuevaFila, filaEnvio); 
            } else {
                tabla.appendChild(nuevaFila); 
            }

            tdEliminar.appendChild(btnEliminar);
            nuevaFila.appendChild(tdEliminar);

            // Evento para actualizar ahorro y total con descuento
            selectValorDescuento.addEventListener('change', function () {
                actualizarAhorroTotalDescuento();
                totalConDescuento();
            });

            actualizarAhorroTotalDescuento();
            totalConDescuento();
        }
        

        function actualizarAhorroTotalDescuento() {
            const filaDescuento = document.querySelector('.fila-descuento');
            if (!filaDescuento) return;
            const selectValorDescuento = filaDescuento.querySelector('select[name="descuento"]');
            const inputAhorroTotal = filaDescuento.querySelector('input.input-ahorro-total');
            if (!selectValorDescuento || !inputAhorroTotal) return;
            const porcentaje = parseFloat(selectValorDescuento.value) || 0;
            const totalGeneral = parsearMoneda(document.getElementById('total').value);
            inputAhorroTotal.value = porcentaje ? formatearMoneda(totalGeneral * (porcentaje / 100)) : '$0.00';
        }

        function totalConDescuento() {
            const totalGeneral = parsearMoneda(document.getElementById('total').value);
            const filaDescuento = document.querySelector('.fila-descuento');
            const totalConDescuentoDiv = document.querySelector('.totalConDescuento')

            totalConDescuentoDiv.innerHTML = '';

            if (filaDescuento) {
                const selectValorDescuento = filaDescuento.querySelector('select[name="descuento"]');
                const porcentaje = parseFloat(selectValorDescuento.value) || 0;
                if (porcentaje > 0) {
                    const descuento = totalGeneral * (porcentaje / 100);
                    const totalFinal = totalGeneral - descuento;

                    let input = totalConDescuentoDiv.querySelector('input[name="totalConDescuento"]');
                    let label = totalConDescuentoDiv.querySelector('label.totalConDescuentoLabel');

                    if (!input) {
                        label = document.createElement('label');
                        label.textContent = 'Total con descuento';
                        label.className = 'totalConDescuentoLabel';
                        input = document.createElement('input');
                        input.type = 'text';
                        input.readOnly = true;
                        input.className = 'form-control';
                        input.name = 'totalConDescuento';
                        totalConDescuentoDiv.appendChild(label);
                        totalConDescuentoDiv.appendChild(input);
                    }
                    input.value = formatearMoneda(totalFinal);
                }
            }
        }

// --- Envío ---
        function costoEnvio() {
            const tabla = document.querySelector('.invoice-items tbody');
            if (tabla.querySelector('.fila-costo-envio')) return;

            const nuevaFila = document.createElement('tr');
            nuevaFila.classList.add('fila-costo-envio');

            // Cantidad (siempre 1, no editable)
            const tdCantidad = document.createElement('td');
            const inputCantidad = document.createElement('input');
            inputCantidad.name = "cantidad";
            inputCantidad.type = "number";
            inputCantidad.value = 1;
            inputCantidad.min = 1;
            inputCantidad.max = 1;
            inputCantidad.readOnly = true;
            tdCantidad.appendChild(inputCantidad);
            nuevaFila.appendChild(tdCantidad);

            // 
            const tdEnvio = document.createElement('td');
             tdEnvio.className = "align-middle"; 
            tdEnvio.textContent = "Envio";
            nuevaFila.appendChild(tdEnvio);

            // Select zona envio
            const localidadIngresada = prompt('Ingrese la localidad de envío (ej: CABA, GBA CORDON 1, etc.)');
            if (localidadIngresada === null || localidadIngresada.trim() === '') {
                alert('Localidad inválida. No se agregará la fila.');
                return;
            }
            const tdLocalidad = document.createElement('td');
            tdLocalidad.className = "align-middle"; 
            tdLocalidad.textContent = localidadIngresada.trim();
            nuevaFila.appendChild(tdLocalidad);


            // Input costo envio
            const tdInputCostoEnvio = document.createElement('td');
            const inputCostoEnvio = document.createElement('input');
            inputCostoEnvio.type = 'number';
            inputCostoEnvio.min = 0;
            inputCostoEnvio.step = '0.01';
            inputCostoEnvio.className = 'form-control input-costo-envio';
            inputCostoEnvio.placeholder = 'Costo envío';
            
            // Pido el costo con prompt para arrancar (podés sacar el prompt y dejar solo editable)
            const costoIngresado = prompt('Ingrese el costo de envío (sin $)');
            if (costoIngresado === null || costoIngresado === '' || isNaN(costoIngresado) || Number(costoIngresado) < 0) {
                alert('Costo inválido. No se agregará la fila.');
                return;
            }
            inputCostoEnvio.value = Number(costoIngresado).toFixed(2);
            tdInputCostoEnvio.appendChild(inputCostoEnvio);
            nuevaFila.appendChild(tdInputCostoEnvio);


            // Botón eliminar fila
            const tdEliminar = document.createElement('td');
            tdEliminar.className = "text-center align-middle"; 
            const btnEliminar = document.createElement('button');
            btnEliminar.type = "button";
            btnEliminar.className = "btn btn-sm btn-outline-danger"; // 
            btnEliminar.innerHTML = '<i class="fas fa-times"></i>'; // 
            btnEliminar.title = "Eliminar descuento";


            // Evento para eliminar la fila
            btnEliminar.addEventListener('click', function () {
                nuevaFila.remove();
                actualizarTotalEnvio();
            });

            tdEliminar.appendChild(btnEliminar);
            nuevaFila.appendChild(tdEliminar);

            tabla.appendChild(nuevaFila);
            actualizarTotalEnvio();
        }        

        // --- Envío: solo actualiza el input oculto ---
        function actualizarTotalEnvio() {
            const filaEnvio = document.querySelector('.fila-costo-envio');
            const inputEnvio = document.getElementById('costo_envio');
            if (!filaEnvio || !inputEnvio) {
                if (inputEnvio) inputEnvio.value = '0';
                return;
            }
            const inputCostoEnvio = filaEnvio.querySelector('input.input-costo-envio');
            const costo = parseFloat(inputCostoEnvio?.value || 0);
            inputEnvio.value = !isNaN(costo) && costo > 0 ? costo.toFixed(2) : '0';
        }
    // --- Inicialización y eventos ---
    document.addEventListener('DOMContentLoaded', function () {
        const condicionPagoEl = document.getElementById('condiciones-pago');
        if (condicionPagoEl) {
            condicionPagoEl.addEventListener('change', function () {
                const filas = document.querySelectorAll('.invoice-items tbody tr');
                filas.forEach(actualizarTotalesFila);
                actualizarTotalesGenerales();
            });
        }

        document.querySelectorAll('.invoice-items tbody tr').forEach(asignarEventosFila);

        const primerSelect = document.getElementById('articulo');
        if (primerSelect) primerSelect.addEventListener('change', completarCampos);

        const btnAgregar = document.getElementById('agregarArticulo');
        if (btnAgregar) btnAgregar.addEventListener('click', agregarArticuloNuevo);

        const btnEliminar = document.getElementById('eliminarArticulo');
        if (btnEliminar) btnEliminar.addEventListener('click', eliminarArticulosSeleccionados);

        const btnDescuento = document.getElementById('aplicarDescuento');
        if (btnDescuento) btnDescuento.addEventListener('click', aplicarDescuentoNuevo);

        const btnEnvio = document.getElementById('sumarCostoEnvio');
        if (btnEnvio) btnEnvio.addEventListener('click', costoEnvio);

        const empresaEl = document.getElementById('empresa');
        if (empresaEl) empresaEl.addEventListener('change', mostrarInfoEmpresa);

        const clienteEl = document.getElementById('cliente');
        if (clienteEl) clienteEl.addEventListener('change', mostrarInfoCliente);
    });

        // --- Info empresa/cliente ---
        function mostrarInfoEmpresa() {
            const selected = this.options[this.selectedIndex];
            const infoDiv = document.getElementById('empresa-info');
            if (selected.value) {
                infoDiv.innerHTML = `
                    <p><strong>CUIT:</strong> ${selected.getAttribute('data-cuit')}</p>
                    <p><strong>Teléfono:</strong> ${selected.getAttribute('data-telefono')}</p>
                    <p><strong>Mail:</strong> ${selected.getAttribute('data-mail-empresa')}</p>
                `;
            } else {
                infoDiv.innerHTML = '';
            }
        }

        function mostrarInfoCliente() {
            const selected = this.options[this.selectedIndex];
            const infoDiv = document.getElementById('cliente-info');
            if (selected.value) {
                infoDiv.innerHTML = `
                    <p><strong>Empresa:</strong> ${selected.getAttribute('data-empresa')}</p>
                    <p><strong>Cuit:</strong> ${selected.getAttribute('data-cuit-cliente')}</p>
                    <p><strong>Mail:</strong> ${selected.getAttribute('data-mail-cliente')}</p>
                `;
            } else {
                infoDiv.innerHTML = '';
            }
        }
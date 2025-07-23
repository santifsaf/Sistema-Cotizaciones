# Proyecto 

Este proyecto permite gestionar empresas, clientes, artículos y cotizaciones, con generación de PDFs y autenticación de usuarios.

# App Cotizaciones

Esta app gestiona la creación, edición y eliminación de cotizaciones.


### Modelos 

- **Cotizaciones**: Representa una cotización, con campos para usuario, cliente, empresa, totales y descuentos.
- **ArticulosCotizado**: Relaciona artículos con cotizaciones, incluye cantidad y subtotal.

Cada cotización calcula automáticamente sus totales y genera un número de referencia único.

## Vistas 

- `MisCotizaciones`: Listado de cotizaciones del usuario.
- `NuevaCotizacion`: Formulario para crear una nueva cotización.
- `EliminarCotizacion`: Permite eliminar cotizaciones seleccionadas.
- `generar_pdf`: Exporta una cotización en PDF.


## Cómo funciona

1. El usuario crea una cotización seleccionando los datos de su empresa, el cliente, y artículos.
2. Se calculan los totales y descuentos automáticamente.
3. Las cotizaciones pueden exportarse en PDF.

---

# App Clientes

Esta app gestiona los clientes del sistema de cotizaciones.

## Modelos

- **Cliente**: Información básica, empresa asociada, contacto.

## Vistas

- Listado de clientes
- Alta/edición/eliminación de clientes

## Uso

Accede al panel de clientes para ver, agregar o modificar registros.

---

# App Artículos

Gestiona los artículos disponibles para cotizar.

## Modelos

- **Artículo**: Nombre, descripción, precio, stock.

## Vistas

- Listado de artículos
- Alta/edición/eliminación

---

# App Facturación

Administra empresas y cotizaciones.

## Modelos

- **Empresa**
- **Cotización**
- **ArtículosCotizado**

## Vistas

- Listado de empresas
- Listado y gestión de cotizaciones

---
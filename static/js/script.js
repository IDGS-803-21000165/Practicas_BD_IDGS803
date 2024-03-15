function confirmarCompra() {
    Swal.fire({
        title: '¿Desea guardar la compra?',
        showDenyButton: true,
        showCancelButton: true,
        confirmButtonText: 'Guardar',
        denyButtonText: `No guardar`,
    }).then(result => {
        /* Read more about isConfirmed, isDenied below */
        if (result.isConfirmed) {
            window.location.href = '/guardarpizza';
            Swal.fire('Saved!', '', 'success');
        } else if (result.isDenied) {
            const botonesModificar = document.querySelectorAll('#btnModificar');
            botonesModificar.forEach(boton => boton.classList.remove('desactivado'));
            Swal.fire('No se completo la compra, puede modificar la información', '', 'info');
        }
    });
}

async function guardarCompra(token) {
    try {
        await axios
            .post('/guardarpizza', {
                headers: {
                    'X-CSRF-Token': token,
                },
            })
            .then(response => {
                console.log('🚀 ~ guardarCompra ~ response:', response);
                return response;
            });
    } catch (error) {
        console.error(error);
    }
}

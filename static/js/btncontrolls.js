document.addEventListener('DOMContentLoaded', function () {

    var crearProductoModal = new bootstrap.Modal(document.getElementById('crearProductoModal'));
    var abrirModalBtn = document.getElementById('abrirModalBtn');
    abrirModalBtn.addEventListener('click', function () {

        crearProductoModal.show();
    });

    var guardarDatosBtn = document.getElementById('guardarDatosBtn');
    guardarDatosBtn.addEventListener('click', function () {

        crearProductoModal.hide();
    });
});
function goBack() {
    window.history.back();
}
document.addEventListener('DOMContentLoaded', function () {
    var deleteButtons = document.querySelectorAll('.delete-comment-button');

    deleteButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var form = this.closest('.delete-comment-form');

            Swal.fire({
                title: '¿Estás seguro?',
                text: 'Esta acción eliminará el comentario. No podrás deshacer esta acción.',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Si el usuario confirma, envía el formulario para eliminar el comentario
                    form.submit();
                }
            });
        });
    });
});
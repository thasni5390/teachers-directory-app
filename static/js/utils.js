var Utils = {
    init: function () {
        this.fileChangeHandler();
    },
    fileChangeHandler: function () {
        $(document).on('change', 'input[type="file"]', function (event) {
            var filename = $(this).val();
            if (filename == undefined || filename == ""){
            $(this).next('.custom-file-label').html('No file chosen');
            }
            else
            { $(this).next('.custom-file-label').html(event.target.files[0].name); }
        });
    }
}

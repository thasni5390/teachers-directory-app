var AdvancedFilterForm ={
    elements: {
        form: '#advanced_filter_form',
        reset_btn: '#js-advanced-form-reset',
    },
    init: function () {
        $(this.elements.reset_btn).click(function () {
            $(this.elements.form).find("input[type=text], select").val("");
            $(this.elements.form).submit();
        }.bind(this))
    }
}

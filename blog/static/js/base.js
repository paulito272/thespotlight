function addFooterPadding() {
    var pb = $('#footer').height() + 70;
    $('body').css({paddingBottom: pb + 'px'});
}

$(document).ready(function () {
    $('#ts-loginModal').appendTo('body');
    $('#ts-interview-content').find('img').addClass('img-fluid');

    // Redirect on selection change
    $('.custom-select').on('change', function () {
        if (this.value === '') {
            return false;
        } else {
            var id = $(this).attr('id');
            if (id === 'ts-interview-date-selection') {
                window.location.href = '/interviews/' + this.value;
            } else if (id === 'ts-suggestion-date-selection') {
                window.location.href = '/suggestions/' + this.value;
            }
        }
    });
    addFooterPadding();
});

$(window).resize(function () {
    addFooterPadding();
});
function addFooterPadding() {
    var pb = $('#footer').height() + 70;
    $('body').css({paddingBottom: pb + 'px'});
}

$(document).ready(function () {
    $('#ts-loginModal').appendTo('body');
    $('#ts-interview-content').find('img').addClass('img-fluid');
    addFooterPadding();
});

$(window).resize(function () {
    addFooterPadding();
});
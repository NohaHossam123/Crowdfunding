$(function() {
    $('#exampleModal').on("show.bs.modal", function (e) {
        let button = $(e.relatedTarget)
        action = button.data('action')
        $("#text_form").attr('action', action)
        $("#message-text").val(button.data('message'))
        $("#text_header").text(button.data('header'))
        $("#submit_button").text(button.data('button'))
    });
});



$(document).ready(function() { 
    $('input[name=rating]').change(function(){
         $('#rate_form').submit();
    });
});
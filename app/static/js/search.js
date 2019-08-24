$("#column-select-checkboxes input:checkbox:not(:checked)").each(function() {
        var column = "table ." + $(this).attr("name");
        $(column).hide();
});

$("#column-select-checkboxes input:checkbox").click(function(){
        var column = "table ." + $(this).attr("name");
        $(column).toggle();
});

$(".sort-by").click(function(event) {
    column = $(this).parent().get(0).className;
    $('input[name="sort_column"]').val(column);
    $(".form").submit();
});

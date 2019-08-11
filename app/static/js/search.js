$("#column-select-checkboxes input:checkbox:not(:checked)").each(function() {
        var column = "table ." + $(this).attr("name");
        $(column).hide();
});

$("#column-select-checkboxes input:checkbox").click(function(){
        var column = "table ." + $(this).attr("name");
        $(column).toggle();
});

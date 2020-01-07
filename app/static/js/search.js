$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = $('meta[name=csrf-token]').attr('content');
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
        xhr.setRequestHeader("Content-type", "application/json");
    }
})

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

$('#tbl').on('click','.delete',function() {
    cells = $(this).parent().siblings();
    id = cells.filter(".id").text()

    if (!confirm("Are you sure you want to permanently delete entry " + id + "?")) {
        return;
    }

    var data = JSON.stringify( true )
    $.ajax({
        type: "DELETE",
        url: "/lexicon/" + id,
        data: data,
        success: function(response) {
            alert(response.message);
            location.reload();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert(xhr.responseText);
        }
    });
});

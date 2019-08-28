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

$('#tbl').on('click','.edit',function() {
    f = function(c){
        var t = $(c).text();
        var len = 12 > t.length ? 12 : t.length;
        $(c).html($('<input />',{'value' : t, 'size':len}).val(t));
    };

    rows = $(this).parent().siblings();

    f(rows.filter(".concept"));
    f(rows.filter(".ortho"));
    f(rows.filter(".stem"));
    f(rows.filter(".ipa"));

    $(this).attr("class", "save");
    $(this).text("[OK]");
});

$('#tbl').on('click','.save',function() {
    f = function(c){
        $(c).text($(c).find('input').val());
    };

    /* reset the UI */
    rows = $(this).parent().siblings();
    f(rows.filter(".concept"));
    f(rows.filter(".ortho"));
    f(rows.filter(".stem"));
    f(rows.filter(".ipa"));

    /* TODO: make an ajax post */
    alert(rows.filter(".term_id").text());

    $(this).attr("class", "edit");
    $(this).text("[✎]");
});
$('#tbl').on('click','.delete',function() {
    rows = $(this).parent().siblings();
});

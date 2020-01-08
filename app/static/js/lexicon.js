
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        var csrftoken = $('meta[name=csrf-token]').attr('content');
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
        xhr.setRequestHeader("Content-type", "application/json");
    }
})

document.addEventListener("DOMContentLoaded", function(){
    var term_id = $('#id').val();
    if (term_id === "") {
        $('#gloss_pane').hide();
        $('#delete').hide();
    }
});

$('#newGlossBtn').on('click', function(e) {
    var m = $('#newGlossModal');
    m.modal('show');
});

// Callbacks for gloss creating
$('#newGlossModalSubmit').on('click', function(e) {
    var term_id = $('#id').val();

    var m = $('#newGlossModal');

    var gloss = m.find('#newGlossGloss').val();
    var source = m.find('#newGlossSource').val();
    var page = m.find('#newGlossPage').val();

    var data = JSON.stringify(
        {"term_id": term_id, "gloss": gloss, "source": source, "page": page}
    );

    $.ajax({
        type: "POST",
        url: "/gloss/",
        data: data,
        success: function(response) {
            m.modal('hide');
            location.reload();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert(xhr.responseText);
        }
    });
});

// Callbacks for gloss editing

$('#gloss_tbl').on('click','.edit',function() {
    var rows = $(this).parent().siblings();

    var id = rows.filter(".id")[0].innerText;
    var gloss = rows.filter(".gloss")[0].innerText;
    var source = rows.filter(".source")[0].innerText;
    var page = rows.filter(".page")[0].innerText;

    var m = $('#editGlossModal');
    m.modal();

    m.find('#editGlossID').val(id);
    m.find('#editGlossGloss').val(gloss);
    m.find('#editGlossSource').val(source);
    m.find('#editGlossPage').val(page);
});

$('#editGlossModalSubmit').on('click', function(e) {
    var m = $('#editGlossModal');

    var id = m.find('#editGlossID').val();
    var gloss = m.find('#editGlossGloss').val();
    var source = m.find('#editGlossSource').val();
    var page = m.find('#editGlossPage').val();

    var data = JSON.stringify(
        {"id": id, "gloss": gloss, "source": source, "page": page }
    );

    $.ajax({
        type: "PUT",
        url: "/gloss/" + id,
        data: data,
        success: function(response) {
            m.modal('hide');
            location.reload();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            resp = JSON.parse(xhr.responseText);
            alert(resp.message);
        }
    });
});

$('#delete').on('click', function(e) {
    var id = $('#id').val();

    if (!confirm("Are you sure you want to delete entry " + id + "?")) {
        return;
    }

    var data = JSON.stringify( true )

    $.ajax({
        type: "DELETE",
        url: "/lexicon/" + id,
        data: data,
        success: function(response) {
            window.location.replace("/lexicon");
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert(xhr.responseText);
        }
    });

});


$('#gloss_tbl').on('click','.delete',function() {
    var rows = $(this).parent().siblings();

    var id = rows.filter(".id")[0].innerText;

    if (!confirm("Are you sure you want to delete this gloss?")) {
        return;
    }

    var data = JSON.stringify( true )

    $.ajax({
        type: "DELETE",
        url: "/gloss/" + id,
        data: data,
        success: function(response) {
            location.reload();
        },
        error: function(xhr, ajaxOptions, thrownError) {
            alert(xhr.responseText);
        }
    });

})

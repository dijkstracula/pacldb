
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        let csrftoken = $('meta[name=csrf-token]').attr('content');
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken)
        }
        xhr.setRequestHeader("Content-type", "application/json");
    }
})

document.addEventListener("DOMContentLoaded", function(){
    let term_id = $('#id').text();
    if (term_id === "") {
        $('#gloss_pane').hide();
        $('#delete').hide();
    }
});

$('#newGlossBtn').on('click', function(e) {
    let m = $('#newGlossModal');
    m.modal('show');
});

// Callbacks for gloss creating
$('#newGlossModalSubmit').on('click', function(e) {
    let term_id = $('#id').text();

    let m = $('#newGlossModal');

    let gloss = m.find('#newGlossGloss').val();
    let source = m.find('#newGlossSource').val();
    let page = m.find('#newGlossPage').val();

    let data = JSON.stringify(
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
    let rows = $(this).parent().siblings();

    let id = rows.filter(".id")[0].innerText;
    let gloss = rows.filter(".gloss")[0].innerText;
    let source = rows.filter(".source")[0].innerText;
    let page = rows.filter(".page")[0].innerText;

    let m = $('#editGlossModal');
    m.modal();

    m.find('#editGlossID').val(id);
    m.find('#editGlossGloss').val(gloss);
    m.find('#editGlossSource').val(source);
    m.find('#editGlossPage').val(page);
});

$('#editGlossModalSubmit').on('click', function(e) {
    let m = $('#editGlossModal');

    let id = m.find('#editGlossID').val();
    let gloss = m.find('#editGlossGloss').val();
    let source = m.find('#editGlossSource').val();
    let page = m.find('#editGlossPage').val();

    let data = JSON.stringify(
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
    let id = $('#id').text();

    if (!confirm("Are you sure you want to delete entry " + id + "?")) {
        return;
    }

    let data = JSON.stringify( true )

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
    let rows = $(this).parent().siblings();

    let id = rows.filter(".id")[0].innerText;

    if (!confirm("Are you sure you want to delete this gloss?")) {
        return;
    }

    let data = JSON.stringify( true )

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

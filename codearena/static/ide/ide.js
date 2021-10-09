
let editor;

window.onload = function(){
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/c_cpp");
    $(".inputSection").hide()
}

function changetheme(){
    let theme = $("#theme").val();

    editor.setTheme(theme);
}

function changelanguage(){
    let language = $("#languages").val();

    if(language == 'c' || language == 'cpp')editor.session.setMode("ace/mode/c_cpp");
    else if(language == "py")editor.session.setMode("ace/mode/python");
}

function ischecked(cbox){
    $(".inputSection").toggle(cbox.checked);
}

function runCode(){
    
    $.ajax({

        url:"/compiler",

        method:"POST",

        data:{
            language : $("#languages").val(),
            code : editor.getSession().getValue(),
            input: $(".input").val(),
        },

        beforeSend: function(){
            $("#loader").removeClass("d-none");
        },

        success : function(response){
            $("#loader").addClass("d-none");
            $(".output").text (response)
        },
    })
}
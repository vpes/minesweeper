window.do_login = function(el){
    var $form = $("#login_form");
    var $user = $("#username").val();
    var $password = $("#password").val();
    if (! $user) {
        $("#username").addClass("required");
        return false;
    }
    else{
        $("#username").removeClass("required");
    }
    if (! $password) {
        $("#password").addClass("required");
        return false;
    }
    else{
        $("#password").removeClass("required");
    }
    $.ajax({
            headers: { "Accept": "application/json"},
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({"email": $user,
                    "password": $password}),
            dataType: 'json',
            url: "http://localhost:8008/v1/login/",
            crossDomain: true,
          //   beforeSend: function(xhr){
          //       xhr.withCredentials = true;
          // },
            success: function(data, textStatus, request){
                $("#game").data("auth", data.body.results[0].response);
                $("#login_container").hide();
                $("#game_container").show();
            }
})
};


window.create_board = function (el_name, rows, cols){
    var $el = $(el_name);
    if ($el.empty()){
        create_game(el_name, rows, cols);
    }
};

window.create_game = function (el_name, rows, cols, mines=40){
    $.ajax({
            headers: { "Accept": "application/json",
                "Authorization" : "Token " + $("#game").data("auth").token
            },
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({"rows": rows,
                    "columns": cols,
                    "mines_count": mines}),
            dataType: 'json',
            url: "http://localhost:8008/v1/game/",
            crossDomain: true,
            beforeSend: function(xhr){
                xhr.withCredentials = true;
          },
            success: function(data, textStatus, request){
                console.log(data);
                $("#game").data("id", data.body.results[0].id).data("mines", mines)
                $("#message").hide();
                $(".start_button").hide();
                var $table = $('<table>').addClass('game');
                for(i=0; i<rows; i++){
                    var row = $('<tr>').addClass('row');
                    for (j=0; j<cols; j++){
                        var cell = $('<td>');
                        cell.append($('<div>').addClass('cell')
                            .data('row',i)
                            .data('col',j)
                        .attr("id","r"+i+"c"+j)
                        );
                        row.append(cell);
                    }
                    $table.append(row);
                }
                var $el = $(el_name);
                $el.html($table);
                $('div.cell').contextmenu(function() {
                    return false;
                            }).on( "mousedown", function(event) {
                    event.preventDefault();
                    var data = $( this ).data();
                    switch (event.which) {
                        case 1:
                            select_cell( data.row, data.col);
                            break;
                        case 3:
                            toggle_flag( data.row, data.col);
                            break;
                    }
                    return false;
                });
            }

})
};

window.toggle_flag = function (row, col) {
    $.ajax({
        url: "http://localhost:8008/v1/game/" + $("#game").data("id") + "/toggle_flag/",
        headers: {"Accept": "application/json",
                "Authorization" : "Token " + $("#game").data("auth").token
        },
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({"row": row,
                "col": col}),
        dataType: 'json',
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.withCredentials = true;
        },
        success: (function (data) {
            var flag_data = data.body.results[0];
            console.log(flag_data);
            $("#flags").text(flag_data.flag_count + " / " + $("#game").data("mines"));
            var $cell = $("#r"+row+"c"+col);
            switch (flag_data.flag) {
                case 0:
                    $cell.text("").addClass("default").removeClass("flag");
                    break;
                case 1:
                    $cell.text("X").addClass("flag").removeClass("default");
                    break;
                case 2:
                    $cell.text("?").addClass("flag").removeClass("default");;
                    break;
                    }
        })
})
};

window.select_cell = function (row, col) {
    var $cell = $("#r"+row+"c"+col);
    if ($cell.data("selected"))
        return false;
    $cell.data("selected", true);
    $.ajax({
        url: "http://localhost:8008/v1/game/" + $("#game").data("id") + "/select_cell/",
        headers: {"Accept": "application/json",
                "Authorization" : "Token " + $("#game").data("auth").token
        },
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({"row": row,
                "col": col}),
        dataType: 'json',
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.withCredentials = true;
        },
        success: (function (data) {
            var cell_data = data.body.results[0];
            console.log(cell_data);
            if (cell_data.cells){
                for (var i=0; i < cell_data.cells.length;i++){
                    var cell_tuple = cell_data.cells[i];
                    var $cell = $("#r"+cell_tuple[0]+"c"+cell_tuple[1]);
                    $cell.text(cell_tuple[2]).addClass("selected");
                }
            }
        })
})
};

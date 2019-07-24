//Local url API
window.API_URL = "http://localhost:8008/v1/";
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
            url: window.API_URL + "login/",
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

window.create_board = function (el_name, rows, cols, mines=40){
    var $el = $(el_name);
    if ($el.empty()){
        create_game(el_name, rows, cols, mines);
    }
};

window.create_custom_board = function (el_name, rows, cols){
    var $rows = $("#input_rows").val();
    var $cols = $("#input_cols").val();
    var $mines = $("#input_mines").val();
    if (! $rows || $rows < 3 || $rows > 1000) {
        $("#input_rows").addClass("required");
        $("#message").text("Please fill the Rows value (a numbre between 3 and 1000)")
        return false;
    }
    else{
        $("#input_rows").removeClass("required");
        $("#message").text("Click the button to start")
    }
    if (! $cols || $cols < 3 || $cols > 1000) {
        $("#input_cols").addClass("required");
        $("#message").text("Please fill the Columns value (a numbre between 3 and 1000)")
        return false;
    }
    else{
        $("#input_cols").removeClass("required");
        $("#message").text("Click the button to start")
    }
    var board_size = $cols * $rows;
    if (! $mines || $mines < 1 || $mines > 96) {
        $("#input_mines").addClass("required");
        $("#message").text("Please fill the Columns value (a numbre between 3 and 1000)")
        return false;
    }
    else{
        $mines = Math.floor(board_size * $mines / 100);
        $("#input_mines").removeClass("required");
        $("#message").text("Click the button to start")
    }
    create_board(el_name, $rows, $cols, $mines);
};

window.create_game = function (el_name, rows, cols, mines=60){
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
            url: window.API_URL + "game/",
            crossDomain: true,
            beforeSend: function(xhr){
                xhr.withCredentials = true;
          },
            success: function(data, textStatus, request){
                console.log(data);
                var game_data = data.body.results[0];
                var rows = game_data.board.length;
                var columns = game_data.board[0].length;
                $("#game").data("id", data.body.results[0].id)
                          .data("mines", mines)
                          .data("rows", rows)
                          .data("columns", columns)
                          .data("status", "started");
                $("#message").hide();
                $("#menu").hide();
                $("#flags").text( "0 / " + $("#game").data("mines"));
                $(".start_button").hide();
                var $table = $('<table>').addClass('game');
                for(i=0; i<rows; i++){
                    var row = $('<tr>').addClass('row');
                    for (j=0; j<columns; j++){
                        var cell = $('<td>');
                        var $cell_div = $('<div>').addClass('cell')
                            .data('row',i)
                            .data('col',j)
                            .attr("id","r"+i+"c"+j);
                        var $game_cell =  game_data.board[i][j];
                        if ($game_cell.v){
                           $cell_div.text($game_cell.n > 0?$game_cell.n:"").addClass('selected');
                        }
                        else if ($game_cell.f){
                            switch ($game_cell.f) {
                                case 0:
                                    $cell_div.text("").addClass("default").removeClass("flag");
                                    break;
                                case 1:
                                    $cell_div.text("F").addClass("flag").removeClass("default");
                                    break;
                                case 2:
                                    $cell_div.text("?").addClass("flag").removeClass("default");;
                                    break;
                            }
                        }
                        cell.append($cell_div);
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
    var $cell = $("#r"+row+"c"+col);
    if ($cell.data("selected") || $("#game").data("status") != "started")
        return false;
    $.ajax({
        url: window.API_URL + "game/" + $("#game").data("id") + "/toggle_flag/",
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
                    $cell.text("F").addClass("flag").removeClass("default");
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
    if ($cell.data("selected") || $("#game").data("status") != "started")
        return false;
    $cell.data("selected", true);
    $.ajax({
        url: window.API_URL + "game/" + $("#game").data("id") + "/select_cell/",
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
                if (cell_data.cells.length === 1 && cell_data.cells[0][2] === -1){
                    draw_mines(); // Draw the hidden mines
                    var cell_tuple = cell_data.cells[0];
                    var $cell = $("#r"+cell_tuple[0]+"c"+cell_tuple[1]);
                    $cell.text("#").addClass("bomb");
                    $("#game").data("status", "lose");
                    $("#message").show().text("You loose");
                }
                else if (cell_data.cells.length === 1 && cell_data.cells[0][2] === -1000){
                    var cell_tuple = cell_data.cells[0];
                    var $cell = $("#r"+cell_tuple[0]+"c"+cell_tuple[1]);
                    $cell.text("#").addClass("bomb");
                    $("#game").data("status", "win");
                    $("#message").show().text("You win!!");
                }
                else{
                    // For debugging purposes
                    // if (!$("#game").data("mine_list"))
                    //     draw_mines();
                    for (var i=0; i < cell_data.cells.length;i++){
                        var cell_tuple = cell_data.cells[i];
                        var $cell = $("#r"+cell_tuple[0]+"c"+cell_tuple[1]);
                        $cell.text(cell_tuple[2] > 0?cell_tuple[2]:"").addClass("selected");
                }}
            }
        })
})
};

window.draw_mines = function(){
    $.ajax({
        url: window.API_URL + "game/" + $("#game").data("id") + "/get_mines/",
        headers: {"Accept": "application/json",
                "Authorization" : "Token " + $("#game").data("auth").token
        },
        type: 'GET',
        async: false,
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.withCredentials = true;
        },
        success: (function (data) {
            var mine_list = data.body.results;
            var $game = $("#game");
            $game.data("mine_list", mine_list);
            var rows = $game.data("rows");
            var columns = $game.data("columns");
            for (var i=0; i<mine_list.length; i++){
                var row = Math.floor(mine_list[i] / rows);
                var column = mine_list[i] % columns;
                var $cell = $("#r"+row+"c"+column).text("O").addClass("hidden_mine");
            }
        })
    })
}

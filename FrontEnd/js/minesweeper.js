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

window.create_game = function (el_name, rows, cols){
    $.ajax({
            headers: { "Accept": "application/json",
                "Authorization" : "Token " + $("#game").data("auth").token
            },
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({"rows": rows,
                    "columns": cols,
                    "mine_count": 40}),
            dataType: 'json',
            url: "http://localhost:8008/v1/game/",
            crossDomain: true,
            beforeSend: function(xhr){
                xhr.withCredentials = true;
          },
            success: function(data, textStatus, request){
                console.log(data);
                $("#message").hide();
                var $table = $('<table>').addClass('game');
                for(i=0; i<rows; i++){
                    var row = $('<tr>').addClass('row');
                    for (j=0; j<cols; j++){
                        var cell = $('<td>');
                        cell.append($('<div>').addClass('cell').data('row',i).data('col',j));
                        row.append(cell);
                    }
                    $table.append(row);
                }
                $el.html($table);
                $('div.cell').on( "click", function() {
                    var data = $( this ).data();
                    select_cell( data.row, data.col);
                });
            }

})
};

window.select_cell = function (row, col) {
    $.ajax({
        url: "http://localhost:8008/v1/game/select_cell",
        headers: {"Accept": "application/json"},
        type: 'POST',
        crossDomain: true,
        beforeSend: function (xhr) {
            xhr.withCredentials = true;
        },
        success: (function (data) {
            if (console && console.log) {
                console.log("Data:", data);
            }
        })
})
};

window.create_board = function (el_name, rows, cols){
    var $el = $(el_name);
    if ($el.empty()){
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
}

window.select_cell = function (row, col){
    $.ajax({
  url: "http://localhost:8008/v1/game/select_cell",
        async: true
})
  .done(function( data ) {
    if ( console && console.log ) {
      console.log( "Data:", data );
    }
  });
}

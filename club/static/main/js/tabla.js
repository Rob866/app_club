//tabla de alumnos
var $table = $('#table')

 function buildTable($el, cells, rows) {
   var i; var j; var row
   var columns = []
   var data = []

   for (i = 0; i < cells; i++) {
     columns.push({
       field: 'field' + i,
       title: 'Cell' + i,
       sortable: true
     })
   }
   for (i = 0; i < rows; i++) {
     row = {}
     for (j = 0; j < cells; j++) {
       row['field' + j] = 'Row-' + i + '-' + j
     }
     data.push(row)
   }
   $el.bootstrapTable({
     columns: columns,
     data: data,
     detailView: cells > 1,
     onExpandRow: function (index, row, $detail) {
       /* eslint no-use-before-define: ["error", { "functions": false }]*/
       expandTable($detail, cells - 1)
     }
   })
 }

 function expandTable($detail, cells) {
   buildTable($detail.html('<table></table>').find('table'), cells, 1)
 }

 $(function() {
   buildTable($table, 8, 1)
 })

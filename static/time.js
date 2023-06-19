$(function() {
  function cb(start, end) {
    $('#reportrange span').html(start.format('MMMM D, YYYY HH:mm A') + ' - ' + end.format('MMMM D, YYYY HH:mm A'));
  }
  var start = moment().subtract(29, 'days');
  var end = moment();
  $('#reportrange').daterangepicker({
    startDate: start,
    endDate: end,
    timePicker: true,
    timePicker24Hour: true,
    ranges: {
      'Today': [moment(), moment()],
      'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
      'Last 7 Days': [moment().subtract(6, 'days'), moment()],
      'Last 30 Days': [moment().subtract(29, 'days'), moment()],
      'This Month': [moment().startOf('month'), moment().endOf('month')],
      'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
    }
  }, cb);
  $("#reportrange").on("apply.daterangepicker", function(ev, picker) {
    var startDate = picker.startDate.format('YYYY-MM-DD HH:mm:ss A');
    var endDate = picker.endDate.format('YYYY-MM-DD HH:mm:ss A');
    var selectedTable = $("input[name='table_name']:checked").val();
    console.log(selectedTable);
    $.ajax({
      url: "/range",
      type: "POST",
      data: {
        start: startDate,
        end: endDate,
        table_name: selectedTable
      },
     success: function(data) {
       console.log(data);  // Check the response object in the browser console
       $('#averageodo').html(data);
       $('#averageodo').append(data.htmlresponse);
}
    });
  });
  $("input[name='table_name']").change(function() {
    var startDate = $('#reportrange').data('daterangepicker').startDate;
    var endDate = $('#reportrange').data('daterangepicker').endDate;
    var selectedTable = $(this).val();
    console.log(selectedTable);

    $.ajax({
      url: "/range",
      type: "POST",
      data: {
        start: startDate.format('YYYY-MM-DD HH:mm:ss A'),
        end: endDate.format('YYYY-MM-DD HH:mm:ss A'),
        table_name: selectedTable
      },
      success: function(data) {
        console.log(data);  // Check the response object in the browser console
 $('#averageodo').html(data);
       $('#averageodo').append(data.htmlresponse);
}
    });
  });
  cb(start, end);
});
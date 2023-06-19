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

  // Function to handle the AJAX request
  function sendCountRequest() {
    var startDate = $('#reportrange').data('daterangepicker').startDate;
    var endDate = $('#reportrange').data('daterangepicker').endDate;
    var selectedTable = $("input[name='table_name']:checked").val();
    var lowerLimit = $("#lower_limit").val();
    var upperLimit1 = $("#upper_limit1").val();
    var upperLimit2 = $("#upper_limit2").val();

    $.ajax({
      url: "/count",
      type: "POST",
      data: {
        start: startDate.format('YYYY-MM-DD HH:mm:ss A'),
        end: endDate.format('YYYY-MM-DD HH:mm:ss A'),
        table_name: selectedTable,
        lower_limit: lowerLimit,
        upper_limit1: upperLimit1,
        upper_limit2: upperLimit2
      },
      success: function(data) {
        console.log(data);
        $('#acceleration').html(data.htmlresponse);
        updateIdCount(data.id_count); // Call the function to update id_count value
      },
      error: function(xhr, status, error) {
        console.log(xhr.responseText);
        // Handle error if the request fails
      }
    });
  }

  // Function to update the id_count value
  function updateIdCount(idCount) {
    $('#id_count').text(idCount);
  }

  // Add event listener to date range selection
  $("#reportrange").on("apply.daterangepicker", function(ev, picker) {
    sendCountRequest();
  });

  // Add event listener to table selection
$("input[name='table_name']").on("change", function() {
  sendCountRequest();
});

  // Form submit event handler
  $("#count-form").submit(function(event) {
    event.preventDefault(); // Prevent form submission and page refresh
    sendCountRequest();
    // After sending the request, update id_count value
    updateIdCount("Loading..."); // Show a loading message
  });

  cb(start, end);
});

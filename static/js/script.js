(function() {
  var TIMEOUT = 20000;
  var loadingImg = '<img id="loadingImage" src="/static/img/ajax-loader.gif" />';

    var errored = function(xml, status, message, $elem) {
      if (status === "timeout") {
        $elem.html("Timed out. Try again.");
      } else {
        $elem.html("Something went wrong. Try again.");
      }
      return null;
    };

    var updateValue = function(url, text, $elem, success) {
      $elem.append(loadingImg);
      $.ajax({
        url: url,
        type: "POST",
        timeout: TIMEOUT,
        data: {"text": text},
        dataType: "json",
        success: success,
        error: function(xml, status, message) {
          errored(xml, status, message, $elem);
        }
      });
    };

    var fetchOpenClasses = function() {
      var $sentDiv = $("#resultTable");
      $sentBtn = $("#analyzeOpenClass");
      if ($sentDiv.is(":visible")) {
        $sentDiv.hide();
        $sentBtn.removeClass("active");
      } else {
        $sentDiv.show();
        var $sentTable = $("#resultTable table");
        var $tbody = $sentTable.children("tbody");
        updateValue("/scrapeOpen", "", $tbody, function(res){
          $sentBtn.addClass("active");
          $tbody.empty();

          var sentences = res.result;
          if (sentences.length <= 0) {
            $tbody.append("<tr>" +
                          "<td>I'm sad :(</td>" +
                          "<td>No open classes found</td>" + 
                          "</tr>");
          } else {
            sentences.forEach(function(elem, index) {
              $tbody.append("<tr>" +
                "<td>" + elem.course + "</td>" +
                "<td>" + elem.instructor + "<br/><br/>" + elem.CCN + "</td>" + 
                "<td>" + elem.rec + "</td>" +
                "<td>" + elem.desc + "</td>" +
                "</tr>");
            });

            // Initialize data tables
            $("#all-open-classes").dataTable( {
              "sDom": "<'row'fr>t<'row'<'span12'l><'span12'ip>>",
              "sPaginationType": "bootstrap",
              "sDefaultContent": "",
              "bInfo": false,
              "bAutoWidth": false,
              "bLengthChange": false,
              "bPaginate": false,
              "oLanguage": {
                  "sLengthMenu": "_MENU_  records per page",
                  "sEmptyTable": "No Open Classes Found :("
              },
              "aoColumns" : [
                  { sWidth: '50px' },
                  { sWidth: '100px' },
                  { sWidth: '120px' },
                  { sWidth: '30px' }
              ]  
            });

            $("#all-open-classes_filter label input").attr("id", "searchbox"); // add ID for highlighting

            $("#searchbox").keyup(function() {
              $("#all-open-classes").removeHighlight();
              $("#all-open-classes").highlight($("#searchbox").val());
            });
          }
        });
      }
    };

    $("#analyzeOpenClass").one('click', function(e){
      e.preventDefault();
      fetchOpenClasses();
      $("#analyzeOpenClass").attr("disabled", "disabled");
    });

    var fetchEnrollment = function(text) {
      var $sentDiv = $("#enrollmentTable");
      $sentBtn = $("#analyzeEnrollment");
      text = text.trim();  // trim whitespace from both ends

      if ($sentDiv.is(":visible")) {
        $sentDiv.hide();
        $sentBtn.removeClass("active");
      } else {
        $sentDiv.show();
        var $sentTable = $("#enrollmentTable table");
        var $tbody = $sentTable.children("tbody");
        updateValue("/checkEnrollment", text, $tbody, function(res) {
          $sentBtn.addClass("active");
          $tbody.empty();
          var sentences = res.result;
          if (sentences.length <= 0 || !text.trim()) {
            $tbody.append("<tr>" +
              "<td>I'm sad :(</td>" +
              "<td>Bear is crying...</td>" +
              "<td>jk, try again</td>" + 
              "</tr>");
          } else {   
            sentences.forEach(function(elem, index) {         
              $tbody.append("<tr>" + 
                "<td>" + elem.course + "</td>" +
                "<td>" + elem.stats +"</td>" + 
                "<td>" + elem.category +"</td>" + 
                "</tr>");
            });
          }
        });
      }
    };

    // Click handlers
    $("#analyzeEnrollment").on("click", function(e) {
      e.preventDefault();
      var text = $("textarea[name='text']")[0].value;
      fetchEnrollment(text);
    });
}).call(this);
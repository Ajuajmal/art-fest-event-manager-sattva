$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-participant .modal-content").html("");
        $("#modal-participant").modal("show");
      },
      success: function (data) {
        $("#modal-participant .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#participant-table tbody").html(data.html_participant_list);
          location.reload(true);
          $("#modal-participant").modal("hide");
        }
        else {
          $("#modal-participant .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create participant
//  $(".js-create-participant").click(loadForm);
//  $("#modal-participant").on("submit", ".js-participant-create-form", saveForm);

  // Update participant
//  $("#participant-table").on("click", ".js-update-participant", loadForm);
//  $("#modal-participant").on("submit", ".js-participant-update-form", saveForm);

  // Delete participant
  $("#participant-table").on("click", ".js-delete-participant", loadForm);
  $("#modal-participant").on("submit", ".js-participant-delete-form", saveForm);

});

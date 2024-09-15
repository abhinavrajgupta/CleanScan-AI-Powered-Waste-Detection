window.onload = () => {
  $("#sendbutton").click(() => {
    $("#link").css("visibility", "visible");
    $("#download").attr("href", "static/");
  });
};

function readUrl(input) {
  imagebox = $("#imagebox");
  console.log(imagebox);
  console.log("evoked readUrl");
  if (input.files && input.files[0]) {
    let reader = new FileReader();
    reader.onload = function (e) {
      console.log(e.target);

      imagebox.attr("src", e.target.result);
      imagebox.height(500);
      imagebox.width(800);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

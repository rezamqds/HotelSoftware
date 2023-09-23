function calc() {
  var n = checkNumberToEn($("#number").val().split(",").join(""));
  if (n) {
    var a = Num2persian(n);
    $("#word").text(a+" تومان "), $("#show").removeClass("d-none");
  }
}

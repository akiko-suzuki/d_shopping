$(function(){
    $("form").attr("novalidate", "novalidate");
    $("input").removeAttr("required");

    // sidebar非表示
    $("#close-sidebar").on("click", function() {
        $(".page-wrapper").removeClass("toggled");
    });
    // sidebar表示
    $("#close-sidebar").on("click", function() {
        $(".page-wrapper").addClass("toggled");
    });

    // メッセージのfadeOut時間
    setTimeout("$('.alert').fadeOut()", 4000)
});

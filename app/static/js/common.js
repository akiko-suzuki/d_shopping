$(function(){
    $("form").attr("novalidate", "novalidate");
    $("input").removeAttr("required");

    // sidebar非表示
    $("#close-sidebar").on("click", function() {
        $(".page-wrapper").removeClass("toggled");
    });
    // sidebar表示
    $("#show-sidebar").on("click", function() {
        $(".page-wrapper").addClass("toggled");
    });

    // メッセージのfadeOut時間
    setTimeout("$('.alert').fadeOut()", 4000)

    // Enterキーでsubmitの制御
    // TODO 管理側の画面だけにする
    $(document).on('keypress', function(event) {
        return event.which !== 13;
    });
//    $(document).on('keypress', 'input:not(.allow_submit)', function(event) {
//        return event.which !== 13;
//    });
});

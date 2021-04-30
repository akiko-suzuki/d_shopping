$(function(){
    // sidebar非表示
    // 「$("#close-sidebar").on("click", function() {}」の形だとイベントが発火しない
    //（「.on("click", function() {}」は動的に追加した要素に対して発火しない挙動になってるが、今回は別ファイルとして読み込んでるから？）
    $(document).on("click", "#close-sidebar", function() {
        $(".page-wrapper").removeClass("toggled");
    });
    // sidebar表示
    $(document).on("click", "#show-sidebar", function() {
        $(".page-wrapper").addClass("toggled");
    });
});
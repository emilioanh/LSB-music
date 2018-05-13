$(function(){
    $("audio").on("play", function() {
        $("audio").not(this).each(function(index, audio) {
            audio.pause();
            var id = audio.currentSrc.split("=").pop();
            var unselectedRow = document.getElementById(id);
            $(unselectedRow).removeClass('active');
        });
    });
});

function playEvent(element){
    var id = element.currentSrc.split("=").pop();
    var selectedRow = document.getElementById(id);
    $(selectedRow).addClass('active');
}
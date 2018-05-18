$(function(){
    var message = $('.messages');
    if(message){
        var decrBool = message.find('#watermark');
        if(decrBool.length>0){
            setTimeout(()=>{
                message.hide();
            }, 3000);
        }else{
            setTimeout(()=>{
                message.hide();
                $('.ui.basic.modal').modal('hide');
            }, 3000);
        }
    }
    $('.ui.basic.modal').modal('show');
    switch (window.location.pathname){
        case "/":
            $("#home").addClass("active");
            break;                    
        case "/decode":
            $("#check").addClass("active");
            break;
        case "/login/":
            $("#login_nav").addClass("active");
            break;
        case "/signup":
            $("#signup_nav").addClass("active");
            break;
        case "/mysong":
            $("#mysong").addClass("active");
            break;
    }
});

function playEvent(element){
    var id = element.currentSrc.split("=").pop();
    var selectedRow = document.getElementById(id);
    $(selectedRow).addClass('active');
    $("audio").each((index,audio)=>{
        if(audio!=element){
            audio.pause();
            var id = audio.currentSrc.split("=").pop();
            var unselectedRow = document.getElementById(id);
            $(unselectedRow).removeClass('active');
        }
    });
}
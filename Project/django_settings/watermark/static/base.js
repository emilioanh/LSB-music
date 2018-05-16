$(function(){
    $('audio').on('play', function() {
        $("audio").not(this).each(function(index, audio) {
            audio.pause();
            var id = audio.currentSrc.split("=").pop();
            var unselectedRow = document.getElementById(id);
            $(unselectedRow).removeClass('active');
        });
    });
    var login = $('#login');
    var signup = $('#signup');
    if(login.length){
        login.addClass('disabled');
    }else if(signup.length){
        signup.addClass('disabled');
    }
    $('form div input').blur(function(){
        if(this.value==""){
            if(login.length){
                $('#login').removeClass('disabled');
                $('#login').addClass('disabled');
            }else if(signup.length){
                $('#signup').removeClass('disabled');
                $('#signup').addClass('disabled');
            }
        }else{
            if(login.length){
                $('#login').removeClass('disabled');
            }else if(signup.length){
                $('#signup').removeClass('disabled');
            }
        }
    });
    var message = $('.messages');
    if(message){
        setTimeout(function(){
            message.hide();
            $('.ui.basic.modal').modal('hide');
        }, 3000);
    }
    $('.ui.basic.modal').modal('show');
});

function playEvent(element){
    var id = element.currentSrc.split("=").pop();
    var selectedRow = document.getElementById(id);
    $(selectedRow).addClass('active');
}
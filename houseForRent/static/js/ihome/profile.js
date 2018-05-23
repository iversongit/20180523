function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#form-avatar").submit(function(e){
        alert("form-avatar");
        e.preventDefault();
        // avatar = $('#avatar').val();
        $(this).ajaxSubmit({  //提交文件
           url:'/user/user/',
           type:'PUT',
           dataType:'json',
           success:function (data) {
                if(data.code == '200'){
                    $('#user-avatar').attr('src',data.url)
                    // location.href = "/user/profile/"
                }
           },
           error:function () {
               alert("上传头像失败")
           }
        });
    });

    $('#form-name').submit(function (e) {
        alert("form-name");
        $('.error-msg').hide();
        e.preventDefault();
        var username = $('#user-name').val();
        $.ajax({
           url:'/user/user/',
           type:'PUT',
           dataType:'json',
           data:{'username':username},
           success:function(data) {
               alert("lalala");
               alert(data.code);
                if(data.code=='1007'){
                    $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>'+data.msg);
                    $('.error-msg').show();
                    // location.href = "/user/profile/"
                }else if(data.code=='200'){
                    showSuccessMsg();
                    // $('.error-msg').hide();
                }
           },
           error:function () {
               alert("fail");
           }
        });
    });
});


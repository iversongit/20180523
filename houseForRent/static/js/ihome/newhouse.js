function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/house/area_facility/',function (data) {
        var area_list_html = '';
        for(var i=0; i<data.area_list.length; i++){
            var area_html = '<option value="'+ data.area_list[i].id +'">'+ data.area_list[i].name +'</option>';
            area_list_html += area_html
        }
        $('#area-id').html(area_list_html);

        var facility_list_html = '';
         for(var i=0; i<data.facility_list.length; i++){
            var facility_html = '';
            facility_html +=  '<li><div class="checkbox"><label>';
            facility_html += '<input type="checkbox" name="facility" value="'+ data.facility_list[i].id +'">'+ data.facility_list[i].name;
            facility_html += '</label></div></li>';
            facility_list_html += facility_html
        }
        $('.house-facility-list').html(facility_list_html)

    });

    $('#form-house-info').submit(function (e){
        e.preventDefault();
        alert("form-house-info");
        $(this).ajaxSubmit({
            url:'/house/add_house/',
            type:'POST',
            dataType:'json',
            success:function (data) {
                if(data.code==200){
                    alert("form-house-info 200");
                    $('#house-id').val(data.houseid);
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                }
            },
            error:function (data) {
                alert("fail")
            }
        });
    });

    $('#form-house-image').submit(function (e){
        e.preventDefault();
        alert("form-house-image");
        $(this).ajaxSubmit({   // 提交整个表单，包括图片
            url:'/house/add_picture/',
            type:'POST',
            dataType:'json',
            success:function (data) {
                if(data.code==200){
                    alert("form-house-image 200");
                    image = $('<img>').attr('src',data.url);
                    $('.house-image-cons').append(image);
                }
            },
            error:function (data) {
                alert("fail")
            }
        });
    });
});

// $('#form-house-info').submit(function () {
//    e.preventDefault();
//    alert($(this).serialize());
//    $.post('/house/add_house/',$(this).serialize(),function (data) {
//        if(data.code == '200'){
//           $('#house-id').val(data.houseid);
//           $('#form-house-info').hide();
//           $('#form-house-image').show();
//        }
//    }) ;
//    return false;
// });

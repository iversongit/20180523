function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function swiper(){  // 循环加载滚动图（每隔两秒切换一张）
     var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    });
}

$(document).ready(function(){
    swiper();
    $(".book-house").show();
    // window.location.search:获取当前网址的参数部分
    $.get('/house/housedetail/'+ window.location.search,function (data) {
       alert('/house/housedetail/');
       if(data.code==200){
           // if(data.booking==0){   // 如果为房主本人，隐藏预定按钮
           //    $('.book-house').hide();
          // }
           // 使用template.js模版渲染引擎
           // 将需要渲染的部分置于script之中，给script命名为house_detail_list
           // ohouse仅仅在script中生效
            var detail_house = template('house_detail_list',{ohouse:data.house});
           //在script中渲染的部分本来就是.contrain区域的一部分，
           //渲染完毕后仍然需要将其拼接回去
            $('.container').append(detail_house);
            swiper();
            $(".book-house").show();
       }
   });

});
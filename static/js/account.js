/**
 * Created by q1367 on 2017/7/18.
 */
function loginF() {
    $.ajax({
        url:"/account/login/",
        dataType:"json",
        contentType:"application/json",
        type:"post",
        success:function () {
            window.location.href = "/home/";
        },
        error:function (json) {
            var message = json.message;
            $(".message").attr("text", message);
        }
    })
}

function registerF() {
    $.ajax({
        url:"/account/register/",
        dataType:"json",
        contentType:"application/json",
        type:"post",
        success:function () {
            $(".message").attr("text", "注册成功")
        },
        error:function (json) {
            var message = json.message;
            $(".message").attr("text", message);
        }
    })
}

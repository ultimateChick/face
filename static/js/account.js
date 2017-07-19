/**
 * Created by q1367 on 2017/7/18.
 */

// $(document).ready(function () {
//     $.ajaxSetup = {async:false};
// });

function getLoginFormInfo() {
    var info = {
            "username_or_email": $("#login_form").find("#username_or_email").val(),
            "password": $("#login_form").find("#password").val()
    };
    return info;
}

function loginF() {
    $.ajax({
        url:"/account/login/",
        data:JSON.stringify(getLoginFormInfo()),
        processData: false,
        dataType:"json",
        contentType:"application/json",
        type:"post",
        success:function () {
            window.location.href = "/home/";
        },
        error:function (json) {
            var message = json.message;
            // $(".message").attr("text", message);
            alert(JSON.stringify(json));

        }
    })
}

function getRegisterFormInfo() {
    var info = {
            "username": $("#signup_form").find("#username").val(),
            "email": $("#signup_form").find("#email").val(),
            "password": $("#signup_form").find("#password").val(),
            "repeat_password": $("#signup_form").find("#password2").val()
    };
    return info;
}

function registerF() {
    $.ajax({
        url:"/account/register/",
        dataType:"json",
        contentType:"application/json",
        data:JSON.stringify(getRegisterFormInfo()),
        processData: false,
        type:"post",
        success:function () {
            alert("成功");

        },
        error:function (json) {
            var obj=jQuery.parseJSON(json);
            console.log(obj);
            console.log(obj.status);       //取json.dumps(data)字典的值status
            console.log(obj.msg);
            console.log(obj.data);
            alert("失败");
        }
    })
}

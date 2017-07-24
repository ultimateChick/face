/**
 * Created by lee on 17-7-19.
 */
function urlload() {
        if($('#imgurl').val() != ""){
        //$("#imgWait").show();
        var formData = new FormData();
        $('#uplPic').hide();
        $('#uplPic').attr('src', $('#imgurl').val());
        $('#uplPic').show();

        //formData.append("myfile", document.getElementById("file1").files[0]);
        formData.append("img_url", $("#imgurl").val());
        $.ajax({
            url:"/detect/api/",
            type:"post",
            data:formData,
            contentType: false,
            processData:false,
            success:function (data) {
                var dict = data.info;
                /*alert(JSON.stringify(data));*/

                $("#info").find("#age").attr("value", dict.age);
                $("#info").find("#sex").attr("value", dict.gender);
                $("#info").find("#race").attr("value", dict.ethnicity);
                $("#info").find("#emotion").attr("value", dict.emotion);
                $("#info").find("#smile").attr("value", dict.smile);
                $("#info").find("#left-eye").attr("value", dict.lefteye);
                $("#info").find("#right-eye").attr("value", dict.righteye);
            },
            error:function (json) {
                var dict = json.responseJSON;

            }
        });
    }
}


 function localload(){

    if($("#file1").val() != ''){

         var formData = new FormData();

        formData.append("myfile", document.getElementById("file1").files[0]);
        var reader = new FileReader();
        reader.readAsDataURL(document.getElementById("file1").files[0]);
        reader.onload = function (e) {
            //$('#file1').hide();
            $('#uplPic').hide();
            $('#uplPic').attr('src', e.target.result);
            $('#uplPic').show();
            //$('#uplPic').css('display','inline');

        }
        //formData.append("img_url", $("#upload").val());
        $.ajax({
            url:"/detect/api/",
            type:"post",
            data:formData,
            contentType: false,
            processData:false,
            success:function (data) {
                var dict = data.info;
               // alert(JSON.stringify(data));

                $("#info").find("#age").attr("value", dict.age);
                $("#info").find("#sex").attr("value", dict.gender);
                $("#info").find("#race").attr("value", dict.ethnicity);
                $("#info").find("#emotion").attr("value", dict.emotion);
                $("#info").find("#smile").attr("value", dict.smile);
                $("#info").find("#left-eye").attr("value", dict.lefteye);
                $("#info").find("#right-eye").attr("value", dict.righteye);
            },
            error:function (json) {
                var dict = json.responseJSON;

            }
        });
    }
}
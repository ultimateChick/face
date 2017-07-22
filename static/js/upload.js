/**
 * Created by lee on 17-7-19.
 */
function upload() {
    $("#upload").click(function () {
        $("#imgWait").show();
        var formData = new FormData();
        formData.append("myfile", document.getElementById("file1").files[0]);
        $.ajax({
            url:"/detect/api/",
            type:"post",
            data:formData,
            contentType: false,
            processData:false,
            success:function (data) {
                alert(JSON.stringify(data));
                var dict = data.responseJSON.info;
                $("#info").find("#age").attr("value", dict.age);
                $("#info").find("#sex").attr("value", dict.gender);
                $("#info").find("#race").attr("value", dict.ethnicity);
                $("#info").find("#emotion").attr("value", dict.emotion);
                $("#info").find("#smile").attr("value", dict.smile);
                $("#info").find("#eye").attr("value", dict.eyestatus)
            },
            error:function (json) {
                var dict = json.responseJSON;
                
            }
        })
    });
}

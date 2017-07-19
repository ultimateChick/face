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
            }
        })
    });
}

function urlload() {
        if(($('#imgurl').val() != "")&&($('#imgurl2').val() != "")){
        //$("#imgWait").show();
        var formData = new FormData();
        /*$('#uplPic1').hide();*/
        $('#uplPic1').attr('src', $('#imgurl1').val());
        $('#uplPic2').attr('src', $('#imgurl2').val());
        /*$('#uplPic1').show();*/

        //formData.append("myfile", document.getElementById("file1").files[0]);
        formData.append("img_url1", $("#imgurl1").val());
        formData.append("img_url2", $("#imgurl2").val());
        $.ajax({
            url:"/compare/api/",
            type:"post",
            data:formData,
            contentType: false,
            processData:false,
            success:function (data) {
                var dict = data.info;
                alert(JSON.stringify(data));
              
               /* $("#info").find("#age").attr("value", dict.age);
                $("#info").find("#sex").attr("value", dict.gender);
                $("#info").find("#race").attr("value", dict.ethnicity);
                $("#info").find("#emotion").attr("value", dict.emotion);
                $("#info").find("#smile").attr("value", dict.smile);
                $("#info").find("#left-eye").attr("value", dict.lefteye)
                $("#info").find("#right-eye").attr("value", dict.righteye)*/
            },
            error:function (json) {
                var dict = json.responseJSON;

            }
        });
    }
}

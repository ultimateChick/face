function showPic(input) {
    if (input.files && input.files[0]) {
      if(/image\/\w+/.test(input.files[0].type)){
        var reader = new FileReader();

        reader.onload = function (e) {
          var max = $("#upload").width();
          $("#drop").hide();
          $("#stage").show();

          $('#uplPic').attr('src', e.target.result);

          // fitting the picture to its parent node
          $('#uplPic').hide();

          $("#uplPic").attr("width", max);

          // var picwd = $("#uplPic").width();
          // var picht = $("#uplPic").height();
          // var factor = maxwd / picwd;
          // picwd = maxwd;
          // picht = factor * picht;
          // if(picht > maxht) {
          //   factor = maxht / picht;
          //   picht = maxht;
          // } else {
          //   factor = 1;
          // }
          // picwd = factor * picwd;
          //
          // $('#uplPic').attr("height", picht);
          // $('#uplPic').attr("width", picwd);
          $("#uplPic").show();

        }
        reader.readAsDataURL(input.files[0]);
      }else {
        alert("not image!");
        window.location.refresh();
    }
  }
}

$("input[name=upl]").change(function(){
    showPic(this);
});

$(function(){
    $("stage").hide();
    var ul = $('#upload ul');

    $('#drop a').click(function(){
        // Simulate a click on the file input button
        // to show the file browser dialog
        $(this).parent().find('input').click();
    });

    // Initialize the jQuery File Upload plugin
    $('#upload').fileupload({
        // how to use these parameter
        // https://github.com/blueimp/jQuery-File-Upload/wiki/Options

        url : "/detect",
        type : "POST",
        dataType : "json",

        // This element will accept file drag/drop uploading
        dropZone: $('#drop'),

        // This function is called when a file is added to the queue;
        // either via the browse button, or via drag/drop:
        add: function (e, data) {

            // data.files[0] is odd so prewing is done by readURL

            var tpl = $('<li class="working"><input type="text" value="0" data-width="48" data-height="48"'+
                ' data-fgColor="#0788a5" data-readOnly="1" data-bgColor="#3e4043" /><p></p><span></span></li>');

            // Append the file name and file size
            tpl.find('p').text(data.files[0].name)
                         .append('<i>' + formatFileSize(data.files[0].size) + '</i>');

            // Add the HTML to the UL element
            data.context = tpl.appendTo(ul);

            // Initialize the knob plugin
            tpl.find('input').knob();

            // Listen for clicks on the cancel icon
            tpl.find('span').click(function(){

                if(tpl.hasClass('working')){
                    jqXHR.abort();
                }

                tpl.fadeOut(function(){
                    tpl.remove();
                });

            });

            // Automatically upload the file once it is added to the queue
            var jqXHR = data.submit();

            // The jqXHR object returned by $.ajax()
            // a superset of the browser's native XMLHttpRequest object.
            // to read more : http://api.jquery.com/jQuery.ajax/#jqXHR

            if (jqXHR.readyState==4 && jqXHR.status==200)
              {
                console.log(jqXHR.responseText);
                var responseText = jQuery.parseJSON(jqXHR.responseText);
                console.log(responseText);
              }


        },

        progress: function(e, data){

            // Calculate the completion percentage of the upload
            var progress = parseInt(data.loaded / data.total * 100, 10);

            // Update the hidden input field and trigger a change
            // so that the jQuery knob plugin knows to update the dial
            data.context.find('input').val(progress).change();

            if(progress == 100){
                data.context.removeClass('working');
            }
        },

        fail:function(e, data){
            // Something has gone wrong!
            data.context.addClass('error');
        }

    });


    // Prevent the default action when a file is dropped on the window
    $(document).on('drop dragover', function (e) {
        e.preventDefault();
    });

    // Helper function that formats the file sizes
    function formatFileSize(bytes) {
        if (typeof bytes !== 'number') {
            return '';
        }

        if (bytes >= 1000000000) {
            return (bytes / 1000000000).toFixed(2) + ' GB';
        }

        if (bytes >= 1000000) {
            return (bytes / 1000000).toFixed(2) + ' MB';
        }

        return (bytes / 1000).toFixed(2) + ' KB';
    }

});

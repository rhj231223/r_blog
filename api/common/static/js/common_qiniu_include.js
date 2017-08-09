/**
 * Created by renhuijun on 2017/8/10.
 */
"use strict";

//上传文件的函数
$(function(){
    var upload_btn=$('#upload_btn');

    xtqiniu.setUp({
        upload_btn:'upload_btn',
        success:function(up,file,info){
            window.file_url=file.name;
            upload_btn.attr('src',window.file_url);
        }
    })

});
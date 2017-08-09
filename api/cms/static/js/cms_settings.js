/**
 * Created by renhuijun on 2017/8/10.
 */
"use strict";

$(function(){
    var submit_btn=$('#submit_btn');
    submit_btn.click(function(event){
        event.preventDefault();
        var username=$('input[name=username]').val();
        var avatar=$('#upload_btn').attr('src');

        rhjajax.post({
            url:'/cms/settings/',
            data:{
                username:username,
                avatar:avatar,
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('用户信息更新成功！')
                    setTimeout(function(){
                        window.location.reload();
                    },1200)
                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        })

    })
});



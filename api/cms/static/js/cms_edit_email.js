/**
 * Created by renhuijun on 2017/8/10.
 */
'use strict';
//发送邮件的函数
$(function(){
    var send_btn=$('#send_btn');
    send_btn.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]').val();

        rhjajax.post({
            url:'/cms/captcha_email/',
            data:{
                email:email,
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('邮件发送成功!')
                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        })
    })
});


//修改邮箱的函数
$(function(){
    var submit_btn=$('#submit_btn');
    submit_btn.click(function(event){
        event.preventDefault();

        var email=$('input[name=email]')
        var email_captcha=$('input[name=email_captcha]')

        rhjajax.post({
            url:'/cms/edit_email/',
            data:{
                email:email.val(),
                email_captcha:email_captcha.val(),
            },
            success:function(data){
                if(data['code']==200){
                    email.val('');
                    email_captcha.val('');
                    xtalert.alertSuccessToast('邮件修改成功!')
                }else{
                    xtalert.alertInfo(data['message'])
                }
            },
        })
    })
});
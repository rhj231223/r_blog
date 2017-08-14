/**
 * Created by renhuijun on 2017/8/14.
 */

'use strict';

$(function () {
    var comment_btn=$('#comment_btn');
    comment_btn.click(function(){
        var content=$('textarea[name=content]');
        var article_id=comment_btn.attr('data_article_id');

        rhjajax.post({
            url:window.location.href,
            data:{
                content:content.val(),
            },
            success:function(data){
                if(data['code']==200){
                    xtalert.alertSuccessToast('回复提交成功!');
                    setTimeout(function(){
                        window.location='/article_detail/'+article_id+'/#footer'
                    },1200)
                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        })
    })
});

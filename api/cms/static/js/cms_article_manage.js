/**
 * Created by renhuijun on 2017/8/11.
 */
'use strict';
//过滤功能的函数
$(function(){
    var select=$('select[name=category]');
    select.change(function(){
        var value=$(this).val();

        window.location='/cms/article_manage/1/'+value+'/';
    })
});

//置顶功能的函数
$(function(){
    var top_btn=$('.top_btn');
    top_btn.click(function(event){
        event.preventDefault();

        var article_id=$(this).attr('data_article_id');
        var is_top=$(this).attr('data_is_top');
        var category_id=$('select[name=category]').val();

        rhjajax.post({
            url:'/cms/top_article/',
            data:{
                article_id:article_id,
                is_top:is_top,
            },
            success:function(data){
                if(data['code']==200){
                    var msg='';
                    if(is_top='1'){
                        msg='置顶操作成功!';
                        xtalert.alertSuccessToast(msg);
                        setTimeout(function(){
                            window.location='/cms/article_manage/1/'+category_id+'/'
                    },1200)
                    }else{
                        msg='取消置顶成功!'
                        xtalert.alertSuccessToast(msg);
                        setTimeout(function() {
                            window.location.reload();
                        })
                        }


                }else{
                    xtalert.alertInfo(data['message'])
                }
            }
        })

    })
});

//删除操作的函数

$(function(){
    var delete_btn=$('.delete_btn');
    delete_btn.click(function (event) {
        event.preventDefault();

        var article_id=$(this).attr('data_article_id');
        var is_remove=$(this).attr('data_is_remove');

        rhjajax.post({
            url:'/cms/delete_article/',
            data:{
                article_id:article_id,
                is_remove:is_remove,
            },
            success:function(data){
                if(data['code']==200){
                    var msg='';
                    if(is_remove=='1'){
                        msg='删除操作成功!';
                    }else{
                        msg='取消删除成功!'
                    }
                    xtalert.alertSuccessToast(msg);
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

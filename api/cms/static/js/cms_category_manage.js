/**
 * Created by renhuijun on 2017/8/12.
 */

//编辑操作的函数
$(function(){
    var edit_btn=$('.edit_btn');
    edit_btn.click(function(event){
        event.preventDefault();

        var category_id=$(this).attr('data_category_id');
        var category_name=$(this).attr('data_category_name');
        var self=$(this);

        xtalert.alertOneInput({
            text:'请输入分类名称!',
            placeholder:category_name,
            confirmCallback:function(inputValue){
                rhjajax.post({
                    url:'/cms/edit_category/',
                    data:{
                        category_id:category_id,
                        category_name:inputValue,
                    },
                    success:function(data){
                        if(data['code']==200){
                            xtalert.alertSuccessToast('分类名修改成功!')
                            self.parent().parent().children().eq(0).text(inputValue);
                        }else{
                        xtalert.alertInfo(data['message'])
                    }
                    }
                })
            }
        })
    })
});

//删除分类的函数
$(function(){
    var delete_btn=$('.delete_btn');
    delete_btn.click(function(event){
        event.preventDefault();

        var category_id=$(this).attr('data_category_id');
        var category_name=$(this).attr('data_category_name');
        var self=$(this);

        xtalert.alertConfirm({
            text:'您确定要删除' + category_name + ' 分类吗?',
            confirmText:'删除',
            cancelText:'取消',
            confirmColor:'#CC0000',
            confirmCallback:function(){
                rhjajax.post({
                    url:'/cms/delete_category/',
                    data:{
                        category_id:category_id,
                    },
                    success:function(data){
                        if(data['code']==200){
                            self.parent().parent().hide(1000)
                        }else{
                            setTimeout(function(){
                                xtalert.alertInfo(data['message'])
                            },500)
                        }
                    },
                })
            },
        })
    })
});
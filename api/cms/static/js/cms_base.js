/**
 * Created by renhuijun on 2017/8/9.
 */
'use strict';

$(function(){
    var current_index=1;
    var nav_box=$('#nav_box');
    var current_url=window.location.href;
    if(current_url.indexOf('add_article')>0){
        current_index=2;
    }else{
        current_index=1;
    }
    nav_box.children().eq(current_index-1).addClass('active').siblings().removeClass('active')

});
/**
 * Created by renhuijun on 2017/8/9.
 */
'use strict';

$(function(){
    var graph_btn=$('#graph_btn');
    var graph_img=graph_btn.children('img')
    graph_btn.click(function(){
        var old_src=graph_img.attr('src');
        var new_src=xtparam.setParam(old_src,'xxx',Math.random())
        graph_img.attr('src',new_src);


    })
});
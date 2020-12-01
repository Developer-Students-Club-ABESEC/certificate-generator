function getMousePosition(canvas, event) {
    let rect = canvas.getBoundingClientRect();
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    $("#textmodal").show();
    $('#coordinates').val("The point you selected is: (" + x+"," + y+")");
    localStorage.setItem("x",x);
    localStorage.setItem("y",y);
}

let canvasElem = document.querySelector("canvas");
var config = {};
var i=0;
var image = "";

canvasElem.addEventListener("mousedown", function (e) {
    getMousePosition(canvasElem, e);
});

function draw(ev) {

document.getElementById("sec1").style.display = "none";
$("#loader").show();
var ctx = document.getElementById('canvas').getContext('2d'),
img = new Image(),
f = document.getElementById("uploadimage").files[0],
url = window.URL || window.webkitURL,
src = url.createObjectURL(f);
img.src = src;

img.onload = function() {

ctx.drawImage(img, 0, 0,842,595);
image = document.getElementById('canvas').toDataURL().replace('data:image/png;base64,', "");
url.revokeObjectURL(src);
}
$("#loader").hide();
$("#sec2").show();
}


function imageobject(id,size,color,x,y,font,text){
    var element = '<div class="objects" id="'+id+'" style="top:'+y+'px;left:'+x+'px">'+
            '<span style="font-size:'+ size+'px;font-family:'+font+';color:'+color+';">'+ text+'</span>'+
                '<span onclick="'+"delelement("+id+")"+'" class="clickable close">&times</span>'+
                '<i onclick="'+"move("+id+",'left',-1)"+'"class="clickable left fa fa-angle-left" style="font-size:24px"></i>'+
                '<i onclick="'+"move("+id+",'top',-1)"+'" class="clickable top fa fa-angle-up" style="font-size:24px"></i>'+
                '<i onclick="'+"move("+id+",'left',1)"+'" class="clickable right fa fa-angle-right" style="font-size:24px"></i>'+
                '<i onclick="'+"move("+id+",'top',1)"+'" class="clickable down fa fa-angle-down" style="font-size:24px"></i>'+
        '</div>'
    $("#container").append(element);
}

function move(id,side,val){
    var x = $("#"+id).position();
    if(side=="top"){
        val = x.top + val;
        $("#"+id).css({top:val,position:"absolute"});
        config[id]['y'] = val;
    }
    else{
        val = x.left + val;
        $("#"+id).css({left:val,position:"absolute"});
        config[id]['x'] = val;

    }
    console.log(config);


}

function delelement(id){
    $("#"+id).remove();
    i-=1;
    delete config[id];
    for(j=id;j<=i;j++){
        config[j] = config[j+1];
        $("#"+j).remove();
        if(config[j]!=null){
        imageobject(j,config[j]["size"],config[j]["color"],Number(config[j]["x"]),Number(config[j]["y"])+20,config[j]["style"],config[j]["text"]);
        }
    }
    delete config[i];
}

$("#addpoint").on("click",()=>{
    x = localStorage.getItem("x");
    y = localStorage.getItem("y");
    var ctx = document.getElementById("canvas").getContext("2d");
    font = $('#fonts').find(":selected").text();
    size =  $('#fontsize').find(":selected").text();
    ctx.font = size +"px "+font;
    text = $("#textfield").val();
    // color = $('#color').find(":selected").val();
    const color_get = $('#color').val();
    const r = parseInt(color_get.substr(1,2), 16);
    const g = parseInt(color_get.substr(3,2), 16);
    const b = parseInt(color_get.substr(5,2), 16);
    let color = `rgb(${r},${g},${b})`;
    imageobject(i,size,color,x,y-10,font,text);
    //ctx.fillText(text,x,y);
    insertrecord(x,y-30,color,size,font,text);
    $("#textmodal").hide();
    $("#textfield").val("");
});


    function insertrecord(x,y,color,fontsize,fontstyle,text){
        temp = {}
         key = $('#keys').find(":selected").text();
         temp["text"] = text;
         temp["column"] = key;
         temp["x"] = x;
         temp["y"] =y;
         temp["color"] = color;
         temp["size"] = fontsize
         temp["style"] = fontstyle
        config[i] = temp;
        i+=1;
    }


document.getElementById("uploadimage").addEventListener("change", draw, false);


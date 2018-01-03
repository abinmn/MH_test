$(document).ready(function(){
    let data_global={};

    //Generate the clickable thumbnails
    jQuery.getJSON("/static/mhsite/assets/gallery/images.json",function(data){
        data_global=data;
        for(let album in data){
            for(let image in data[album]){
                if(image=='thumb'){
                    let s="<div class='col s6 m3 l3'><div id='"+album+"'class='card waves-effect waves-light'><div class='card-image'><img src='/static/mhsite/assets/gallery"+data[album][image]+"'><span class='card-title'>MH-site</span></div></div></div>";
                    $('#thumbs').append(s);
                }
            }
        }
        
        //Initialize carousel in gallery page for inital load
        let s="<div class='carousel carousel-slider' data-indicators='true'>";
        for(let image in data[Object.keys(data)[0]]){
            if(image!='thumb'){
                s=s+"<div class='carousel-item'><img src='/static/mhsite/assets/gallery"+data[Object.keys(data)[0]][image]+"'></div>";
            }
        }
        s=s+"</div>";
        $('.carousel-container').html(s);
        $('.carousel').carousel({fullWidth:true});
    });

    //Next and previous arrow move the carousal
    /*$('.carousal-container').on('click','.moveNextCarousel',function(e){
        e.preventDefault();
        e.stopPropagation();
        $('.carousel').carousel('next');
     });
  
     // move prev carousel
     $('.carousal-container').on('click','.movePrevCarousel',function(e){
        e.preventDefault();
        e.stopPropagation();
        $('.carousel').carousel('prev');
     });*/

    //Clicking on thumbnail changes carousel content to that album
    $('#thumbs').on('click','.card',function(){
        let album=$(this).attr('id');
        //let s="<div class='carousel carousel-slider' data-indicators='true'><div class='left'><a class='movePrevCarousel middle-indicator-text waves-effect waves-light content-indicator'><i class='material-icons left middle-indicator-text'>chevron_left</i></a></div><div class='right'><a class='moveNextCarousel middle-indicator-text waves-effect waves-light content-indicator'><i class='material-icons right middle-indicator-text'>chevron_right</i></a></div>";
        let s="<div class='carousel carousel-slider' data-indicators='true'>";
        for(let image in data_global[album]){
            if(image!='thumb'){
                s=s+"<div class='carousel-item'><img src='/static/mhsite/assets/gallery"+data_global[album][image]+"'></div>";
            }
        }
        s=s+"</div>";
        $("html, body").animate({ scrollTop: 0 }, 750);
        $('.carousel-container').html(s);
        $('.carousel').carousel({fullWidth:true});

    });
});
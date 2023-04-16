(function() {
  /*  
  ...customise bootstrap carousel 
  ...change bootstrap carousel interval
  */
  $('#carousel-item').carousel({
    interval: 4000
  });
}());

(function() {
  $('.carousel-multiItem  .item').each(function() {
    var itemToClone = $(this);
    /*
    .....number  of item show  in slide  !
    */
    for (var i = 1; i < 3; i++) {
      /* 
        ..... go to the  next  item  in curasol 
      */
      itemToClone = itemToClone.next();

      /*  ....
        when that  item is last  item  in cauarsol-item  do this choos first sibling item and 
         go to do  add it , clone, add class, and add to collection
      */

      /*    else..... 
            skip this  condition and go to  add item content  and  clone it ....
      */

      if (!itemToClone.length) {
        itemToClone = $(this).siblings(':first');
      }

      /* 
        .... show the first-child in item class  " this div contain the content inside in" 
        ... then clone this selector "clearly meaning copy the data"
        ...  and give  it tha css style 
        ...  then add it  to collection in slide 
      */
      itemToClone.children(':first-child').clone()
        .addClass("cloneditem-" + (i))
        .appendTo($(this));

      $(".carousel-multiItem ").find(".item").css("transition", "   500ms ease-in-out all  ").css("transition", "  500ms ease-in-out all").css("backface-visibility", "visible").css("transform", "none!important")

      /*
       .... you  can  use  bootstrap function  if you used bootstrap CDN 
       .... but iam used  always  bootstrap.min.js   so  i do  this 
      
       .... @media all and (min-width: 768px) and (transform-3d),
           all and (min-width: 768px) and (-webkit-transform-3d)
      
      */

    }
  });
}());
$('#carouselExample').on('slide.bs.carousel', function (e) {
    var carousel = e.target;
    var itemsPerSlide = 3;
    var totalItems = $('.carousel-item', carousel).length;
    var currentSlide = $('div.active', carousel).index();

    // Check if the last slide is a complete set of items
    var delta = itemsPerSlide - (totalItems % itemsPerSlide);
    if (delta != itemsPerSlide) {
        // Append the remaining items to the end of the carousel
        for (var i=0; i<delta; i++) {
            var $item = $('.carousel-item', carousel).eq(i);
            $item.clone().appendTo($('.carousel-inner', carousel));
        }
    }

    // Remove any blank spaces in the carousel
    $('.carousel-item', carousel).removeClass('prev next');

    // Wait for the images to load before appending the items
    $('.carousel-item img', carousel).on('load', function() {
        if (currentSlide >= totalItems-(itemsPerSlide-1)) {
            var it = itemsPerSlide - (totalItems - currentSlide);
            for (var i=0; i<it; i++) {
                // Append slides to end
                if (e.direction=="left") {
                    $('.carousel-item', carousel).eq(i).appendTo($('.carousel-inner', carousel));
                }
                else {
                    $('.carousel-item', carousel).eq(totalItems-i-1).prependTo($('.carousel-inner', carousel));
                }
            }
        }

        // Add appropriate classes to the items in the carousel
        $('.carousel-item', carousel).each(function () {
            var $this = $(this);
            var slideIndex = $this.index();
            var slidesPerPage = itemsPerSlide;
            var delta = totalItems - slideIndex;

            if (delta <= slidesPerPage) {
                $this.addClass('next');
            }
            else if (delta > (totalItems - slidesPerPage)) {
                $this.addClass('prev');
            }
            else {
                $this.removeClass('prev next');
            }
        });
    });
});

function resize() {
    if ($(window).width() < 700) {
        $('.desktop-navigation').hide()
        $('.mobile-navigation').show()
        $('.desktop-player').hide()
        $('.mobile-player').show()
    } else {
        $('.desktop-navigation').show()
        $('.mobile-navigation').hide()
        $('.desktop-player').show()
        $('.mobile-player').hide()
    }
}

function collapse_desktop_sidebar() {
    $('.key-ideas').fadeOut(100)
    $('.font-size-modifier').fadeOut(100)
    $('.explore').fadeOut(100)
    $('.library').fadeOut(100)
    $('.sidebar-separator').fadeOut(100)
    $('.font-size-modifier-arrow').fadeOut(100)
    $('.menu-bar').addClass('menu-bar--collapsed')
    $('.collapse-button').removeClass('rotate-180')
}

function expand_desktop_sidebar() {
    $('.key-ideas').fadeIn(700)
    $('.font-size-modifier').fadeIn(700)
    $('.sidebar-separator').fadeIn(700)
    $('.explore').fadeIn(700)
    $('.library').fadeIn(700)
    $('.font-size-modifier-arrow').fadeIn(700)
    $('.menu-bar').removeClass('menu-bar--collapsed')
    $('.collapse-button').addClass('rotate-180')
}

function expand_font_size_modifier() {
    $('.font-size-modifier-arrow').removeClass('rotate-180')
    $('.font-size-list').empty()
    $('.font-size-list').append(`
    <div class="flex flex-row font-medium mr-6 mb-4">
		<button type="button" data-size="text-base" class="w-10 h-8 text-dark-grey cursor-pointer flex justify-center items-center border-2 border-solid border-light-grey hover:border-green rounded-sm ml-4 last:mr-0 text-base">
			ما
		</button>
		<button type="button" data-size="text-xl" class="w-10 h-8 text-dark-grey cursor-pointer flex justify-center items-center border-2 border-solid border-light-grey hover:border-green rounded-sm ml-4 last:mr-0 text-xl">
			ما
		</button>
		<button type="button" data-size="text-2xl" class="w-10 h-8 text-dark-grey cursor-pointer flex justify-center items-center border-2 border-solid border-light-grey hover:border-green rounded-sm ml-4 last:mr-0 text-2xl">
			ما
		</button>
	</div>
    `)

    let active_font_size = $('.reader-content__text').attr('class').split(' ').pop()

    $('.flex-row button').each(function () {
        if ($(this).hasClass(active_font_size)) {
            $(this).removeClass('border-light-grey').addClass('border-green')
        }
    });
}

function collapse_font_size_modifier() {
    $('.font-size-list').empty()
    $('.font-size-modifier-arrow').addClass('rotate-180')
}

$(window).on('resize', function () {

    resize()
});

$(document).ready(function () {

    resize()

    $('.collapse-button').click(function () {
        if ($('.menu-bar').hasClass('menu-bar--collapsed')) {
            expand_desktop_sidebar()
        } else {
            if (!$('.font-size-modifier-arrow').hasClass('rotate-180')) {
                collapse_font_size_modifier()
            }
            collapse_desktop_sidebar()
        }
    })

    $('.font-size-modifier-parent').click(function () {
        if ($('.menu-bar').hasClass('menu-bar--collapsed')) {
            expand_desktop_sidebar()
        }
        if ($('.font-size-modifier-arrow').hasClass('rotate-180')) {
            expand_font_size_modifier()
        } else {
            collapse_font_size_modifier()
        }
    })

    $('.font-size-list').on('click', 'button', function () {
        $('.font-size-list').find('button').removeClass('border-green').addClass('border-light-grey')
        $(this).removeClass('border-light-grey').addClass('border-green')
        $('.reader-content__text').removeClass('text-base').removeClass('text-xl').removeClass('text-2xl')
        let textSize = $(this).data('size')
        $('.reader-content__text').addClass(textSize)
    });

    $('.key-ideas-div').on('click', function () {
        if ($('.key-ideas-sidebar').hasClass('opacity-100')) {
            $(".key-ideas-sidebar").removeClass("opacity-100").addClass("opacity-0").css("display", "none");
        } else {
            $(".key-ideas-sidebar").removeAttr("style").removeClass("opacity-0").addClass("opacity-100");
        }
    });

    let sidebar = $('.key-ideas-popup');

    $(document).mouseup(function (e) {
        if (!sidebar.is(e.target) && sidebar.has(e.target).length === 0) {
            $(".key-ideas-sidebar").removeClass("opacity-100").addClass("opacity-0").css("display", "none");
        }
    });
    
});

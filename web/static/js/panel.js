$(document).ready(function () {

    $("#historymenbtn").click(function () {
        $("#Cartads").hide();
        $("#boysales").hide();
        $("#pricesec").hide();
        $("#settinpanel").hide();

        $("#history").show();
        $("#verfery").hide();

    });


    $("#settinpanel").hide();
    $("#verfery").hide();
    $("#vvv").click(function () {
        $("#verfery").show();
        $("#history").hide();

        $("#Cartads").hide();
        $("#boysales").hide();
        $("#pricesec").hide();
        $("#settinpanel").hide();


    });
    $("#pricesec").hide();
    $("#pricebtn1").click(function () {
        $("#Cartads").hide();
        $("#boysales").hide();
        $("#pricesec").show();
        $("#history").hide();

        $("#settinpanel").hide();


        $("#verfery").hide();

    });


    $("#boysales").hide();
    $("#salebuy").click(function () {
        $("#Cartads").hide();
        $("#history").hide();

        $("#settinpanel").hide();

        $("#pricesec").hide();

        $("#boysales").show();

        $("#verfery").hide();
        $("#lable222").hide();
        $("#lable22").hide();
        $("#nextstep123").hide();
        $("#nextstep1234").hide();
        $("#button1234").hide();
        $("#asd").hide();
    });

    $("#Cartads").hide();
    $("#adnewscart").click(function () {
        $("#Cartads").show();
        $("#history").hide();

        $("#settinpanel").hide();

        $("#boysales").hide();
        $("#pricesec").hide();

        $("#verfery").hide();

    });


    $("#button123").click(function () {
        $("#history").hide();

        $("#lable222").show();
        $("#lable22").show();
        $("#nextstep123").show();
        $("#settinpanel").hide();

        $("#nextstep1234").show();
        $("#button1234").show();
        $("#asd").show();

    });


    $("#settingmenu").click(function () {
        $("#history").hide();

        $("#settinpanel").show();
        $("#Cartads").hide();

        $("#boysales").hide();
        $("#pricesec").hide();

        $("#verfery").hide();
    });


    /* For the sticky navigation */
    $('.js--section-features').waypoint(function (direction) {
        if (direction == "down") {
            $('nav').addClass('sticky');
        } else {
            $('nav').removeClass('sticky');
        }
    }, {
        offset: '60px;'
    });


    /* Scroll on buttons */
    $('.js--scroll-to-plans').click(function () {
        $('html, body').animate({scrollTop: $('.js--section-plans').offset().top}, 1000);
    });

    $('.js--scroll-to-start').click(function () {
        $('html, body').animate({scrollTop: $('.js--section-features').offset().top}, 1000);
    });


    /* Navigation scroll */
    $(function () {
        $('a[href*=#]:not([href=#])').click(function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html,body').animate({
                        scrollTop: target.offset().top
                    }, 1000);
                    return false;
                }
            }
        });
    });


    /* Animations on scroll */
    $('.js--wp-1').waypoint(function (direction) {
        $('.js--wp-1').addClass('animated fadeIn');
    }, {
        offset: '50%'
    });

    $('.js--wp-2').waypoint(function (direction) {
        $('.js--wp-2').addClass('animated fadeInUp');
    }, {
        offset: '50%'
    });

    $('.js--wp-3').waypoint(function (direction) {
        $('.js--wp-3').addClass('animated fadeIn');
    }, {
        offset: '50%'
    });

    $('.js--wp-4').waypoint(function (direction) {
        $('.js--wp-4').addClass('animated pulse');
    }, {
        offset: '50%'
    });


    /* Mobile navigation */
    $('.js--nav-icon').click(function () {
        var nav = $('.js--main-nav');
        var icon = $('.js--nav-icon i');

        nav.slideToggle(200);

        if (icon.hasClass('ion-navicon-round')) {
            icon.addClass('ion-close-round');
            icon.removeClass('ion-navicon-round');
        } else {
            icon.addClass('ion-navicon-round');
            icon.removeClass('ion-close-round');
        }
    });
});

function setamount() {
    let source_currency;
    let destionatio_currency;
    let source_amount;
    source_currency = document.getElementsByName("source_currency")[0].value;
    destionatio_currency = document.getElementsByName("destination_currency")[0].value;
    source_amount = document.getElementsByName("source_amount")[0].value;
    // alert(source_currency)
    // alert(destionatio_currency)
    // alert(source_amount);
    let webaddress = document.location.origin;
    const Http = new XMLHttpRequest();
    let url = webaddress + '/coin/' + destionatio_currency;
    Http.open("GET", url);
    Http.send()
    Http.onreadystatechange = (e) => {
        response = Http.responseText
        parsedresponse = JSON.parse(response)
        if (source_currency == 'USD') {
            result = source_amount / parsedresponse.USD
        }
        if (source_currency == 'IRR') {
            result = source_amount / (parsedresponse.IRR * parsedresponse.USD)
        }
        document.getElementsByName("destination_amount")[0].value = result
    }
}
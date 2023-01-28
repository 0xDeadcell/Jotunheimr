function updateFormFields(appContent) {
    // get app data
    let name = appContent.find('.app-name').text();
    let desc = appContent.find('.app-desc').text();
    let tag = appContent.closest('.app-tag-wrapper').find('.app-tag').text();
    let customUrl = appContent.find('.app-custom-url').val();
    let enableCustomUrl = appContent.find('.app-enable-custom-url').val();

    // if the customurl is not set, then the app_enable_custom_url should be set to false
    if (appContent.find('.app-custom-url').val().trim() === '') {
        enableCustomUrl = "false";
    }

    // update form fields
    $('#updateName').val(name);
    $('#updateDesc').val(desc);
    $('#updateTag').val(tag);
    $('#updateCustomUrl').val(customUrl);

    // update modal title
    $('#updateAppModal').find('.modal-title').text('Edit ' + name + ' App');

    if (enableCustomUrl.toLowerCase() === 'true' || enableCustomUrl === 'on') {
        $('#updateEnableCustomUrl').prop('checked', true);
        $('#updateCustomUrl').prop('disabled', false);
    } else {
        $('#updateEnableCustomUrl').prop('checked', false);
        $('#updateCustomUrl').prop('disabled', true);
    }

    // listen to the checked state of the checkbox of app_enable_custom_url, if checked, enable the custom url input
    $('#updateEnableCustomUrl').on('change', function(e) {
        if ($(this).is(':checked')) {
            $('#updateCustomUrl').prop('disabled', false);
        } else {
            $('#updateCustomUrl').prop('disabled', true);
        }
    });
}



$(document).on('click', '#addAppBtn', function(e) {
    e.preventDefault();
    $('#addAppModal').modal('show');
});

$(document).on('click', '.update-btn-wrapper', function(e) {
    $(this).closest('.app-actions-wrapper').removeClass('d-none');

    // get app data
    let appContent = $(this).closest('.card-wrapper');
    // update form fields
    updateFormFields(appContent);

    // update modal form action, replace space with underscore
    $('#updateAppModal').find('form').attr('action', `/api/app/${appContent.find('.app-name').text().toLowerCase().trim().replace(/\s/g, '_')}/update`);

    // show modal
    $('#updateAppModal').modal('show');
});

$(document).on('mouseenter', '.card', function(e) {
    //$(this).find('.app-actions-wrapper').css('background-color', 'rgba(0, 0, 0, 0.4)');
    $(this).parent().find('.app-actions-wrapper').toggleClass('d-none');
});

$(document).on('mouseleave', '.app-actions-wrapper', function(e) {
    $(this).toggleClass('d-none');
});

$(document).on('mouseenter', '.delete-btn-wrapper, .update-btn-wrapper', function(e) {
    $(this).closest('.app-actions-wrapper').css('background-color', 'rgba(0, 0, 0, 0.4)');
    $(this).css('opacity', '1');
});

$(document).on('mouseleave', '.delete-btn-wrapper, .update-btn-wrapper', function(e) {
    $(this).closest('.app-actions-wrapper').css('background-color', 'rgba(0, 0, 0, 0)');
    $(this).css('opacity', '0');
});

$(document).on('click', '.delete-btn-wrapper', function(e) {
    $(this).children('form').submit();
});

// on the checked state of the checkbox of app_enable_custom_url
$(document).on('change', '#app_enable_custom_url', function(e) {
    if ($(this).is(':checked')) {
        $('#app_custom_url').prop('disabled', false);
    } else {
        $('#app_custom_url').prop('disabled', true);
    }
});


// add some javascript so that the navbar-burger will work
$(document).ready(function() {
    $('.navbar-burger').click(function() {
        $('.navbar-burger').toggleClass('is-active');
        $('.navbar-menu').toggleClass('is-active');
    });
});

$(document).ready(function() {
    $('.group-title').each(function() {
        let customIcon = $(this).find('#custom-icon');
        if (customIcon.width() === 0 || customIcon.height() === 0) {
            customIcon.addClass('fa-fw fas fa-tools');
        }
    });
});


// set toggleDisplayModeBtn to toggle:
// @media screen and (min-width: 769px), print
// .columns:not(.is-desktop) {
//     display: flex;
// }

$(document).ready(function() {
    let toggleDisplayModeBtn = $('#toggleDisplayModeBtn');
    let columns = $('.columns');
    let isDesktop = columns.hasClass('is-desktop');

    // get the local storage value of displayMode
    let displayMode = localStorage.getItem('displayMode');
    // if the displayMode is not set, then set it to flex
    if (displayMode === null) {
        localStorage.setItem('displayMode', 'flex');
    }
    console.log(displayMode);

    // get the default width
    let defaultWidth = columns.find('.app-tag-wrapper').css('width');
    let maxdefaultWidth = columns.find('.app-tag-wrapper').css('max-width');
    // if the columns is not desktop, then the display mode is list
    // set the button to toggle between flex and block
    toggleDisplayModeBtn.on('click', function(e) {
        if (!isDesktop) {
            // find app-tag-wrapper column and set the width to 100%
            columns.find('.app-tag-wrapper').css('width', '100%');
            columns.find('.app-tag-wrapper').css('max-width', '100%');
            // set the columns to list
            columns.removeClass('is-desktop');
            columns.addClass('is-mobile');
            // set the button to toggle between flex and block
            columns.css('display', 'block');
        } else {
            // return to the default width
            columns.find('.app-tag-wrapper').css('max-width', maxdefaultWidth);
            columns.find('.app-tag-wrapper').css('width', defaultWidth);
            // set the columns to flex
            columns.removeClass('is-mobile');
            columns.addClass('is-desktop');
            // set the button to toggle between flex and block
            columns.css('display', 'flex');
        }

        // store the display mode in local storage
        if (isDesktop) {
            localStorage.setItem('displayMode', 'flex');
            console.log('block');
        }
        else {
            localStorage.setItem('displayMode', 'block');
            console.log('flex');
        }

        isDesktop = !isDesktop;
    });

    if (displayMode === 'block') {
        // if the displayMode is block, and the columns display is not block, then set the columns display to block
        if (columns.css('display') !== 'block') {
            // click the button to toggle the display mode
            toggleDisplayModeBtn.click();
        }
    } else if (displayMode === 'flex') {
        // if the displayMode is flex, and the columns display is not flex, then set the columns display to flex
        if (columns.css('display') !== 'flex') {
            // click the button to toggle the display mode
            toggleDisplayModeBtn.click();
        }
    }
});


// change the class="theme-default page-default is-light" to class="theme-default page-default is-dark" to change the theme when the toggleDarkModeBtn is clicked if the div with id="app" has the class "is-light" or "is-dark"
$(document).ready(function() {
    let toggleDarkModeBtn = $('#toggleDarkModeBtn');
    let app = $('#app');
    let isDark = app.hasClass('is-dark');
    let isLight = app.hasClass('is-light');

    // if the page is loaded and the local storage has a theme, then set the theme to the local storage theme
    if (localStorage.getItem('theme') === 'is-dark') {
        app.removeClass('is-light');
        app.addClass('is-dark');
        isDark = true;
        isLight = false;
    } else if (localStorage.getItem('theme') === 'is-light') {
        app.removeClass('is-dark');
        app.addClass('is-light');
        isDark = false;
        isLight = true;
    }
    toggleDarkModeBtn.on('click', function(e) {
        if (isDark) {
            app.removeClass('is-dark');
            app.addClass('is-light');
        } else if (isLight) {
            app.removeClass('is-light');
            app.addClass('is-dark');
        }
        isDark = !isDark;
        isLight = !isLight;

        // store the current theme in the local storage
        if (isDark) {
            localStorage.setItem('theme', 'is-dark');
        }
        if (isLight) {
            localStorage.setItem('theme', 'is-light');
        }
    });
});





// if the page is mobile, then set the columns to block
if ($(window).width() < 769) {
    $('.columns').css('display', 'block');
}
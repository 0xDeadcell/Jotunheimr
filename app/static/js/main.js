// set the dark wallpaper image globally

// get the background image from the api /api/get_background?theme=dark, light
var darkBackgroundImage = null;
var lightBackgroundImage = null;
$(document).ready(function() {
    $.ajax({
        url: '/api/get_background?theme=dark',
        type: 'GET',
        success: function(data) {
            darkBackgroundImage = data;
        }
    });
    $.ajax({
        url: '/api/get_background?theme=light',
        type: 'GET',
        success: function(data) {
            lightBackgroundImage = data;
        }
    });
});


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
        }
        else {
            localStorage.setItem('displayMode', 'block');
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

    toggleDarkModeBtn.on('click', function(e) {
        if (isDark) {
            app.removeClass('is-dark');
            app.addClass('is-light');

            // set the toggleDarkModeBtn icon to the correct icon
            toggleDarkModeBtn.children('i').removeClass('fa-moon');
            toggleDarkModeBtn.children('i').addClass('fa-sun');
        } else if (isLight) {
            app.removeClass('is-light');
            app.addClass('is-dark');
            toggleDarkModeBtn.children('i').removeClass('fa-sun');
            toggleDarkModeBtn.children('i').addClass('fa-moon');
        }
        isDark = !isDark;
        isLight = !isLight;

        // store the current theme in the local storage
        if (isDark) {
            localStorage.setItem('theme', 'is-dark');
            if (localStorage.getItem('backgroundImageToggled') == 'true')
                document.getElementById('app').setAttribute('style', "background-image: url(" + '/api/get_background?theme=dark' + ");");
            else {
                document.getElementById('app').setAttribute('style', "");
            }
        }

        if (isLight) {
            localStorage.setItem('theme', 'is-light');
            if (localStorage.getItem('backgroundImageToggled') == 'true')
                document.getElementById('app').setAttribute('style', "background-image: url(" + '/api/get_background?theme=light' + ");");

            else {
                document.getElementById('app').setAttribute('style', "");
            }
        }
    });

    // if the page is loaded and the local storage has a theme, then set the theme to the local storage theme
    if (localStorage.getItem('theme') === 'is-dark') {
        if (isLight) {
            toggleDarkModeBtn.click();
        }
    } else if (localStorage.getItem('theme') === 'is-light') {
        if (isDark) {
            toggleDarkModeBtn.click();
        }
    }
});

// listen for changeBackgroundImageBtn to be clicked, when it is prompt the user to select an image, then upload the image to the server at /api/uploadBackgroundImage
$(document).ready(function() {
    let changeBackgroundImageBtn = $('#changeBackgroundImageBtn');
    
    changeBackgroundImageBtn.on('click', function(e) {
        let fileInput = document.createElement('input');
        let file;
        fileInput.type = 'file';
        fileInput.accept = 'image/*';
        fileInput.onchange = e => {
            file = e.target.files[0];
            if (file) {
                let theme = localStorage.getItem('theme');
                if (theme === 'is-dark') {
                    theme = 'dark';
                } else if (theme === 'is-light') {
                    theme = 'light';
                }
                let formData = new FormData();
                formData.append('theme', theme);
                formData.append('background-image', file);
                
                $.ajax({
                    url: '/api/upload_background',
                    type: 'POST',
                    data: formData,
                    contentType: false,
                    processData: false,
                    success: function(data) {
                        console.log('Image uploaded successfully');
                        //location.reload();
                        location.reload();
                    },
                    error: function(error) {
                        console.log('Error uploading image: ', error);
                    }
                });
            }
        }
        fileInput.click();
    });
});



$(document).ready(function() {
    if (localStorage.getItem('backgroundImageToggled') == 'true') {

        // check to see if light mode or dark mode is enabled
        if (document.getElementById('app').classList.contains('is-light')) {
            document.getElementById('app').setAttribute('style', "background-image: url(" + '/api/get_background?theme=light' + ");");
        }
        else
        {
            document.getElementById('app').setAttribute('style', "background-image: url(" + '/api/get_background?theme=dark' + ");");
        }
        document.getElementById('toggleBackgroundImageBtn').innerHTML = '<i class="fas fa-toggle-on fa-fw"></i><i class="fas fa-toggle-off fa-fw" style="display: none;"></i>';
        }
    else {
        document.getElementById('app').setAttribute('style', "");
        localStorage.getItem('backgroundImageToggled') == 'false';
        document.getElementById('toggleBackgroundImageBtn').innerHTML = '<i class="fas fa-toggle-off fa-fw"></i><i class="fas fa-toggle-on fa-fw" style="display: none;"></i>';
    }
    // listen for a click on the toggleBackgroundImageBtn
    document.getElementById('toggleBackgroundImageBtn').addEventListener('click', function() {
        // if the backgroundImageToggled is true, then set it to false
        if (localStorage.getItem('backgroundImageToggled') == 'true') {
            localStorage.setItem('backgroundImageToggled', 'false');
            document.getElementById('app').setAttribute('style', "");
            document.getElementById('toggleBackgroundImageBtn').innerHTML = '<i class="fas fa-toggle-off fa-fw"></i><i class="fas fa-toggle-on fa-fw" style="display: none;"></i>';
        } else {
                // check to see if light mode or dark mode is enabled
            if (document.getElementById('app').classList.contains('is-light')) {
                document.getElementById('app').setAttribute('style', "background-image: url(" + '/api/get_background?theme=light' + ");");
            }
            else
            {
                document.getElementById('app').setAttribute('style', "background-image: url(" + '/api/get_background?theme=dark' + ");");
            }
            // if the backgroundImageToggled is false, then set it to true
            localStorage.setItem('backgroundImageToggled', 'true');
            document.getElementById('toggleBackgroundImageBtn').innerHTML = '<i class="fas fa-toggle-on fa-fw"></i><i class="fas fa-toggle-off fa-fw" style="display: none;"></i>';
        }
    });
});

       



// div class="search-bar navbar-item is-inline-block-mobile">
//                       <label for="search" class="search-label"></label>
//                       <input type="text">
//                     </div>

$(document).ready(function() {
    // listen for text to be entered into the search-bar text input field
    // listen for no text to be entered into the search-bar text input field
    $('.search-bar').on('input', function(e) {
        // if the key pressed is delete, then show all the apps
        // get the text from the search-label text input
        let searchLabel = $(this).children('input').val();
        // if the searchLabel is not empty, then search for the label
        if (searchLabel !== '') {
            // search for the label
            // loop through the card-content, get the app-name title, and compare it to the searchLabel, if it does not match, then hide the app
            $('.app-name').each(function() {
                let appName = $(this).text();
                if (appName.toLowerCase().indexOf(searchLabel.toLowerCase()) === -1) {
                    $(this).parent().parent().parent().parent().hide();
                    $(this).attr('data-show', 'hidden');
                } else {
                    $(this).parent().parent().parent().parent().show();
                    $(this).attr('data-show', 'shown');
                }
            });
        } else {
            // if the searchLabel is empty, then show all the apps
            $('.app-name').each(function() {
                $(this).parent().parent().parent().parent().show();
                $(this).attr('data-show', 'shown');
            });
        }
        // check to see if there are no apps in the category, if there are none, then do not show the category
        $('.app-tag-wrapper.column.is-3').each(function() {
            let categoryShown = false;
            $(this).find('.app-name').each(function() {
                if ($(this).attr('data-show') === 'shown') {
                    categoryShown = true;
                }
            });
            if (categoryShown === false) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
});


// if the page is mobile, then set the columns to block
if ($(window).width() < 769) {
    $('.columns').css('display', 'block');
}
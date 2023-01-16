function updateFormFields(appContent) {

    // get app data
    let name = appContent.find('.app-name').text();
    let desc = appContent.find('.app-desc').text();
    let tag = appContent.closest('.app-tag-wrapper').find('.app-tag').text();
    let customUrl = appContent.find('.app-custom-url').val();
    let enableCustomUrl = appContent.find('.app-enable-custom-url').val();
    console.log(enableCustomUrl);
    
    // update form fields
    $('#updateName').val(name);
    $('#updateDesc').val(desc);
    $('#updateTag').val(tag);
    $('#updateCustomUrl').val(customUrl);
    $('#updateEnableCustomUrl').prop('checked', enableCustomUrl.toLowerCase() === 'true' ? true : false);
    $('#updateEnableCustomUrl').trigger('change');

    // update modal title
    $('#updateAppModal').find('.modal-title').text('Edit ' + name + ' App');
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

    // update modal form action
    $('#updateAppModal').find('form').attr('action', `/api/app/${appContent.find('.app-name').text().trim()}/update`);

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

$(document).on('change', '#updateEnableCustomUrl', function(e) {
    console.log('change');
    if ($(this).is(':checked')) {
        $('#updateCustomUrl').prop('disabled', false);
    } else {
        $('#updateCustomUrl').prop('disabled', true);
    }
});
function submitEmailForm(csrfToken) {
    $.ajax({
        url: '/submit_contact_email/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'viewer_email': document.getElementById('id_viewer_email').value
        },
        success: function(data) {
            console.log('POST succeeded.')
            alert('Your request has been submitted.')
        },
        error: function(data) {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}

function submitPrayerReqForm(csrfToken) {
    $.ajax({
        url: '/submit_prayer_request/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'name': document.getElementById('id_name').value,
            'comment': document.getElementById('id_comment').value
        },
        success: function(data) {
            console.log('POST succeeded.')
            alert('Your request has been submitted.')
        },
        error: function(data) {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}

function submitContactForm(csrfToken) {
    $.ajax({
        url: '/submit_contact_form/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'fname': document.getElementById('id_fname').value,
            'lname': document.getElementById('id_lname').value,
            'email': document.getElementById('id_email').value,
            'comment': document.getElementById('id_comment').value
        },
        success: function(data) {
            console.log('POST succeeded.')
            alert('Your request has been submitted.')
        },
        error: function(data) {
            console.log('POST failed.')
            alert('Your request could not be submitted.')
        }
    })
}
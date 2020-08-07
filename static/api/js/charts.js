var modal = document.getElementById('modal');
var open_modal_btn = document.getElementById('open-modal');
var close_modal_el = document.getElementById('close-modal');
var collapse = document.getElementById('collapse-menu');

function changeViewsEndDate() {
    window.location.replace('/api/views/charts/' + document.getElementById('enddate').value)
}

function changeVisitorsEndDate() {
    window.location.replace('/api/visitors/charts/' + document.getElementById('enddate').value)
}

function showExportDialog() {
    collapse.click();
    modal.style.display = 'block';
    
    var export_time_period = document.getElementById('export-views').value;
    var end_date = document.getElementById('end-date').value;
    document.getElementById('id_time_period').value = export_time_period;
    document.getElementById('id_end_date').value = end_date;
}

function hideExportDialog() {
    collapse.click();
    modal.style.display = 'none';
}

function deleteViews(csrfToken, enddate) {
    var sel = document.getElementById('delete-views');
    var time_period = sel.options[sel.selectedIndex].value;

    // Make post request here.
    $.ajax({
        url: '/api/views/data/delete/' + time_period + '/' + enddate,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(data) {
            console.log('POST succeeded.')
            alert('Records deleted!')
            window.location.reload(true)
        },
        error: function(data) {
            console.log('POST failed.')
            console.log(data)
            alert('Deletetion failed!')
        }
    })
}

function deleteVisitors(csrfToken, enddate) {
    var sel = document.getElementById('delete-visitors');
    var time_period = sel.options[sel.selectedIndex].value;

    // Make post request here.
    $.ajax({
        url: '/api/visitors/data/delete/' + time_period + '/' + enddate,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken
        },
        success: function(data) {
            console.log('POST succeeded.')
            window.location.reload(true)
            alert('Records deleted!')
        },
        error: function(data) {
            console.log('POST failed.')
            console.log(data)
            alert('Deletion failed!')
        }
    })
}
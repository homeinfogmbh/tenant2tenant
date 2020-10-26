/*
    Tenant-to-tenant java script library.

    (C) 2018-2020 HOMEINFO - Digitale Informationssysteme GmbH

    Maintainer: Richard Neumann <r period neumann at homeinfo dot de>
*/
'use strict';

import { request } from 'https://javascript.homeinfo.de/his/his.js';


/*
    Returns an error message.
*/
function error (string) {
    return '<font size="4" color="#FF0000">' + string + '</font>';
}


/*
    Returns the environment arguments.
*/
function getEnviron () {
	if (localStorage.getItem('customer') === '')
		return {};

    return {
        'customer': localStorage.getItem("customerid"),
    };
}


/*
    Creates a list element from the respective record.
*/
function listElement (record, i) {
	const parser = new DOMParser();
	const messageDOM = parser.parseFromString(record.message, 'text/html');
	const oneweek = new Date(record.created);
	oneweek.setDate(oneweek.getDate() + 7);
	const  enddatestring = oneweek.getFullYear() + "-" + ("0"+(oneweek.getMonth()+1)).slice(-2) + '-' + ("0"+oneweek.getDate()).slice(-2);
	const row = document.createElement('tr');
	row.classList.add(record.released ? 'success' :'danger');
	const colId = document.createElement('td');
	colId.textContent = '' + (i + 1);
	row.appendChild(colId);
	const colCreated = document.createElement('td');
	colCreated.textContent = record.created.split('T').join(' ');
    row.appendChild(colCreated);

    return '<tr class="' + (record.released ?'success' :'danger') + '">' +
        '<td>' + (i+1) + "</td>" +
        '<td>' + record.created.split('T').join(' ') + '</td>' +
        '<td>' + record.address.street + ' ' + record.address.houseNumber + '</td>' +
        '<td><div title="Text bearbeiten" id="textvalue" contenteditable="true" style="background-color:#fff">' + messageDOM.body.textContent + ' </div><i class="fa fa-save btn_save_text pointer" style="font-size:20px; color:#a2a2a2; padding-top:5px" title="Text speichern" data-id="' + record.id + '"></i></td>' +
        '<td width="130px"><input type="text" class="form-control datetime dateFrom" data-id="' + record.id + '" placeholder="Anzeigen von" value="' + (record.startDate != null ?record.startDate :record.created.substr(0, 10)) + '"></td>' +
        '<td width="130px"><input type="text" class="form-control datetime dateUntil" data-id="' + record.id + '" placeholder="Anzeigen bis" value="' + (record.endDate != null ?record.endDate :enddatestring) + '"></td>' +
        '<td style="vertical-align: middle"><input type="checkbox" class="toggle" data-id="' + record.id + '" title="' + (record.released ?'Eintrag sperren" checked' :'Eintrag freigeben"') + '></td>' +
        '<td style="vertical-align: middle"><i class="fa fa-trash-o confirmdelete pointer" style="font-size:20px; color:#a2a2a2; padding-left:5px" title="Eintrag löschen"><br>' +
        '<font class="confirm deleteconfirm" style="display:none; float:right;"> Sicher?<br><a href="#" class="delete no_drag deleteconfirm" data-id="' + record.id + '">ja</a> / <a href="#" class="confirmdelete no_drag deleteconfirm" >nein</a></font></td>' +
        '</tr>';
}


/*
    Toggles the entry with the respective ID
    between released and not released.
*/
function toggle (ident, startDate, endDate) {
	startDate = startDate === '' || startDate == null ?null :startDate;
	endDate = endDate === '' || endDate == null ?null :endDate;
	const promises = [];
	promises.push(updateStartDate(ident, startDate));
	promises.push(updateEndDate(ident, endDate));
	promises.push(request.put('https://backend.homeinfo.de/tenant2tenant/message/' + ident, null, getEnviron()));
	Promise.all(promises).then(init);
}


/*
    Deletes the entry with the respective ID.
*/
function delete_ (ident) {
    request.delete('https://backend.homeinfo.de/tenant2tenant/message/' + ident, getEnviron()).then(init);
}


/*
    Lists the entries for the respective customer.
*/
function list (entries) {
	entries.sort(function(b, a) {
		return compareStrings(a.created, b.created);
	});
    let elements = 'Es wurden keine Nachrichten geschrieben.';
    for (let i = 0; i < entries.length; i++)
        elements += listElement(entries[i], i);
	$('#messages').html(elements);
	$('.btn_save_text').click(function() {
		$('#pageloader').show();
		updateMessageText($(this).data('id'), $(this).parent().find('#textvalue').html()).then(function(){$('#pageloader').hide();});
	});
	$('.toggle').click(function() {
		$('#pageloader').show();
		toggle($(this).data('id'), $(this).parent().parent().find('.dateFrom').val(), $(this).parent().parent().find('.dateUntil').val());
	});
	$('.confirmdelete').click(function(e) {
		if ($(this).text() === 'nein') {
			$(this).parent().hide('fast');
		} else {
			if ($(this).parent().find('.confirm').is(":visible"))
				$(this).parent().find('.confirm').hide('fast')
			else
				$(this).parent().find('.confirm').show('fast');
		}
		e.preventDefault();
	});
	$('.delete').click(function() {
		$('#pageloader').show();
		delete_($(this).data('id'));
	});
	$('.dateFrom').datepicker({
		constrainInput: true,
		monthNames: ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'],
		monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun', 'Jul','Aug','Sep','Okt','Nov','Dez'],
		dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
		dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dateFormat : 'yy-mm-dd',
		onClose: function (date) {
			updateStartDate($(this).data('id'), date);
		}
	}, $.datepicker.regional['de']);
	$('.dateUntil').datepicker({
		constrainInput: true,
		monthNames: ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'],
		monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun', 'Jul','Aug','Sep','Okt','Nov','Dez'],
		dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
		dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
		dateFormat : 'yy-mm-dd',
		firstDay: 1,
		onClose: function (date) {
			updateEndDate($(this).data('id'), date);
		}
    }, $.datepicker.regional['de']);
    $('#pageloader').hide();
}


/*
    Updates the text of the message.
*/
function updateMessageText (id, messageText) {
    const json = {message: messageText};
    return request.patch('https://backend.homeinfo.de/tenant2tenant/message/' + id, json, getEnviron());
}


function updateStartDate (id, date) {
    const json = {startDate: date};
    return request.patch('https://backend.homeinfo.de/tenant2tenant/message/' + id, json, getEnviron());
}


/*
    Updates the end date.
*/
function updateEndDate (id, date) {
    const json = {endDate: date};
    return request.patch('https://backend.homeinfo.de/tenant2tenant/message/' + id, json, getEnviron());
}


/*
    Lists the emails from the API in the input field.
*/
function listEmails (emails) {
    const emailsInput = $('#emails');
    const emailAddresses = [];

    for (const email of emails) {
        emailAddresses.push(email.email);
    }

    emailsInput.val(emailAddresses.join(', '));
}


/*
    Set the autoRelease settings from the API.
*/
function setSettings (settings) {
	if (settings.hasOwnProperty('releaseSec')) {
		$('#time').val(settings.releaseSec/86400); // one Day
		if (settings.autoRelease)
			$('#releasetrue').click();
	}
}


/*
    Loads the configured email addresses from the API.
*/
function loadEmails () {
    return request.get('https://backend.homeinfo.de/tenant2tenant/email', getEnviron()).then(listEmails);
}


/*
    Returns a list of emails from the email input field.
*/
function getEmails () {
    const emailsInput = $('#emails');
    const emailsString = emailsInput.val();
    const emailAddresses = emailsString.split(',');
    const emails = [];

    for (const emailAddress of emailAddresses) {
        const trimmedEmailAddress = emailAddress.trim();

        if (trimmedEmailAddress != '') {
            emails.push({email: trimmedEmailAddress, 'html':true};);
        }
    }

    return emails;
}


function saveSettings () {
	$('#pageloader').show();
	const promises = [];
	promises.push(saveEmails());
	promises.push(saveAutoRelease());
	Promise.all(promises).then(
        function (data) {
            $('#message').html('');
            $('#pageloader').hide();
        },
		function (error) {
			console.log(error);
		}
	);
}


/*
    Saves the set emails.
*/
function saveEmails () {
    return request.post('https://backend.homeinfo.de/tenant2tenant/email', getEmails(), getEnviron()).then(
        loadEmails,
        function (error) {
            console.log('Error: ' + JSON.stringify(error));
            $('#pageloader').hide();
            if (error.status == 403) {
                $('#message').html(error('Sie haben keine Berechtingung, Email Adressen zu ändern.'));
            } else {
                $('#message').html(error('Email Adressen konnten nicht gespeichert werden.'));
            }
        }
    );
}


/*
    Loads the configuration.
*/
function loadAutoRelease () {
    return request.get('https://backend.homeinfo.de/tenant2tenant/configuration', getEnviron()).then(setSettings);
}


/*
    Saves the autorelease settings.
*/
function saveAutoRelease () {
	const json = {
	    'autoRelease': $('input[name=autorelease]:checked').val() === 'true',
	    'releaseSec': parseInt($('#time').val()) * 86400
    };
    return request.post('https://backend.homeinfo.de/tenant2tenant/configuration', json, getEnviron());
}


/*
    Initialization function.
*/
export function init () {
    $('#pageloader').show();
	if (localStorage.getItem("user") && (JSON.parse(localStorage.getItem("user")).admin || JSON.parse(localStorage.getItem("user")).root)) {
		$('#emails').removeAttr('disabled');
		$('.btn_save').removeAttr('disabled');
	} else {
		$('#emails').attr('disabled', 'disabled');
		$('.btn_save').attr('disabled', 'disabled');
		$('#emails').attr('title', 'Das Ändern der E-Mails ist nicht erlaubt. Bitte kontaktieren Sie uns, damit wir dieses Modul für Sie freischalten können.');
	}
    $('.btn_save').click(saveSettings);
    const promiseListMessages = request.get('https://backend.homeinfo.de/tenant2tenant/message', getEnviron()).then(list);
    return Promise.all([loadEmails(), promiseListMessages, loadAutoRelease()]).then(
        function () {
            $('#pageloader').hide();
        }
    );
}

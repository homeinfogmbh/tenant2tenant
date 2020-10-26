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
    var args = getEnviron();
	startDate = startDate === '' || startDate == null ?null :startDate;
	endDate = endDate === '' || endDate == null ?null :endDate;
	var promises = [];
	promises.push(updateStartDate(ident, startDate));
	promises.push(updateEndDate(ident, endDate));
	promises.push(request.put('https://backend.homeinfo.de/tenant2tenant/message/' + ident, args));
	Promise.all(promises).then(init);
}


/*
    Deletes the entry with the respective ID.
*/
function delete (ident) {
    var args = getEnviron();
    request.delete('https://backend.homeinfo.de/tenant2tenant/message/' + ident, args).then(init);
}


/*
    Lists the entries for the respective customer.
*/
function list (entries) {
	entries.sort(function(b, a) {
		return compareStrings(a.created, b.created);
	});
    var elements = 'Es wurden keine Nachrichten geschrieben.';
    for (var i = 0; i < entries.length; i++)
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
		delete($(this).data('id'));
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
    var args = getEnviron();
    var json = {message: messageText};
    return request.patch('https://backend.homeinfo.de/tenant2tenant/message/' + id, args, json);
}


function updateStartDate (id, date) {
    var args = getEnviron();
    var json = {startDate: date};
    return request.patch('https://backend.homeinfo.de/tenant2tenant/message/' + id, args, json);
}


/*
    Updates the end date.
*/
function updateEndDate (id, date) {
    var args = getEnviron();
    var json = {endDate: date};
    return request.patch('https://backend.homeinfo.de/tenant2tenant/message/' + id, args, json);
}


/*
    Lists the emails from the API in the input field.
*/
function listEmails (emails) {
    var emailsInput = $('#emails');
    var emailAddresses = [];

    for (var email of emails) {
        emailAddresses.push(email.email);
    }

    var emailsString = emailAddresses.join(', ');
    emailsInput.val(emailsString);
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
    var args = getEnviron();
    return request.get('https://backend.homeinfo.de/tenant2tenant/email', args).then(listEmails);
}


/*
    Returns a list of emails from the email input field.
*/
function getEmails () {
    var emailsInput = $('#emails');
    var emailsString = emailsInput.val();
    var emailAddresses = emailsString.split(',');
    var emails = [];

    for (var emailAddress of emailAddresses) {
        var trimmedEmailAddress = emailAddress.trim();

        if (trimmedEmailAddress != '') {
            var email = {email: trimmedEmailAddress, 'html':true};
            emails.push(email);
        }
    }
    return emails;
}


function saveSettings () {
	$('#pageloader').show();
	var promises = [];
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
    var args = getEnviron();
    var emails = getEmails();
    var promise = request.post('https://backend.homeinfo.de/tenant2tenant/email', args, emails);
    return promise.then(loadEmails).then(
        function () { },
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
    var args = getEnviron();
	var autorelease = $('input[name=autorelease]:checked').val() === 'true';
	var relaseSec = parseInt($('#time').val())*86400;
    return request.post('https://backend.homeinfo.de/tenant2tenant/configuration', args, {"autoRelease":autorelease, "releaseSec":relaseSec});
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
    var args = getEnviron();
    var promiseListMessages = request.get('https://backend.homeinfo.de/tenant2tenant/message', args).then(list);
    var promiseLoadEmails = loadEmails();
	var promiseLoadAutoRelease = loadAutoRelease();
    return Promise.all([promiseLoadEmails, promiseListMessages, promiseLoadAutoRelease]).then(
        function () {
            $('#pageloader').hide();
        }
    );
}

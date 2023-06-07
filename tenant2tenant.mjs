/*
  Tenant-to-tenant java script module.

  (C) 2015-2021 HOMEINFO - Digitale Informationssysteme GmbH

  This library is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this library.  If not, see <http://www.gnu.org/licenses/>.

  Maintainer: Richard Neumann <r dot neumann at homeinfo period de>
*/
'use strict';


import { request, getUser } from 'https://javascript.homeinfo.de/his/his.mjs';
import { enumerate } from 'https://javascript.homeinfo.de/lib.mjs';


const BASE_URL = 'https://backend.homeinfo.de/tenant2tenant';
const COMCAT_URL = 'https://backend.homeinfo.de/comcat/tenant2tenant';
const CONFIG_URL = BASE_URL + '/configuration';
const MESSAGE_URL = BASE_URL + '/message';
const EMAIL_URL = BASE_URL + '/email';
const DATE_PICKER_CONFIG = {
    constrainInput: true,
    monthNames: ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember'],
    monthNamesShort: ['Jan','Feb','Mär','Apr','Mai','Jun', 'Jul','Aug','Sep','Okt','Nov','Dez'],
    dayNames: ['Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag'],
    dayNamesShort: ['So','Mo','Di','Mi','Do','Fr','Sa'],
    dayNamesMin: ['So','Mo','Di','Mi','Do','Fr','Sa'],
    dateFormat : 'yy-mm-dd'
};


/*
    Returns an error message.
*/
function error (string) {
    const font = document.createElement('font');
    font.setAttribute('size', '4');
    font.setAttribute('color', '#FF0000');
    font.innerHTML = string;
    return font.outerHTML;
}


/*
    Returns the environment arguments.
*/
function getEnviron () {
	if (localStorage.getItem('customer') === '')
		return {};

    return {'customer': localStorage.getItem("customerid")};
}


/*
    Creates a list element from the respective record.
*/
function listElement (record, i) {
	const parser = new DOMParser();
	const messageDOM = parser.parseFromString(record.message, 'text/html');
	const oneweek = new Date(record.created);
	oneweek.setDate(oneweek.getDate() + 7);
	const month = ('0' + (oneweek.getMonth() + 1)).slice(-2);
	const day = ('0' + oneweek.getDate()).slice(-2);
	const enddatestring = oneweek.getFullYear() + '-' + month + '-' + day;

	const row = document.createElement('tr');
	row.classList.add(record.released ? 'success' : 'danger');

	const colId = document.createElement('td');
	colId.textContent = '' + (i + 1);
	row.appendChild(colId);

	const colCreated = document.createElement('td');
	colCreated.textContent = record.created.split('T').join(' ');
    row.appendChild(colCreated);

    const colAddress = document.createElement('td');
    colAddress.textContent = record.address.street + ' ' + record.address.houseNumber + (record.hasOwnProperty('user') ?' (Account: ' + record.user + ')' :'');
    row.appendChild(colAddress);

    const colMessage = document.createElement('td');
    const divText = document.createElement('div');
    divText.setAttribute('id', 'textValue');
    divText.setAttribute('title', 'Text bearbeiten');
    divText.setAttribute('contenteditable', 'true');
    divText.style.backgroundColor = '#fff';
    divText.innerHTML = messageDOM.body.textContent;
    colMessage.appendChild(divText);
    const btnSave = document.createElement('i');
    btnSave.classList.add('fa');
    btnSave.classList.add('fa-save');
    btnSave.classList.add('btn_save_text');
    btnSave.classList.add('pointer');
    btnSave.setAttribute('title', 'Text speichern');
    btnSave.setAttribute('data-id', '' + record.id);
    btnSave.style.color = '#a2a2a2';
    btnSave.style.fontSize = '20px';
    btnSave.style.paddingTop = '5px';
    colMessage.appendChild(btnSave);
    row.appendChild(colMessage);

    const colFrom = document.createElement('td');
    colFrom.setAttribute('width', '130px');
    const from = record.startDate != null ? record.startDate : record.created.substr(0, 10);
    const inputFrom = document.createElement('input');
    inputFrom.classList.add('form-control');
    inputFrom.classList.add('datetime');
    inputFrom.classList.add('dateFrom');
    inputFrom.setAttribute('type', 'text');
    inputFrom.setAttribute('data-id', '' + record.id);
    inputFrom.setAttribute('placeholder', 'Anzeigen von');
    inputFrom.setAttribute('value', from);
    colFrom.appendChild(inputFrom);
    row.appendChild(colFrom);

    const colUntil = document.createElement('td');
    colUntil.setAttribute('width', '130px');
    const until = record.endDate != null ? record.endDate : enddatestring;
    const inputUntil = document.createElement('input');
    inputUntil.classList.add('form-control');
    inputUntil.classList.add('datetime');
    inputUntil.classList.add('dateUntil');
    inputUntil.setAttribute('type', 'text');
    inputUntil.setAttribute('data-id', '' + record.id);
    inputUntil.setAttribute('placeholder', 'Anzeigen bis');
    inputUntil.setAttribute('value', until);
    colUntil.appendChild(inputUntil);
    row.appendChild(colUntil);

    const colReleased = document.createElement('td');
    colReleased.style.verticalAlign = 'middle';
    const title = record.released ? 'Eintrag sperren' : 'Eintrag freigeben';
    const inputReleased = document.createElement('input');
    inputReleased.checked = record.released;
    inputReleased.classList.add('toggle');
    inputReleased.setAttribute('type', 'checkbox');
    inputReleased.setAttribute('data-id', '' + record.id);
    inputReleased.setAttribute('title', title);
    colReleased.appendChild(inputReleased);
    row.appendChild(colReleased);

    const colDelete = document.createElement('td');
    colDelete.style.verticalAlign = 'middle';
    const iDelete = document.createElement('i');
    iDelete.classList.add('fa');
    iDelete.classList.add('fa-trash-o');
    iDelete.classList.add('confirmdelete');
    iDelete.classList.add('pointer');
    iDelete.setAttribute('title', 'Eintrag löschen');
    iDelete.style.fontSize = '20px';
    iDelete.style.color = '#a2a2a2';
    iDelete.style.paddingLeft = '5px';
    colDelete.appendChild(iDelete);
    colDelete.appendChild(document.createElement('br'));

    const fontDelete = document.createElement('font');
    fontDelete.classList.add('confirm');
    fontDelete.classList.add('deleteconfirm');
    fontDelete.style.display = 'none';
    fontDelete.style.float = 'right';
    fontDelete.appendChild(document.createTextNode('Sicher?'))
    fontDelete.appendChild(document.createElement('br'));

    const aConfirmDelete = document.createElement('a');
    aConfirmDelete.classList.add('delete');
    aConfirmDelete.classList.add('no_drag');
    aConfirmDelete.classList.add('deleteconfirm');
    aConfirmDelete.setAttribute('href', '#');
    aConfirmDelete.setAttribute('data-id', '' + record.id);
    aConfirmDelete.textContent = 'ja';
    fontDelete.appendChild(aConfirmDelete);
    fontDelete.appendChild(document.createTextNode(' / '));

    const aCancelDelete = document.createElement('a')
    aCancelDelete.classList.add('confirmdelete');
    aCancelDelete.classList.add('no_drag');
    aCancelDelete.classList.add('deleteconfirm');
    aCancelDelete.setAttribute('href', '#');
    aCancelDelete.setAttribute('data-id', '' + record.id);
    aCancelDelete.textContent = 'nein';
    fontDelete.appendChild(aCancelDelete);
    colDelete.appendChild(fontDelete);
    row.appendChild(colDelete);
    return row;
}


/*
    Toggles the entry with the respective ID
    between released and not released.
*/
function toggle (ident, startDate, endDate) {
	const oneweek = new Date();
	oneweek.setDate(oneweek.getDate() + 7);
	const month = ('0' + (oneweek.getMonth() + 1)).slice(-2);
	const day = ('0' + oneweek.getDate()).slice(-2);
	const enddatestring = oneweek.getFullYear() + '-' + month + '-' + day;


	startDate = startDate === '' || startDate == null ?null :startDate;
	endDate = endDate === '' || endDate == null ?enddatestring :endDate;
	const promises = [];
	promises.push(updateStartDate(ident, startDate));
	promises.push(updateEndDate(ident, endDate));
	promises.push(request.put(MESSAGE_URL + '/' + ident, null, getEnviron()));
	Promise.all(promises).then(init);
}


/*
    Deletes the entry with the respective ID.
*/
function delete_ (ident) {
    request.delete(MESSAGE_URL + '/' + ident, getEnviron()).then(init);
}


/*
    Lists the entries for the respective customer.
*/
function list (response) {
    const entries = response[0].json;
	
	if (response.length > 1) {
		for (var mappingEntry of entries) {
			for (var mapping of response[1].json) {
				if (mappingEntry.id === mapping.tenantMessage) {
					mappingEntry.user = mapping.user;
					break;
				}
			}
		}
	}

	entries.sort(function(b, a) {
		return compareStrings(a.created, b.created);
	});

    const rows = [];
    let index, entry;
	$('#messages').html("");

    for (const [index, entry] of enumerate(entries))
        rows.push(listElement(entry, index));

    if (rows.length == 0)
        rows.push(document.createTextNode('Es wurden keine Nachrichten geschrieben.'));
	
    for (const row of rows)
	    $('#messages').append(row);

	$('.btn_save_text').click(function() {
		$('#pageloader').show();
		updateMessageText($(this).data('id'), $(this).parent().find('#textValue').html()).then(function(){$('#pageloader').hide();});
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

	const configFrom = Object.assign({}, DATE_PICKER_CONFIG);
	configFrom.onClose = function (date) {
		updateStartDate($(this).data('id'), date);
	};
	$('.dateFrom').datepicker(configFrom, $.datepicker.regional['de']);

	const configUntil = Object.assign({firstDay: 1}, DATE_PICKER_CONFIG);
	configUntil.onClose = function (date) {
		updateEndDate($(this).data('id'), date);
	};
	$('.dateUntil').datepicker(configUntil, $.datepicker.regional['de']);

    $('#pageloader').hide();
}


/*
    Updates the text of the message.
*/
function updateMessageText (id, messageText) {
    return request.patch(MESSAGE_URL + '/' + id, {message: messageText}, getEnviron());
}


/*
    Updates the start date.
*/
function updateStartDate (id, date) {
    return request.patch(MESSAGE_URL + '/' + id, {startDate: date}, getEnviron());
}


/*
    Updates the end date.
*/
function updateEndDate (id, date) {
    return request.patch(MESSAGE_URL + '/' + id, {endDate: date}, getEnviron());
}


/*
    Lists the emails from the API in the input field.
*/
function listEmails (response) {
    const emailsInput = $('#emails');
    const emailAddresses = [];

    for (const email of response.json)
        emailAddresses.push(email.email);

    emailsInput.val(emailAddresses.join(', '));
}


/*
    Set the autoRelease settings from the API.
*/
function setSettings (settings) {
	if (settings.hasOwnProperty('json') && settings.json.hasOwnProperty('releaseSec')) {
		$('#time').val(settings.json.releaseSec/86400); // one Day
		if (settings.json.autoRelease)
			$('#releasetrue').click();
	}
}


/*
    Loads the configured email addresses from the API.
*/
function loadEmails () {
    return request.get(EMAIL_URL, getEnviron()).then(listEmails);
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

        if (trimmedEmailAddress != '')
            emails.push({email: trimmedEmailAddress, 'html':true});
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
    return request.post(EMAIL_URL, getEmails(), getEnviron()).then(
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
    return request.get(CONFIG_URL, getEnviron()).then(setSettings);
}


/*
    Saves the autorelease settings.
*/
function saveAutoRelease () {
	const json = {
	    'autoRelease': $('input[name=autorelease]:checked').val() === 'true',
	    'releaseSec': parseInt($('#time').val()) * 86400
    };
    return request.post(CONFIG_URL, json, getEnviron());
}


/*
    Initialization function.
*/
export function init () {
    $('#pageloader').show();
    const user = getUser('user');

	if (user != null && (user.admin || user.root)) {
		$('#emails').removeAttr('disabled');
		$('.btn_save').removeAttr('disabled');
	} else {
		$('#emails').attr('disabled', 'disabled');
		$('.btn_save').attr('disabled', 'disabled');
		$('#emails').attr('title', 'Das Ändern der E-Mails ist nicht erlaubt. Bitte kontaktieren Sie uns, damit wir dieses Modul für Sie freischalten können.');
	}

    $('.btn_save').click(saveSettings);
    const promiseListMessages = request.get(MESSAGE_URL, getEnviron());
	//const promiseMessageUser = request.get(COMCAT_URL, getEnviron());
	const messagemapping = Promise.all([promiseListMessages/*, promiseMessageUser*/]).then(list)
    return Promise.all([loadEmails(), messagemapping, loadAutoRelease()]).then(
        function () {
            $('#pageloader').hide();
        }
    );
}

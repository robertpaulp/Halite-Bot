var url = "api/web/";
// Attempts to store the username/password combo given
// Returns false if the username is already taken
// If async returns null
function storeUserDatabase(email, username, password, async) {
    var result = $.ajax({
        url: url+"user",
        async: async,
        method: "POST",
        data: {email: email, username: username, password: password}
    });

    if(async == true) {
        return null;
    }

    console.log(result)
    return result.responseJSON;
}

function storeUserSession(username, password, async) {
    $.ajax({
        url: url+"session",
        async: async,
        method: "POST",
        data: {username: username, password: password}
    });
}

// Uploads source code for users's bot
// When given the html ID of a form with the userID as a value and the file as another value
function storeBotFile(formID) {
    if(!$("#"+formID).find("input[name='userID']").length || $("#"+formID).find("input[name='userID']").val().localeCompare("") == 0) {
        console.log("Form not setup correctly. Does not include userID");
        throw 1;
    }
    var formData = new FormData($("#"+formID)[0]);
    var result = $.ajax({
        url: url+"botFile",
        async: false,
        method: "POST",
        data: formData,
        processData: false,
        contentType: false,
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            return myXhr;
        },
        success: function(result) {
            console.log(result);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            console.log(xhr.responseText)
        }
    })
    console.log(result);
    return result.responseJSON;
}

function getSession() {
    var result =  $.ajax({
        url: url+"session",
        async: false,
        method: 'GET'
    });
    return result.responseJSON;
}

function getUser(userID, username, password) {
    var result = $.ajax({
        url: url+"user",
        async: false,
        method: "GET",
        data: {userID: userID, username: username, password: password}
    });
    console.log(result)
    return result.responseJSON;
}

function getActiveUsers(limit, page) {
    var result = $.ajax({
        url: url+"user",
        async: false,
        method: "GET",
        data: {fields: ["isRunning"], values: ["1"], limit: limit, page: page}
    });
    console.log(result)
    console.log(result.responseJSON)
    return result.responseJSON;
}

function getLatestGamesForUser(userID, limit, startingID) {
    console.log(startingID)
    var result = $.ajax({
        url: url+"game",
        async: false,
        method: "GET",
        data: {userID: userID, limit: limit, startingID: startingID}
    });
    console.log(startingID)
    return result.responseJSON;
}

function destroySession(async) {
    $.ajax({
        url: url+"session",
        async: async,
        method: "DELETE"
    });
}

function verifyUser(userID, verificationCode) {
    return $.ajax({
        url: url+"user",
        async: false,
        method: "POST",
        data: {userID: userID, verificationCode: verificationCode}
    }).responseJSON;
}

function getNumActiveUsers() {
    return $.ajax({
        url: url+"stats",
        async: false,
        method: "GET",
        data: {numActive: 1}
    }).responseJSON;
}

function getExtraStats(userID) {
    return $.ajax({
        url: url+"extraStats",
        async: false,
        method: "GET",
        data: {userID: userID}
    }).responseJSON;
}

function getForumSignInURL(payload, signature, userID, email, username) {
    return $.ajax({
        url: url+"forums",
        async: false,
        method: "GET",
        data: {
            payload: payload,
            signature: signature,
            userID: userID,
            email: email,
            username: username
        }
    }).responseJSON;
}

function getWorkers() {
    return $.ajax({
        url: url+"worker",
        async: false,
        method: "GET",
        data: {}
    }).responseJSON;
}

function getLatestAnnouncement(userID) {
    return $.ajax({
        url: url+"announcement",
        async: false,
        method: "GET",
        data: {userID: userID}
    }).responseJSON;
}

function closedAnnouncement(announcementID) {
    var response = $.ajax({
        url: url+"announcement",
        async: false,
        method: "POST",
        data: {announcementID: announcementID}
    });
    console.log(response)
    return response.responseJSON;
}

function getRandomGameName() {
    var response = $.ajax({
        url: url+"game",
        async: false,
        method: "GET",
        data: {random: true}
    });
    console.log(response)
    return response.responseJSON;
}

function getHistories(userID) {
    var response = $.ajax({
        url: url+"history",
        async: false,
        method: "GET",
        data: {userID: userID}
    });
    console.log(response)
    return response.responseJSON;
}

function getThroughput() {
    return $.ajax({
        url: url+"stats",
        async: false,
        method: "GET",
        data: {throughput: 1}
    }).responseJSON;
}

function getNumSubmissions() {
    return $.ajax({
        url: url+"stats",
        async: false,
        method: "GET",
        data: {numSubmissions: 1}
    }).responseJSON;
}

function getFilteredUsers(filters, orderBy, limit, page) {
    var fields = Object.keys(filters);
    var values = fields.map(function(a) {return filters[a];});
    var result = $.ajax({
        url: url+"user",
        async: false,
        method: "GET",
        data: {fields: fields, values: values, orderBy: orderBy, limit: limit, page: page}
    });
	console.log(result)

    return result.responseJSON;
}

function getNotifications() {
    return $.ajax({
        url: url+"notification",
        async: false,
        method: "GET"
    }).responseJSON;
}

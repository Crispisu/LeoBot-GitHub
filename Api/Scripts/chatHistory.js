function sendMessageEvent(event) 
{
    if (event.keyCode === 13) {
        sendMessage();
    }
}

function sendMessage()
{
    var chatInput = $('#userMessage');
    
    var chatBox = $('#chatHistoryContainer');

    if (chatBox.html().trim() === "")
    {
        chatBox.html("You: " + chatInput.val());
    }
    else
    {
        chatBox.html(chatBox.html() + "<br>You: " + chatInput.val());
        chatBox.animate({ scrollTop: chatBox.prop("scrollHeight")}, 10);

    }

     // Send the data using post
    var url = "http://192.168.1.200:56001/leobot/chat";
    var requestdata = '{"message": "' + chatInput.val() + '"}';
    console.log(requestdata);

    $.ajax
    ({
        type: "POST",
        contentType: 'application/json',
        //the url where you want to sent the userName and password to
        url: url,
        dataType: 'json',
        async: false,
        //json object to sent to the authentication url
        data: requestdata,
        success: function (data) {
            chatBox.html(chatBox.html() + "<br>LeoBot: " + data.response);
            chatBox.animate({ scrollTop: chatBox.prop("scrollHeight")}, 10);
        },
        error: function(error) {console.log(error)}
    })

    chatInput.val("");
}

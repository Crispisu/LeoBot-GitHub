var cards;
var step = 1;
var patientId = null;

selectedCards = {
    Draw_1_S_1 : '',
    Draw_1_S_2 : '',
    Draw_1_A_1 : '',
    Draw_1_A_2 : '',
    Draw_2_S_1 : '',
    Draw_2_S_2 : '',
    Draw_2_A_1 : '',
    Draw_2_A_2 : '',
    Draw_3_S_1 : '',
    Draw_3_S_2 : '',
    Draw_3_A_1 : '',
    Draw_3_A_2 : '',
    Draw_4_S_1 : '',
    Draw_4_S_2 : '',
    Draw_4_A_1 : '',
    Draw_4_A_2 : '',
    Draw_5_S_1 : '',
    Draw_5_S_2 : '',
    Draw_5_A_1 : '',
    Draw_5_A_2 : '',
    Draw_6_S_1 : '',
    Draw_6_S_2 : '',
    Draw_6_A_1 : '',
    Draw_6_A_2 : ''
}

function returningPatientEvent(event) 
{
    if (event.keyCode === 13) {
        returningPatient();
    }
}

function returningPatient()
{
    patientId = $("#returning").val();
    var url = `/checkpatientsessions/${patientId}`;

    $.ajax
    ({
        type: "GET",
        contentType: 'application/json',
        url: url,
        dataType: 'json',
        async: false,
        success: function (data) {
            canContinueTest = data.response;
            if (canContinueTest == true)
            {
                switchToTestView();
                getCards();
            }
            else
            {
                $("#welcomeSection").hide();
                $("#gameContainer").hide();
                $("#testFinished").show();
                
            }
        },
        error: function(error) {console.log(error)}
    });
}

function getCards()
{
    var url = "/getseries";

    $.ajax
    ({
        type: "GET",
        contentType: 'application/json',
        url: url,
        dataType: 'json',
        async: false,
        success: function (data) {
            cards = data;
            drawCards(cards.set1);
        },
        error: function(error) {console.log(error)}
    });
}

function drawCards(set)
{
    for (let i = 0; i < set.length; i++)
    {
        $(`#card${i}`).prepend(`<img id="${set[i]}" src="Content/Cards/${set[i]}.png" onclick="saveSelection('${set[i]}')" />`)
    }
    alert("Pick 2 likeable");
}

function emptyCardHolders()
{
    for (let i = 0; i < 8; i++)
    {
        $(`#card${i}`).empty();
    }
}

function saveSelection(id)
{
    $(`#${id}`).remove();
    switch (step) {
        case 1:
            selectedCards.Draw_1_S_1 = id;
            break;
        case 2:
            selectedCards.Draw_1_S_2 = id;
            alert("Pick 2 unlikeable");
            break;
        case 3:
            selectedCards.Draw_1_A_1 = id;
            break;
        case 4:
            selectedCards.Draw_1_A_2 = id;
            emptyCardHolders();
            drawCards(cards.set2);
            break;
        case 5:
            selectedCards.Draw_2_S_1 = id;
            break;
        case 6:
            selectedCards.Draw_2_S_2 = id;
            alert("Pick 2 unlikeable");
            break;
        case 7:
            selectedCards.Draw_2_A_1 = id;
            break;
        case 8:
            selectedCards.Draw_2_A_2 = id;
            emptyCardHolders();
            drawCards(cards.set3);
            break;
        case 9:
            selectedCards.Draw_3_S_1 = id;
            break;
        case 10:
            selectedCards.Draw_3_S_2 = id;
            alert("Pick 2 unlikeable");
            break;
        case 11:
            selectedCards.Draw_3_A_1 = id;
            break;
        case 12:
            selectedCards.Draw_3_A_2 = id;
            emptyCardHolders();
            drawCards(cards.set4);
            break;
        case 13:
            selectedCards.Draw_4_S_1 = id;
            break;
        case 14:
            selectedCards.Draw_4_S_2 = id;
            alert("Pick 2 unlikeable");
            break;
        case 15:
            selectedCards.Draw_4_A_1 = id;
            break;
        case 16:
            selectedCards.Draw_4_A_2 = id;
            emptyCardHolders();
            drawCards(cards.set5);
            break;
        case 17:
            selectedCards.Draw_5_S_1 = id;
            break;
        case 18:
            selectedCards.Draw_5_S_2 = id;
            alert("Pick 2 unlikeable");
            break;
        case 19:
            selectedCards.Draw_5_A_1 = id;
            break;
        case 20:
            selectedCards.Draw_5_A_2 = id;
            emptyCardHolders();
            drawCards(cards.set6);
            break;
        case 21:
            selectedCards.Draw_6_S_1 = id;
            break;
        case 22:
            selectedCards.Draw_6_S_2 = id;
            alert("Pick 2 unlikeable");
            break;
        case 23:
            selectedCards.Draw_6_A_1 = id;
            break
        case 24:
            selectedCards.Draw_6_A_2 = id;
            emptyCardHolders();
            saveResults();
            break;
    }
    step++;
}

function saveResults()
{
    var url = "/saveresults"
    var request = {
        patientId: patientId,
        cards: selectedCards
    }
    
    $.ajax
    ({
        type: "POST",
        contentType: 'application/json',
        url: url,
        dataType: 'json',
        async: false,
        data: JSON.stringify(request),
        success: function (data) {
            $('#gameContainer').empty();
            alert("You have completed this session. Thanks!");
        },
        error: function(error) {console.log(error)}
    })
}

function newPatient()
{
    // Send the data using post
    var url = "/newpatient";

    $.ajax
    ({
        type: "GET",
        contentType: 'application/json',
        url: url,
        dataType: 'json',
        async: false,
        data: null,
        success: function (data) {
            patientId = data.response;
            alert("Your ID is: " + patientId + " \n Please note this down and use it in future sessions");
            switchToTestView();
            getCards();
        },
        error: function(error) {console.log(error)}
    })
}

function switchToTestView()
{
    $("#welcomeSection").hide();
    $("#gameContainer").show();
}

const chatBox = document.getElementById("chat-box");

function addMessage(text, sender){

    const div = document.createElement("div");

    div.classList.add("message");

    div.classList.add(sender);

    div.innerHTML = text;

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage(){

    const username =
        document.getElementById("username").value.trim();

    const message =
        document.getElementById("message").value.trim();

    if(username==="" || message==="")
        return;

    addMessage(message,"user");

    document.getElementById("message").value="";

    const response = await fetch("/predict",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            username,

            message

        })

    });

    const data = await response.json();

    let reply="";

    if(data.status==="safe"){

        reply=`
        <b>Message is Safe</b><br><br>

        Confidence:
        ${data.confidence.toFixed(2)}%
        `;
    }

    else if(data.status==="hate"){

        reply=`
        <b>Hate Speech Detected</b><br><br>

        Severity:
        <b>${data.severity}</b>

        <br><br>

        Categories:

        <br>

        ${data.categories.join("<br>")}

        <br><br>

        Violations:

        ${data.violations}/3
        `;
    }

    else if(data.status==="blocked"){

        reply=`
        <b>You are blocked.</b>

        <br><br>

        Remaining Time:

        ${data.remaining_time}
        `;
    }

    else{

        reply=data.message;
    }

    addMessage(reply,"bot");

}
document
.getElementById("message")
.addEventListener("keypress",function(event){

    if(event.key==="Enter"){

        event.preventDefault();

        sendMessage();

    }

});
document.addEventListener("DOMContentLoaded", () => {
    let fail_count = 0;

    function process_message(data) {
        let cmd = data.cmd;
        let payload = data.data;

        if (!(cmd && payload)) {
            console.error("Improper ws message received");
            return;
        }

        switch (cmd) {
            case "GIVE_MEMBERS_PUB_KEYS":
                window.recipients = payload;
                break;
            case "MEMBER_JOIN":
                window.recipients = {...payload, ...recipients};
                break;
            case "MEMBER_LEAVE":
                delete window.recipients[payload];
                break;
            case "TEXT_MESSAGE":
                add_message(payload);
                break;
        }
    }

    (function get_websocket() {
        let chatSocket = new WebSocket(
            'wss://'
            + 'c3e.gnous.eu'
            + '/ws'
            + `/${room_name.guild.id}`
            + `/${room_name.id}`
        );

        chatSocket.onmessage = (e) => {
            const data = JSON.parse(e.data);
            process_message(data)
        };

        chatSocket.onopen = () => {
            console.log('Websocket connected');
            fail_count = 0
        };

        chatSocket.onclose = () => {
            if (fail_count > 2) {
                UIkit.modal(document.getElementById("ws_error_modal")).show();
            } else {
                fail_count += 1;
                console.error('Chat socket closed unexpectedly');
                console.info('Trying to reconnect in 5s...');
                setTimeout(() => get_websocket(), 5000)
            }
        };

        window.ws = chatSocket;
    })();
});

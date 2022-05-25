/* Project specific Javascript goes here. */

function constructKeyPair(keyPair) {
    return nacl.box.keyPair.fromSecretKey(nacl.util.decodeBase64(keyPair[1]));
}

function decipher(message, author) {
    const sharedKey = nacl.box.before(
        nacl.util.decodeBase64(recipients[author]), usableKeyPair.secretKey
    );

    const payload = nacl.box.open.after(
        nacl.util.decodeBase64(message.box),
        nacl.util.decodeBase64(message.nonce),
        sharedKey
    );

    return nacl.util.encodeUTF8(payload);
}

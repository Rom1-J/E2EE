/* Project specific Javascript goes here. */

function cipher(text) {
    return CryptoJS.AES.encrypt(text, me).toString();
}

function decipher(text, key) {
    return CryptoJS.AES.decrypt(text, key).toString(CryptoJS.enc.Utf8);
}

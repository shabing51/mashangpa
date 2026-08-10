import CryptoJS from 'crypto-js';

function encryptByAES(message, key) {
    let CBCOptions = {
        iv: CryptoJS.enc.Utf8.parse(key),
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    };
    let aeskey = CryptoJS.enc.Utf8.parse(key);
    let secretData = CryptoJS.enc.Utf8.parse(message);
    let encrypted = CryptoJS.AES.encrypt(
        secretData,
        aeskey,
        CBCOptions
    );
    return CryptoJS.enc.Base64.stringify(encrypted.ciphertext);
}

let transferKey = "u2oh6Vu^HWe4_AES";
// 没啥防御，也没价值
console.log(encryptByAES("123456", transferKey)); //0QgUbMUJj2usHikiqtb8HQ==
console.log(encryptByAES("18888888888", transferKey)); //0XIPsaZS668CbiOi/PbyOw==
const CryptoJS = require("C:/PycharmProjects/PythonProject/spiderbuf/crypto-js.min.js");

function m(cipher_text){
    const _0x2aac92 = 'mySecretKey123'
          , _0x3f715a = cipher_text
          , _0x29f7bd = CryptoJS['AES']['decrypt'](_0x3f715a, _0x2aac92)
          , _0x356ca6 = _0x29f7bd['toString'](CryptoJS['enc']['Utf8'])
          , _0x45a4dc = JSON['parse'](_0x356ca6);
    return _0x45a4dc
};


const cipher_text = process.argv[1];  // ← 接收 Python 传递的参数
console.log("process.argv: ", process.argv)
if (cipher_text) {
    const result = m(cipher_text);
    console.log(result);
} else {
    console.error("请提供密文参数");
    process.exit(1);
}

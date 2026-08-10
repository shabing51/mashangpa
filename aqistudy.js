// import CryptoJS from "crypto-js";
const CryptoJS = require("crypto-js");
const  ask4u6FbhGV8 = "a0QHmC1Ova5958nC";//AESkey，可自定义
const  asi2hhkBUJbo = "bMu71lHRX6bRmPxU";//密钥偏移量IV，可自定义

const  acky6QolJSJi = "dLRSzDrm8xkryEyL";//AESkey，可自定义
const  acixHVhiNqmK = "fex6AA4zRfVrSPmr";//密钥偏移量IV，可自定义

const  dskQCqpdBOGo = "hEaIOlrX7tlhAOkz";//DESkey，可自定义
const  dsiqYiQHbZQp = "xMBwDXG1HOubUV04";//密钥偏移量IV，可自定义

const  dckCheMkUojW = "oi4aKMxMECWSyTaz";//DESkey，可自定义
const  dciEekKS6Cws = "p2uRrSFcN9oKLrKY";//密钥偏移量IV，可自定义

const aes_local_key = 'emhlbnFpcGFsbWtleQ==';
const aes_local_iv = 'emhlbnFpcGFsbWl2';

function Base64() {
    var _keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    this.encode = function(a) {
        var c, d, e, f, g, h, i, b = "", j = 0;
        for (a = _utf8_encode(a); j < a.length; )
            c = a.charCodeAt(j++),
            d = a.charCodeAt(j++),
            e = a.charCodeAt(j++),
            f = c >> 2,
            g = (3 & c) << 4 | d >> 4,
            h = (15 & d) << 2 | e >> 6,
            i = 63 & e,
            isNaN(d) ? h = i = 64 : isNaN(e) && (i = 64),
            b = b + _keyStr.charAt(f) + _keyStr.charAt(g) + _keyStr.charAt(h) + _keyStr.charAt(i);
        return b
    };
    this.decode = function(a) {
        var c, d, e, f, g, h, i, b = "", j = 0;
        for (a = a.replace(/[^A-Za-z0-9\+\/\=]/g, ""); j < a.length; )
            f = _keyStr.indexOf(a.charAt(j++)),
            g = _keyStr.indexOf(a.charAt(j++)),
            h = _keyStr.indexOf(a.charAt(j++)),
            i = _keyStr.indexOf(a.charAt(j++)),
            c = f << 2 | g >> 4,
            d = (15 & g) << 4 | h >> 2,
            e = (3 & h) << 6 | i,
            b += String.fromCharCode(c),
            64 != h && (b += String.fromCharCode(d)),
            64 != i && (b += String.fromCharCode(e));
        return b = _utf8_decode(b)
    };
    let _utf8_encode = function(a) {
        var b, c, d;
        for (a = a.replace(/\r\n/g, "\n"),
        b = "",
        c = 0; c < a.length; c++)
            d = a.charCodeAt(c),
            128 > d ? b += String.fromCharCode(d) : d > 127 && 2048 > d ? (b += String.fromCharCode(192 | d >> 6),
            b += String.fromCharCode(128 | 63 & d)) : (b += String.fromCharCode(224 | d >> 12),
            b += String.fromCharCode(128 | 63 & d >> 6),
            b += String.fromCharCode(128 | 63 & d));
        return b
    };
    let _utf8_decode = function(a) {
        for (var b = "", c = 0, d = c1 = c2 = 0; c < a.length; )
            d = a.charCodeAt(c),
            128 > d ? (b += String.fromCharCode(d),
            c++) : d > 191 && 224 > d ? (c2 = a.charCodeAt(c + 1),
            b += String.fromCharCode((31 & d) << 6 | 63 & c2),
            c += 2) : (c2 = a.charCodeAt(c + 1),
            c3 = a.charCodeAt(c + 2),
            b += String.fromCharCode((15 & d) << 12 | (63 & c2) << 6 | 63 & c3),
            c += 3);
        return b
    }
}
var BASE64 = {
    encrypt: function(text) {
        var b = new Base64();
        return b.encode(text);
    },
    decrypt: function(text) {
        var b = new Base64();
        return b.decode(text);
    }
};

var DES = {
 encrypt: function(text, key, iv){
    var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.DES.encrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString();
 },
 decrypt: function(text, key, iv){
    var secretkey = (CryptoJS.MD5(key).toString()).substr(0, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(24, 8);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.DES.decrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString(CryptoJS.enc.Utf8);
  }
};

var AES = {
  encrypt: function(text, key, iv) {
    var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
    // console.log('real key:', secretkey);
    // console.log('real iv:', secretiv);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.AES.encrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString();
  },
  decrypt: function(text, key, iv) {
    var secretkey = (CryptoJS.MD5(key).toString()).substr(16, 16);
    var secretiv = (CryptoJS.MD5(iv).toString()).substr(0, 16);
    secretkey = CryptoJS.enc.Utf8.parse(secretkey);
    secretiv = CryptoJS.enc.Utf8.parse(secretiv);
    var result = CryptoJS.AES.decrypt(text, secretkey, {
      iv: secretiv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    });
    return result.toString(CryptoJS.enc.Utf8);
  }
};

var hexcase = 0
  , b64pad = ""
  , chrsz = 8
  , appId = "b73a4aaa989f54997ef7b9c42b6b4b29";


function rstr2hex(input) {
    try {
        hexcase
    } catch (e) {
        hexcase = 0
    }
    var hex_tab = hexcase ? "0123456789ABCDEF" : "0123456789abcdef";
    var output = "";
    var x;
    for (var i = 0; i < input.length; i++) {
        x = input.charCodeAt(i);
        output += hex_tab.charAt((x >>> 4) & 0x0F) + hex_tab.charAt(x & 0x0F)
    }
    return output
}
function rstr_md5(s) {
    return binl2rstr(binl_md5(rstr2binl(s), s.length * 8))
}
function str2rstr_utf8(input) {
    var output = "";
    var i = -1;
    var x, y;
    while (++i < input.length) {
        x = input.charCodeAt(i);
        y = i + 1 < input.length ? input.charCodeAt(i + 1) : 0;
        if (0xD800 <= x && x <= 0xDBFF && 0xDC00 <= y && y <= 0xDFFF) {
            x = 0x10000 + ((x & 0x03FF) << 10) + (y & 0x03FF);
            i++
        }
        if (x <= 0x7F)
            output += String.fromCharCode(x);
        else if (x <= 0x7FF)
            output += String.fromCharCode(0xC0 | ((x >>> 6) & 0x1F), 0x80 | (x & 0x3F));
        else if (x <= 0xFFFF)
            output += String.fromCharCode(0xE0 | ((x >>> 12) & 0x0F), 0x80 | ((x >>> 6) & 0x3F), 0x80 | (x & 0x3F));
        else if (x <= 0x1FFFFF)
            output += String.fromCharCode(0xF0 | ((x >>> 18) & 0x07), 0x80 | ((x >>> 12) & 0x3F), 0x80 | ((x >>> 6) & 0x3F), 0x80 | (x & 0x3F))
    }
    return output
}
function rstr2binl(input) {
    var output = Array(input.length >> 2);
    for (var i = 0; i < output.length; i++)
        output[i] = 0;
    for (var i = 0; i < input.length * 8; i += 8)
        output[i >> 5] |= (input.charCodeAt(i / 8) & 0xFF) << (i % 32);
    return output
}
function binl2rstr(input) {
    var output = "";
    for (var i = 0; i < input.length * 32; i += 8)
        output += String.fromCharCode((input[i >> 5] >>> (i % 32)) & 0xFF);
    return output
}
function binl_md5(x, len) {
    x[len >> 5] |= 0x80 << ((len) % 32);
    x[(((len + 64) >>> 9) << 4) + 14] = len;
    var a = 1732584193;
    var b = -271733879;
    var c = -1732584194;
    var d = 271733878;
    for (var i = 0; i < x.length; i += 16) {
        var olda = a;
        var oldb = b;
        var oldc = c;
        var oldd = d;
        a = md5_ff(a, b, c, d, x[i + 0], 7, -680876936);
        d = md5_ff(d, a, b, c, x[i + 1], 12, -389564586);
        c = md5_ff(c, d, a, b, x[i + 2], 17, 606105819);
        b = md5_ff(b, c, d, a, x[i + 3], 22, -1044525330);
        a = md5_ff(a, b, c, d, x[i + 4], 7, -176418897);
        d = md5_ff(d, a, b, c, x[i + 5], 12, 1200080426);
        c = md5_ff(c, d, a, b, x[i + 6], 17, -1473231341);
        b = md5_ff(b, c, d, a, x[i + 7], 22, -45705983);
        a = md5_ff(a, b, c, d, x[i + 8], 7, 1770035416);
        d = md5_ff(d, a, b, c, x[i + 9], 12, -1958414417);
        c = md5_ff(c, d, a, b, x[i + 10], 17, -42063);
        b = md5_ff(b, c, d, a, x[i + 11], 22, -1990404162);
        a = md5_ff(a, b, c, d, x[i + 12], 7, 1804603682);
        d = md5_ff(d, a, b, c, x[i + 13], 12, -40341101);
        c = md5_ff(c, d, a, b, x[i + 14], 17, -1502002290);
        b = md5_ff(b, c, d, a, x[i + 15], 22, 1236535329);
        a = md5_gg(a, b, c, d, x[i + 1], 5, -165796510);
        d = md5_gg(d, a, b, c, x[i + 6], 9, -1069501632);
        c = md5_gg(c, d, a, b, x[i + 11], 14, 643717713);
        b = md5_gg(b, c, d, a, x[i + 0], 20, -373897302);
        a = md5_gg(a, b, c, d, x[i + 5], 5, -701558691);
        d = md5_gg(d, a, b, c, x[i + 10], 9, 38016083);
        c = md5_gg(c, d, a, b, x[i + 15], 14, -660478335);
        b = md5_gg(b, c, d, a, x[i + 4], 20, -405537848);
        a = md5_gg(a, b, c, d, x[i + 9], 5, 568446438);
        d = md5_gg(d, a, b, c, x[i + 14], 9, -1019803690);
        c = md5_gg(c, d, a, b, x[i + 3], 14, -187363961);
        b = md5_gg(b, c, d, a, x[i + 8], 20, 1163531501);
        a = md5_gg(a, b, c, d, x[i + 13], 5, -1444681467);
        d = md5_gg(d, a, b, c, x[i + 2], 9, -51403784);
        c = md5_gg(c, d, a, b, x[i + 7], 14, 1735328473);
        b = md5_gg(b, c, d, a, x[i + 12], 20, -1926607734);
        a = md5_hh(a, b, c, d, x[i + 5], 4, -378558);
        d = md5_hh(d, a, b, c, x[i + 8], 11, -2022574463);
        c = md5_hh(c, d, a, b, x[i + 11], 16, 1839030562);
        b = md5_hh(b, c, d, a, x[i + 14], 23, -35309556);
        a = md5_hh(a, b, c, d, x[i + 1], 4, -1530992060);
        d = md5_hh(d, a, b, c, x[i + 4], 11, 1272893353);
        c = md5_hh(c, d, a, b, x[i + 7], 16, -155497632);
        b = md5_hh(b, c, d, a, x[i + 10], 23, -1094730640);
        a = md5_hh(a, b, c, d, x[i + 13], 4, 681279174);
        d = md5_hh(d, a, b, c, x[i + 0], 11, -358537222);
        c = md5_hh(c, d, a, b, x[i + 3], 16, -722521979);
        b = md5_hh(b, c, d, a, x[i + 6], 23, 76029189);
        a = md5_hh(a, b, c, d, x[i + 9], 4, -640364487);
        d = md5_hh(d, a, b, c, x[i + 12], 11, -421815835);
        c = md5_hh(c, d, a, b, x[i + 15], 16, 530742520);
        b = md5_hh(b, c, d, a, x[i + 2], 23, -995338651);
        a = md5_ii(a, b, c, d, x[i + 0], 6, -198630844);
        d = md5_ii(d, a, b, c, x[i + 7], 10, 1126891415);
        c = md5_ii(c, d, a, b, x[i + 14], 15, -1416354905);
        b = md5_ii(b, c, d, a, x[i + 5], 21, -57434055);
        a = md5_ii(a, b, c, d, x[i + 12], 6, 1700485571);
        d = md5_ii(d, a, b, c, x[i + 3], 10, -1894986606);
        c = md5_ii(c, d, a, b, x[i + 10], 15, -1051523);
        b = md5_ii(b, c, d, a, x[i + 1], 21, -2054922799);
        a = md5_ii(a, b, c, d, x[i + 8], 6, 1873313359);
        d = md5_ii(d, a, b, c, x[i + 15], 10, -30611744);
        c = md5_ii(c, d, a, b, x[i + 6], 15, -1560198380);
        b = md5_ii(b, c, d, a, x[i + 13], 21, 1309151649);
        a = md5_ii(a, b, c, d, x[i + 4], 6, -145523070);
        d = md5_ii(d, a, b, c, x[i + 11], 10, -1120210379);
        c = md5_ii(c, d, a, b, x[i + 2], 15, 718787259);
        b = md5_ii(b, c, d, a, x[i + 9], 21, -343485551);
        a = safe_add(a, olda);
        b = safe_add(b, oldb);
        c = safe_add(c, oldc);
        d = safe_add(d, oldd)
    }
    return Array(a, b, c, d)
}
function md5_cmn(q, a, b, x, s, t) {
    return safe_add(bit_rol(safe_add(safe_add(a, q), safe_add(x, t)), s), b)
}
function md5_ff(a, b, c, d, x, s, t) {
    return md5_cmn((b & c) | ((~b) & d), a, b, x, s, t)
}
function md5_gg(a, b, c, d, x, s, t) {
    return md5_cmn((b & d) | (c & (~d)), a, b, x, s, t)
}
function md5_hh(a, b, c, d, x, s, t) {
    return md5_cmn(b ^ c ^ d, a, b, x, s, t)
}
function md5_ii(a, b, c, d, x, s, t) {
    return md5_cmn(c ^ (b | (~d)), a, b, x, s, t)
}
function safe_add(x, y) {
    var lsw = (x & 0xFFFF) + (y & 0xFFFF);
    var msw = (x >> 16) + (y >> 16) + (lsw >> 16);
    return (msw << 16) | (lsw & 0xFFFF)
}
function bit_rol(num, cnt) {
    return (num << cnt) | (num >>> (32 - cnt))
}
function hex_md5(s) {
    return rstr2hex(rstr_md5(str2rstr_utf8(s)))
}

var poPBVxzNuafY8Yu = (function(){
    function osZ34YC04S(obj){
        var newObject = {};
        Object.keys(obj).sort().map(function(key){
            newObject[key] = obj[key];
        });
        return newObject;
    }
    return function(m0fhOhhGL, oNLhNQ){
        var aMFs = '3c9208efcfb2f5b843eec8d96de6d48a';
        var cVWG2 = 'WEB';
        var t5GECZQ = new Date().getTime();

        var pKmSFk8 = {
        appId: aMFs,
        method: m0fhOhhGL,
        timestamp: t5GECZQ,
        clienttype: cVWG2,
        object: oNLhNQ,
        secret: hex_md5(aMFs + m0fhOhhGL + t5GECZQ + cVWG2 + JSON.stringify(osZ34YC04S(oNLhNQ)))
        };
        pKmSFk8 = BASE64.encrypt(JSON.stringify(pKmSFk8));
        pKmSFk8 = AES.encrypt(pKmSFk8, acky6QolJSJi, acixHVhiNqmK);
        return pKmSFk8;
    };
})();




// let oBDNNVgaDf = {
//     "city": "昆明",
//     "month": "202511"
// }
// let hA4Nse2cT = poPBVxzNuafY8Yu("GETDAYDATA", oBDNNVgaDf)
// console.log("hA4Nse2cT:", hA4Nse2cT)

function getReqBody(oBDNNVgaDf) {
    let hA4Nse2cT = poPBVxzNuafY8Yu("GETDAYDATA", oBDNNVgaDf)
    return {
        "hA4Nse2cT": hA4Nse2cT
    }
}

// let ttt = "ckFDTTBNU3ZQdEk4RkUzamQzTllxSlV1SVhVQk05N2U1ZzdxL1B5cmtWdUttM3pCRCtLZGc2T0JTR1ZWYXlqbUZJQUNaV3N3eWs0clNTLzBUdmZGU3BreDN1ZnRkS3JTR214N2k3dUJzUXpWRGdwWDFxUDZiMnBBQmF4ekhKUVBKdzZ3MU4yOG9Kdnp3NlZQRkYvbGRNUWdmZGRmOGM0S25aM3dNRFc3eEo3NnJzQUZaNC9GVTUzN1M5NVFMcSsvWEd1SzRHeHB6VnBiWTJFcnRLR3k1TktEMy9yaXRqMitjZ0V4YURtODlXbEFnU29jUHZtd2trZG5zNVVEZkZyMmNtY3p1bVhtM2dRSHRmaHVHczUvdktFVWRPOHdSVEpWMWVTT2o5ZUd6K3RDcUl6clBiYWR3M0VVVEpodkI5TWxucjdzcVUwc05FQVEwS29yaURZT1V6OWJkeHhTOXBpd0Rkci9wRUtRNm5IUEJHQVppbU04ODJIZXMzcFlSWHFGNzQ3UUJtL0VyeElLZSswV1JpVUltUEVieFRMZWdDMHVzcEltMmVzeVNmeVRuUXE1WjVDUFZWL0RCNDJBSlNiTWRJbTFUeXFRMVJQVGptaDhoUjdZdXVSSWJQa1RQSzhWcmE3dkd3ZWd3MTUvY1dlNjdXaDdYRGxoYXllMVRvZk1VMVpZU3FkWHJlUHZ0ZEhQSmJHcGQzUFppbFM4SWE4U1VoQmlXWkRkUmhFUE56UVNrUE5waFQwZGtaT2oxUWlndVFVVnRUSTVuSkpzNG5SK1VYVklhc0libXRmb2piT3JZL2YvNklURENXY2tsdDhya0VEeXVjYktBamZGWE01UXN3bzFuN3lJSjB1VTFTZkJ6Ti9yaFhJalkzOWQ0T3VnbWdxY0tMZExsUllYVDQvNWMxQTh5WHhudXBGZW5zZEpGeEsxWTNpdU11UVpJY1ppaVh3dDRIOW95cUJtNXNPWTlBWXBtbDh2QlFaNCtvZ0d2SUl6RlR5QmdJdEpURzdFS0F2aFE5d2tzRTRTckE5VzZ1SXJBSXBxaXR0QWxUa0tWMDl5Z2xwYVZmNDZHWXZyeFRHN2VTWEJEajYreFZnS3FPcmRqditEc0c0UnN1dzl4TlFOQ1hIbHdkM0hwckhuQzJEM3p5cjQ1MDlZSExqS2kzbGRvaGVXYkg2ZnlJV0pTTjQzallabTQ1TTZoUzBWQitaRDFTMmQ3Vi9YUG04U3NoV2NXRXQ5SW12UXViTXk3M0dnK1czb2lKeXFlL1QxNGlsdm9nSTZoaEJ0ckwwSFJ4b0IxeWhBNWNHSXFYdEVFS3VsTFVSczJHWlFBeU5ITlFseXpFUFoyS2ZWbVE4TXhOVklKTEg5eWlpdDJSbU9CTXBpYlo2Y21Hbks0VjdlTnpxc0dRbDhrWkJoNk5BWDZMZWhtTUNaNFp1N2l4THpUdDU5UlJyWDlJZ1l5R0crT3hiWEJNVHRNUnFFSjVIZFU4S1RYQnZGemRhaSs1OXdrYkcwT1ltdFlJNEpPZXRjbFp5SnlsdnAydzcyMnJwN0lGMk1CWmFyRGI4RmlsR2FTMC9JditQa3hMRGRaaEtLdkFCMkVOTnJBK1Z1a0R0RklNcFEwYXZUcFJoNng5a1pQT2FFbXB6MzVGdGxhY0ZSbHUrcU5hV2w5TzhQSFNjT1FocnRUMXF5NTcxM01PZXFVYk81NlFWVjRmWnAzRHdHMG1Uc0VRMUxPb2RDUUZwTVE2ejR0K2xqK0hMTUFJQ0ZYcW9tcGZuTHBRc1JmTm5kSnVGM0llZkZHTCszUmFnK2cwOHZZK0FJTVJuVUxNMVNJbDdYU3gvUUx2V3ZwOHFYdlpvaGhCb2ZseDlUOCtWTUp6QzExcHVwY0ZhZE00T1RqcDRQblpTQXh4TndtRnJON1MyTTNTTlFRcm5jUHJMRitsSkl1bFY4WFhRSXREbEMwYmZDMCtEd0hDMGM0VjgvMGRBSmtBblZIdUZLYmZGMXZLSkgycUd4emhIV0xMMjBaRU4vWUhiUFpTN2FoVTV4VDNvNUdPWU8wdFBFd0haZlowdzEyYkszSG0yeFMwaElBdVRqbkx6cmI4bGJWdHFNZHJSTTU2cU11aEI1RkkxU3dFWEJ3SWZOaFRjbndONkVBdWJBMWYzdmQ3djhHWVhwMEVLdnFJUERqak85aU1HbWJnakpHd2d1Vm5jNzloRlJWb2N3dzlMZkRaS1VFYS96czZiMDQ2Q3RuUFdwNU4xVjQyb3ZiZkIrREJEa1pncWhsaU16TVJkOU5sSU5qRHR3U2dHT1Boc1BzR3c3ZGlCYUphVGdNUmcwZ2J0M0lCSGp2c0NHWVVsbHd1Y1JuZHpzbVJEdEhTdldUc0xNRmsvQU5VTjV4cDRNWEk2bU12a1M4L2FsUTNwSGlBMmVsYk9WNDNZZzdORnp1SlcrNC93bWxITy9YQ2txVStGVm5XaGJDbVN0cDQ0OVNmMnprZEdVNlJUK1pKMiszSUk1dGdwRS9SOWFndHhPdmxja0tFWC84cjBKbGU5d2ZIMHNBTElzbFh2bVlUQTBXZGR4R0Jrb2NwSlhxK1kxdU1naGk3YVcycHhOOUczN3JTZVhpbjIvSVJYQmxMNm9FczlkbksrR0JjNXhaMTVtOWJlVmNwb1k5QnNmZnRLbDZ1R0ZIR25DblpPbk40OWkrNDlsRHU0UnpreCs4WGtobkduWDJlcFFrdnZEZ3hqWmhMQzZTK05jclB3Q0VPVm9qSUJ1WHlyUlVuNmhYblBPVXF4TTdZZHZIdzNrVTNwOHZxMkcrR29zQy91OFNoK1RpSmQzYVpjb0VtQ0ZYc3BPQldHTnFTMjkzdVdOeVFZSTdFVnlhMEFZRHJWQXBEY1pSUDJySW9TYkNSc05kY252dkFaaDBNTW85ZlR5NUI2NkZ1ZGJZZnVWV2hxanZzaWpteWhGSUlzVjNoZWtJY3d2MW0rUHJGQ1h0c1Nma082eGtKdGRQUEMrSGlYaEpvRjgyRWxwa0tNZ0QvKzU5TkdibStFczBUOUhiQ0Q1eXMxZmR6VU53bC92MlBSMWxVc0VFNmxtQlk3MDVlQkNjbjhoMjBYTjRRUkh2MWQ5Njd6RmlaUWR1enhBN1FiNWZCRHQrSXZVTWROSHFiZE1IQ1ZkYlVGaGFTemFVSWtsWjFXRnh3cXljQ3dwa2pNV1pUakhCaGJMaTVIQVcrdHJiNldYeXNLbEJXeGUvR3FpMWk5VWdDZi9uaEpvbXBoa1J2OEdoRnNsQ0o5cVZZL24xMWVENkJVYzdoSFY4dWNWSDhCN1BpREFNY1IzTDVJdUdaV3VYLzd1bXFtemQ4UHRXZHc4aDJvVXd6dm1md2V5a2E0SitaVStOL0k4dnhDZjkrUHUyQnYzeEtPRjdBWGNIZXZMSkhIblJUSjBNRVI5QzN3WmtYSHRJejJPVTY5N3JCSTIvZnVvSEtSZ2NSelg5UHBackQzN21qYVQ0VGZZQjY5bDRXOTNaQlArNUdab1dNM3NMTHc0c093YlZRSS9obVdPQUJ4U012dWpwSEtLNE0ySlNiRnNxZEdUSmhXOWJ6RVNmRDc4SzJkM0U1ZkIzRkxQaWpHcU5BS2pMYWtlbi9pNXlkRHl4SmJoWndwaDd5ak5PaXErZFdsNmoxd2w4NE9wWTd4SklmMjc0akxrSm81S0hUWWRmTm9nNW90Q1ZoQVdXaGloQU5sU1UzZEgxNGs3QXpqQ1h5bVBDa0o5RVZKOGR1d040RXhiRGg0bTV0STJ2K3dvb3ZtdmkwakZLTSsyUHdJY2pzQnFYeHVoZHAvYWM2SENncHNUV3M3cm5kZVBZRzJYR28zUk94bWlvK2JZVlBxYmFRM2Z4QWR3QjdHaHl1dkQ0aEgxcDh3alVXNDJ6Mm13cTcyZ3UwMFE0aXNPR3hCOU1HcVN0KzVkU2FDK1NvMm9DbjNXUFMwWDNJUU9sWWJOcW1RbGdUSFpkNDk4QzhLOHZPaER2SXFLdHpaTWoxczN1ZDN1TzM2dU8zb0VQR2prQU9YdUFBRFpyRllaaldXZzQzSElPeURJaWpvWi9tZmg5ZjNBUXhzVU9iVmxWcnhLejMyMXgxOHpZZXBpWHhQeXF6cW1vNjhUU1pvK0RoSGk5bXB6Q21aSG5tR0gxNVR6dVA4eWxieEl3N2h6MmZrQlRjNUJDLzdtYXNKcDEzMk56UTNHREpnWlZad0xVV3NoSUlhenVXb0RpQ3RTcWpFNXdhZEpRSTZjazkwZEZUbjJ5RDVoaXpnUkpLbW5DQ3ZUTFAvU2tQV2VYS2NUS1kwVHJ5d0JkSSs3RXZVT2FIRXFaWUttWHNkL1IwaGgwYTA3RTdrK0RuamJoMG5ZUGZhc2FXYmlZbU4xK1lGaC9yK2ltbkxCc1A3RHl0b3ZRVUYwam4xc1Zwd1dEdXJYRldXekZURnd4TWUvaVpwNTROOUF6cWRoWWduVmVjVmxmK056VjlKbDFkOXRxaXhsYmxPaC9QdGJWTHdWNXFRN0ZtYnVqam15NXVuUDNsT3EvTTFFRzlFNHU0S0tadjAvek9TQW1JcFVuN1RTSE1VYUt0MXZva2ttMkY5UlNxR25IbDhjR3BIbEVOMXpYblpsRE1DM0oyWEU0b1BWcUFkK2VLM2ZRazBaWkw2QUwzWVBDMUlXN05iS3YxMlVOZ0haWTZiZDNxeldidW5ya21BN3FibmFESDUrZUFSY3B2czRGZjhsK1E3dzBMTm0xbjhkT0ZIRFhOWHQwVmJqZWZjWjhtbGt4ZnhxVmpLNXVOSVhybzFGRWsxY0VRd0Y0MSswclMxWkNMdUtqbEREQlRkcnZ2bSszN3cwN2pCbm1MMHNFT0kyZ2hzUC9mR2FzZnBjaEd3NUpOLytQT0tGKzE1ODlpWFhEU0Y2Z2YyM1RiZk9Yd1FwSmpHbmh2N1JoaWNJeUcrVW9wZnN2YjhHNlJ2Y1NLM1NSbGxGZmxNbHIzWG9JUDBBSkFVdVhOMjF1TnFyMXRIdzl5VHR6QllBK0pZSnZSTTFOZjZ2R3B0a1RkeWwzTkYvYUsrN0plOWtlMkpwNjJPejhGd0c1YTBlcDVCZVJVNWNZR1pqaFhZaWRMemdHMUMwdnJySkgrUGFJTFUvYUdJQ3JIcW03TGtwNjc0UlI5NFhzL3ErNVBIcW5xYmVIUGlsMEZVVVIvVUs0cjBqVjllNkc2K2RNTC9IaTBuRUlreHQwUXl1ekFOWmhJK2lOWVdTTmRVV1QzZS9YczVEVk1yZ0ZKdVdZTFZrcUhaVHJkcUpJdlFxVVFlNUNKUmlVbCsyVHZHQUd6ME5VbldjLy9IN3p5NlBQQUw0SjFJa0MyQW1uNjhmWDVUazIrWFJlc05nNDkzWXNDLyt2cjhiUUZOU25WcjhLbytXSE5PbTBWa3ZWOU5VQjJzdHpMMzNmRVZ2Sm1lQU0wUXVJalNlL05NbkFWbU1VY3NuSEM5MGZ6dDRITnZQTmJObWxRL0x6YUQvOFJiVHpOMDFacWFQVUtiYXRIKzJXakhyNDdsK3dRZGNOUVZEWTAvZDROKzNWZmd2NHRwVTBGZSttR2pRRWpzV2EzOFB2SUdKZjRuT0hTOGY3U1ZyWEFxK0g4ZWtuQzFVZmRQcFBnSTFjZXhYSGhsRjJ2VlJPWFo3MEx2TE5UZnEzVmlRYmRjeEpZMGNkM3lORndPejgvbTZwYTVzeEtseDZ0WFRLTlZ0TjIxTFVJQkJOVE1tOHB5b1dtWEZCZXl5dFV1WHgrTGs2ODlQMXR1VTVOdXdYQmgyMEh6TElzcHZlVWhjRUFhMmkwcVBOUmYxbEp1ZDlkRkRhdjFBdlg4Y0FXQ0JpZjg4eXBXdGt0REtDeXVQejZLZTVMb25ZY1ZqZEtUMjhrcndTNm0vM3FoaWJnRDRpRVRucEJOVkxqYUIwYW1NVHBNdUtVOXF3TytSaDBCUUVWSS91MU5MNmFpMXlhdnExem41STJFbStGcTlvZ2tEQnRtekdNaFczWVI5YnVoUFg3UVJhbzY4UG03ZVpueGRrMkJjNllXSmsvYWVicWpORTkxTFBvTDZGVjB0K1grZHR0eEd3dnNZOGtSMmovR2RKdEFjOThGRThWNjY4cWF0NGpwblRKeVg2MTE5cjVuc2RrTnNnVktUNS9qMlFpcEp2MnRwbWxKVkNCWHI0RStWVE1UekZOQ3hsL2M5M2pFUlI3UlBva2FUYUNvOFRIc0JtM1g3bVFtUWlaTnRlOWZuTEVqazN6UnhaVHUwNUFPS21lUFRCZElRbHBHWU0xbnRDdjYvTTR4OHNXVlRsdlM0WGl3dmorUmFhcndHelU1bHJjUlk0emVQRGRqWUtOLzBDS1ArRmFmcUkvb2tDZ2lQc1ZRMDA2MmhrOUhBRGpRS1pyNVEycXJHK1gzMis2bFlZMk9kUU5WQ0MrbWczbWsyL09Oa0U0a0V0ZHh5WFd4b2VHKzdlUXdZM1M2RFphdTgzUk1VUEZ1UFc2Ly9QN3VQWlN3ams3eGo0cXY3QnhXbzFzd2NaZ01DazMzaGhueUlGRmROTmdPZ1d2VGZvN1dCNmxSUXNRS2lkNElSdUxlc05pUmV1eEljZWJmRk4zYzNFYkJ0eDBJajByWG02OTUrRjkyaWt5QUIxeDFUZSttMTF6dVdUK2dBZm5xcnFseXo4YjhtdWZvUkFaZzdBanFad2tpclhYZkN1Ny9xSXlFd09lTTBtSHVUREExY21IZjlrUHFuaWhUOXpvc2lvQjg3YVpYazkzYS80VUwwbWp5dW5aMVJ4dWQ5ck9WcUtqY1N4YWFpRy9GUkUvOW5GS1cwQXRieDNqZUNaNFZhbjk5NnBqenFTcW1ZZGdtVHMxQ0drL05Vemp1MmVDcHFwSGtxSGRwWkdhUnVvR3hQcUc1WUlVSTBGSTJ3c1BVUU9NV3lXOThZYXZGUVZ0cUZzU1JyaTBiTlVoVThLMHBpbzdveTlVUkI2Q01zR1gwaDJENjdKdnFwZkFHOTJKb2EvZnBNUGJzRDVaazhIcjBDaDJ4QWxwRldKUmhRNm8yTTU5cWlnZFdKTkZ3enlQTEt3TXpHaHNjUjlkbjRJR1NkTVhVSG1UMkljRFNQQjFST0dnd08wZkRlbnZibFdjUUxacWgzVzduTS9kZUZhazZQNUZxN3U0aUlyUnFCTDYwYTNRaTVmeE5jbjZqV1N3bTNCNnJBRzAya2Jkbzlra2Vpd3BLK0hsWitCNjV5djRkQkQ1RGdldHNPaTNjSUpLUC9haWtTSGg1VXhEdXptblZNNjlFajMzRm4yVTJsREw1M1E0UmQ2c3hzMzlLMVpNRmlZUWNXdWlwRFhEdkpLQ2UyS3A3eWlKZG1sSGxvVTdNbG45VXdHbnlMN3Z6alEvQ2pPdWphY2p1dHo4am13YTNWRDA5VmdacU5NWXJHeWFZeE9JN1RWa2RXNDFWSVlCQ0UybUpGNG45dWxjRzhmcWlRN3ZGbHVJQldyakNhWWthcng2Y2dKNEprVWx1MmZGNnJWc01qaGZNamlMTFYvOHFGcjhnZWorRitQNlNvdlVpdGdwOGtnanhMWm5CZkRYYUY1YStCTTlQMUV1RGlUTFgwMGI5RDBFUzZxQzN4VWNLTTZubmU3OWNXRjdtZGxlNEhYeldZVlVNb1BsYWd1RlVob1RRSDZEeFk2emdYR215SzQ0cHZlOWtEc0tlc29zalRGVzB4Q2JXOUpJK29nRTFrVk1SaUx2eko5SzdHakUxb21HMEc3b3BRaFh2RFI3ZkpadytMQlR3SjRXYi9pOHNlYldXclkxWlMwY09wSCtNNHMyQW5wUSt0RnlHbjVaU2N5eUlNS09PVW5BajVibnEvWXhhNWdWeEJEQytMK0ZRWk5RYlRIcmpGd3FpcXpQeFlrWVB3WmV3dGQ4RGhOYkRrRmVueEN4WG9tRk9rWUZIYlhwQmpkelU3MTUrcU52ZkRTUWVXUEFxRmpLb3RtdzVCVEVRTUJGRHhseGViYXBKWHNrSi81alQ3MGlpR0FvdTV1anhienYyekJhUzFEWVFZOGxpUFpWQmcxMzhNMWxJdEY5Q1p0SHRnVlBEQXh1TE1NR2FkMjRud2l4QzNzRlZxaU5hakNBVVp1UCsxU1dnekVDYmZRUytDUXZLSXBralhxckdRQi92cEFlU21QYXVySHo5R1o1VmJZZmgrVzdmbDVVVGh0MFQrMWxjNnRiVlE5UGpwaFhBMmYwUlBzYmt2YnhKL2UrWHNrRzRuekhwOW5NWUoyd2ZqSzYxVk5DL0d6YzFaOFhGUWhoWXJObE9IOUNuZUJHZHhrY0lpQW9sV09mTjhqR0tGRDJHVWlCcGdsMWhxa0JKaEM5RlNpV0RucTY0M09pSE1WRTNKNzBDV0RzakRvMzUzRzZwWStKaWd2WVhsVHIxQ0RSWHNwYU5VR2NHTTBLR2cwWDhoOUU5cGUxSWF6UGl2RW1WUGcxY2E1TGJ2TEdnR1p2ajJCK1B5cDVQYjlJektmTVdXUUcwVjFFMXBNWTFCS0NZS1liV2RGOS9aZDFTdTg2SkdYYk9WSTYyT04vbExpNHFNaXJlRVJnUTFPS1lwSk5jbm5ER2V2RExjRU9QN0J1ZS93QldVUTJqQmw3aVRSNno2V2NrTFA0ZFlvRUp0YXh1QlpRSWFJMi9nY3I0QkJsQUtwM1c3VEREa25wTWYyU0UzWHA1Z0Eva0k4QnRGc0Jlb1BzdnhuYkIvK1JyaWozVmhkRmpJMUpuYWk1TysyR0JOaUFDcFREWlZWN3dxTThFeUVqdDF1ZEs1dGM2b09VYTdGMVloWWcrK2xnM1BrVStDMW83TVRycFhPT0lSUWd6T3IzbUQ3ZG1ITVlSWm11WUQ5S3QwMWY1aDVqakpUV2ZKY1dQQlliK01xcFB2TlN3TG9WREEwQlNIajNjNjhkck02WlhLWEVwRCsxa1puY0JseHpKQmZwQ0EyN1psREtSMFRhaHlVYjZvK1VscW10aEtQM0dPakQxYmtsblZXUURoajJqM2tqUjJPY3htcXNmOG5uaDF2Z0J2RWZLOUloamhsV2M5dVJRVEJyWkpkcmpRRnlIZ3NvTDV4SVVxQWRqZWNlcnRBNmg0ZFNNSWlJSm5TK0ozTTE4WDRuY1JtN1R6Zi82bnllekZFQmpEb1VWVlNhTEFhdDIvVmRjaVF3NVBoY0NBamVYM1o0by9OR093RklGK2RIVlhEbHpKNmZ3UTBXcmYvNzEzSDQ3OHlpWThtN284cytGemZBTGpZdjhBNmF6TTJTK1k4MEM3Ymc1ZHhDS3BPaThDc1A3UmpzZGRrUEI2SS9XcmxxUm52YnJmZVZaZkFYZkhoRGIzM3RLQ01BOUpSSE1zc051YWZwQlNUY2ZxQlRkT3lsWkptTlNpcnpoOXVsc2tuNFhaOWtZNkZ3U0FMa2htZ2loMTlINzRNYmhSRkJadnNxYkdsQWRuS1dDaFNuL204cVN5TFc2T0xrNC9Hem1vWGVGbVUwNlJ3RE52dUpoMk9WZ3JYTElPckdTOVhiTmdvRnVkSGU4OHpKYmZzUGRlZVdsNEdvbG5NRFh2TkpjNFpUSjIwempzSVNXR3hNTDZiRU01bUEwVDJ0M0N4ZnRtN3hFQ0JjbEJyeVdmUXZ4aEVFT0d5WW5DNk0zWmpCcVo2QytrT25HeEdVclZqc1JKTW81enpJZklWeEpKLzdsQ0pzdm45cWVHSytFVHZQVGxsMi8vUWlzWEM2MVVpVlZ3VlNFcG54cmc5blVFU3ljOGh5YUk3eXA0NHlvTXVIWi9zWFNjbENWdUhNSEd5dE1YVGJ4MG8wb3g4WWE2NllZWGVwK0lMMDJzZkYzNm9mb09zUVFDUFFmeFJNTjFTVWF0ZTRaUWhTcTM1WllRYmUzT2wxamFmdi9XT3VSblpVdy9JZER4Y0xGY2RnLzlMb2xYTzBsR0dqQS8xQ3Z…"
function dxvERkeEvHbS(data) {
    data = BASE64.decrypt(data);
    data = DES.decrypt(data, dskQCqpdBOGo, dsiqYiQHbZQp);
    data = AES.decrypt(data, ask4u6FbhGV8, asi2hhkBUJbo);
    data = BASE64.decrypt(data);
    return data;
}
// console.log("dxvERkeEvHbS:", dxvERkeEvHbS(ttt))
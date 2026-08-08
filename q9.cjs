const CryptoJS =  require("crypto-js")

function fx(page){
    let data = {page};
    var f = new Date().getTime();
    data.m = CryptoJS["HmacSHA1"](("9527" + f), "xxxooo").toString();
    data.tt = btoa(f);
    return data
}

const page = parseInt(process.argv[2])
// console.log(process.argv)
console.log(fx(page))

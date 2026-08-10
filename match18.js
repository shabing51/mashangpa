import CryptoJS from "crypto-js";
import axios from "axios";

function encrypt(rr, ts){
    let tss = ts.toString(16) + ts.toString(16);
    // console.log(tss);
    let key = CryptoJS.enc.Utf8.parse(tss);
    let iv = CryptoJS.enc.Utf8.parse(tss);
    let encrypted = CryptoJS.AES.encrypt(
        rr,key,{
            iv: iv,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        });
    return encrypted.toString(CryptoJS.enc.Utf8);
}

async function getTime(){
    let url = 'https://match.yuanrenxue.cn/api/getTime';
    let response = await axios.get(url, {
        headers:{
                cookie: "sessionid=1i5v0k8r6a43wlsyiawqngaitay2n0xi",
                "User-Agent": "yuanrenxue"
        }
    });
    return response.data
}

async function getFirstPage(){
    let response = await axios("https://match.yuanrenxue.cn/api/v/question/18data?page=1", {
        headers: {
            "cookie": "sessionid=1i5v0k8r6a43wlsyiawqngaitay2n0xi",
            "User-Agent": "yuanrenxue"
        }
    })
    console.log(response.data);
    return response.data
}

async function getAllDta(page) {
    let total = 0;                                                          
    var data = await getFirstPage();
    total += data.data.reduce((sum,num)=>sum+num,0);           
    let params = ["2|531m141,534m139,536m137,536d137,536u137", '3|583m142,582m142,581m141,581d141,581u141', "4|643m127,644m129,644m131,644d131,644u131", "5|693m127,694m129,693m131,693d131,693u131"];
    for (let pageNum=2; pageNum<=5; pageNum++) {
        let timestamp = await getTime();
        timestamp = parseInt(timestamp / 1000);
        let v = encodeURIComponent(encrypt(params[pageNum-2], timestamp));
        let url = `https://match.yuanrenxue.cn/api/v/question/18data?page=${pageNum}&t=${timestamp}&v=${v}`
        console.log(url);
        break
        let response = await axios(url, {
            headers:{
                    cookie: "sessionid=1i5v0k8r6a43wlsyiawqngaitay2n0xi",
                    "User-Agent": "yuanrenxue"
            }
        });
        data = response.data;
        console.log(data);
        total += data.data.reduce((sum,num)=>sum+num,0);
    }
    console.log(`Total is ${total}`);
}
getAllDta()
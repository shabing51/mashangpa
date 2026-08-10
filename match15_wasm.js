import axios from "axios";

async function getM(){
    const url = "https://match.yuanrenxue.cn/static/new_match/question/15/main.wasm";
    let response = await axios.get(url,{   
            responseType:"arraybuffer",
            headers:{
                cookie: "sessionid=1i5v0k8r6a43wlsyiawqngaitay2n0xi"
            }
        }
    );
    let {instance}=await WebAssembly.instantiate(response.data);
    let encode = instance.exports.encode;
    let t1 = Math.floor(Date.now()/1000/2);
    let t2 = t1-Math.floor(Math.random()*50+1);
    let result = encode(t1,t2);
    return encode(t1,t2)+"|"+t1+"|"+t2;
}

(async (url) => {
    for (let pageNum=1; pageNum<6; pageNum++){
        let m = await getM();
        let uri = `${url}?page=${pageNum}&pageSize=10&kw=&m=${m}`
        let resp = await axios.get(uri,{   
                headers:{
                    cookie: "sessionid=1i5v0k8r6a43wlsyiawqngaitay2n0xi",
                    "User-Agent": "yuanrenxue"
                }
            }
        );
        console.log(await resp.data)
    } 
     

})('https://match.yuanrenxue.cn/api/question/15')
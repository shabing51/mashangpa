import requests
import execjs
import json
import subprocess
js_code = """
const f = {
            '\x52\x4c\x76\x74\x74': function(N, W) {
                return z['\x74\x48\x57\x55\x51'](N, W);
            },
            '\x49\x64\x4a\x70\x53': function(N, W) {
                return z['\x47\x51\x4c\x63\x65'](N, W);
            }
        };
const z = {
        '\x47\x79\x67\x58\x59': '\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x2b\x2f',
        '\x6b\x57\x48\x52\x56': function(e, b) {
            return e >> b;
        },
        '\x42\x77\x4e\x63\x4b': function(e, b) {
            return e & b;
        },
        '\x7a\x4e\x75\x58\x4f': function(e, b) {
            return e << b;
        },
        '\x66\x44\x61\x77\x78': function(e, b) {
            return e + b;
        },
        '\x57\x48\x69\x61\x43': function(e, b) {
            return e !== b;
        },
        '\x45\x67\x54\x6c\x42': '\x43\x47\x57\x4d\x54',
        '\x45\x70\x71\x77\x4b': function(e, b) {
            return e ^ b;
        },
        '\x42\x6f\x68\x51\x71': function(e, b) {
            return e < b;
        },
        '\x5a\x6d\x62\x4f\x61': function(e, b) {
            return e < b;
        },
        '\x78\x42\x55\x50\x41': function(e, b) {
            return e >> b;
        },
        '\x73\x69\x64\x59\x79': function(e, b) {
            return e | b;
        },
        '\x66\x59\x61\x6c\x4d': function(e, b) {
            return e << b;
        },
        '\x58\x6d\x7a\x52\x73': function(e, b) {
            return e >> b;
        },
        '\x64\x55\x6c\x74\x4b': function(e, b) {
            return e(b);
        },
        '\x74\x48\x57\x55\x51': function(e, b) {
            return e < b;
        },
        '\x47\x51\x4c\x63\x65': function(e, b) {
            return e % b;
        },
        '\x71\x6c\x57\x50\x49': function(e, b) {
            return e === b;
        },
        '\x79\x45\x7a\x65\x4c': '\x64\x61\x73\x64\x61\x73\x64\x61\x72\x71\x77\x64\x61\x73\x64\x61\x73\x71\x77\x64\x61\x73\x64\x61',
        '\x73\x54\x68\x4d\x4d': function(e, b) {
            return e(b);
        },
        '\x49\x5a\x43\x64\x42': function(e, b, f) {
            return e(b, f);
        }
    };

function B(b, f, p) {return b ^ z['\x7a\x4e\x75\x58\x4f'](f, p % (-0xf00 + 0x188d + -0x985));}
function J(b, f, p) {return z['\x49\x57\x43\x68\x66'] === z['\x49\x57\x43\x68\x66'] ? z['\x45\x70\x71\x77\x4b'](b, f >> p % (0x730 + -0x1ca5 + -0x1 * -0x157d)) : Q ^ z['\x7a\x4e\x75\x58\x4f'](v, d % (0x23ce * -0x1 + -0x16 * 0x14 + 0x258e * 0x1));}
function Y(b, f) {return (b = b + f - f) ^ f;}

function getM(){
    ts = new Date()['\x67\x65\x74\x54\x69\x6d\x65'](),
    dd = "/api/problem-detail/14/data/";
    var p = function(N) {
        let W = 0x2 * 0xf7f + 0x1 * -0x1af9 + -0x93 * 0x7;
        for (let L = 0x1 * 0x17bf + -0x1fff * -0x1 + -0x37be; f['\x52\x4c\x76\x74\x74'](L, N['\x6c\x65\x6e\x67\x74\x68']); L++) {
            var O = N['\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74'](L);
            for (let y = -0x1034 + -0x2131 + -0x2d * -0x119; y < -0x1ecd + -0x222c + 0x410d; y++)
                switch (f["IdJpS"](y, 0x268a * -0x1 + -0x95c * -0x1 + -0x1d31 * -0x1)) {
                case 0x2d6 * 0xb + 0x2 * -0x3d + -0x1eb8:
                    W = B['\x61\x70\x70\x6c\x79'](null, [W, O, y]);
                    break;
                case -0x1a2f + -0x2448 + 0x3e78 * 0x1:
                    W = J['\x61\x70\x70\x6c\x79'](null, [W, O, y]);
                    break;
                case 0x2c3 + -0x1 * 0x244d + 0x218c:
                    W = Y["apply"](null, [W, O]);
                }
        }
        return W;
    }(z['\x79\x45\x7a\x65\x4c'] + ts)
      , s = ['\x3f', '\x6d', '\x3d']["join"]('')
      , p = p['\x74\x6f\x53\x74\x72\x69\x6e\x67'](0x1 * 0x16c3 + -0x1887 * 0x1 + -0x9 * -0x34);
    return dd += z['\x66\x44\x61\x77\x78'](s, function(N) {
        var W = z['\x47\x79\x67\x58\x59'];
        let O = '', L, y, k, H, D, K, S, I = 0xe * -0xdd + 0x3ad + 0x869;
        for (; z['\x42\x6f\x68\x51\x71'](I, N['\x6c\x65\x6e\x67\x74\x68']); )
            L = N['\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74'](I++),
            y = z['\x5a\x6d\x62\x4f\x61'](I, N['\x6c\x65\x6e\x67\x74\x68']) ? N['\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74'](I++) : -0x18f3 * -0x1 + -0xc5b * 0x3 + 0xc1e,
            k = I < N["length"] ? N['\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74'](I++) : 0x1 * 0x4bf + -0xaf7 + -0x4 * -0x18e,
            H = L >> -0x7fb + -0x1ba1 + -0x2 * -0x11cf,
            D = (-0x39a * 0x1 + -0x5e * -0x35 + -0x1 * 0xfd9 & L) << -0x13b7 * -0x1 + 0xae9 + -0x1e9c | z['\x78\x42\x55\x50\x41'](y, -0x959 * 0x2 + -0x273 * -0xa + -0x5c8),
            K = z['\x73\x69\x64\x59\x79'](z['\x66\x59\x61\x6c\x4d'](0x3 * 0xceb + 0xf0 + -0x27a2 & y, -0x45d * -0x1 + -0x24b0 + 0x2055), z["XmzRs"](k, 0x19a7 + 0x2d * -0xb2 + 0xcf * 0x7)),
            S = -0x283 + 0x178b + -0x14c9 & k,
            isNaN(y) ? K = S = 0x1058 + 0x67 * -0x61 + -0x7a5 * -0x3 : z["dUltK"](isNaN, k) && (S = 0x13 * -0x20c + 0x2 * -0x1079 + -0x1 * -0x4816),
            O = z['\x66\x44\x61\x77\x78'](O, W['\x63\x68\x61\x72\x41\x74'](H)) + W["charAt"](D) + W["charAt"](K) + W['\x63\x68\x61\x72\x41\x74'](S);
        return O;
    }(z['\x66\x44\x61\x77\x78'](p, ts)));
};
console.log(getM());
"""

if __name__ == "__main__":
    cookies = {"sessionid": "7jkdu0y5c22e0vd7bca2ybusg7qhdgjs"}

    total = 0
    base_url = "https://www.mashangpa.com"
    for pageNumber in range(1,21):
        result = subprocess.check_output(['node', "./q14.cjs"], text=True).strip()
        # result = execjs.compile(js_code).call("getM")
        url = f"{base_url}{result}"
        print(url)
        data = json.dumps({"page": pageNumber}, separators=(',', ':'))

        resp = requests.post(url, data=data, cookies=cookies)
        current_array = resp.json().get("current_array")
        total += sum(current_array)
        print(f"第{pageNumber:02d}页数据: {current_array}")

    print(f"{total=}")
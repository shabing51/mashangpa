const fs = require('fs');
window = global;
delete global;

wasmCode =  fs.readFileSync('./encrypt.wasm')
const info = {
    env: {
        memoryBase: 0,
        tableBase: 0,
        memory: new WebAssembly.Memory({initial: 256}),
        table: new WebAssembly.Table({initial: 0, element: 'anyfunc'}),
        stackAlloc: function (size) {
            return instance.exports.stackAlloc(size);
        },
        stackRestore: function (ptr) {
            instance.exports.stackRestore(ptr);
        },
        stackSave: function () {
            return instance.exports.stackSave();
        }
    },
    wasi_snapshot_preview1: {}
};
const wasmModule = new WebAssembly.Module(wasmCode);
const instance = new WebAssembly.Instance(wasmModule, info);
window.shabing = instance.exports;


//console.log(window.shabing)

var _js = 'jsjiami.com.v7';
function a() {
    const P = (function() {
        return [_js, 'EFLSjPQVsjReiPMOaFtrmJHiI.DcWUVoRmE.vd7k==', 'bNTQlG', 'ra7cVCkEW41VASo+W7y0vM3cLa', 'mxStoSoW', 'lHKJW5CVWQxcP8koW41iW4BdVa', 'oSoJsbaXhc3cUmkbW63cTha', 'W5zmW49fW4i', 'uamBWP3cP8knESk+bHpcUSogmSoWWQvWW4Hus8kgWQddI8o8ACkCWR49pKeTWPi', 'WRFcSmkcCN8', 'W40cdSkMW4q', 'bqCzwJ8aW4a', 'umkHiLPM', 'DSoZWRVcKCoP', 'c21XfmktdmoD', 'WONcSSkWWQ1ArtLBW7jhWPddUhX0W4lcMX7cJqy+', 'W5ZdUgfpoq', 'seOBW7NcO8oSWQu', 'W6NdPmkQWPBcNq', 'ymkgpuH3'].concat((function() {
            return ['W5pcHHBdRhfSWQtdLCkLbCoXWPZcRa', 'rSoGmCo5WRi', 'Ch8hdG', 'W7ddGw3dGdHlbG', 'xs8ZdL4', 'q3ZdU8o/gq', 'jKBdRmojWQ0', 'W7zuWRBdUHK', 'WPzIW5FdLmoz', 'seeVW4ZcKSkxWP10WOxdU8keW6hdMrvNpmoTnvRcVcrOWOS', 'WPbNW6G/WRJcOmk+nhpdPmoQCLS', 'WOq4ySk0', 'W5RdRmoPmW3dQ8kIddtdGJyy', 'WOCfumkrW6q', 'W4xdGfXrgG', 'qcPCuG', 'WPdcSuS8WRG', 'CcJdImkltCkjcG', 'fqDmC8ov', 'W6uVWPPOW7G'].concat((function() {
                return ['bxq4W4FcT8oaWP3cKG', 'lr0RW5D8W6NcTmkVW4bI', 'W5JdVMVdGmoxgCkPtstcICkVW6ZdPa', 'q8kDwXxdUwtcImkvW6C', 'W67cMCk/WPFdQSkVW5/cH8oplXZdSCkK', 'WPbLjqRcJxOXfN7cHSosvq', 'h8onkCoHW7hdPI/dGKRdRmoSWRj4BXOBW402WRlcPG', 'pab5WPNcJmkeWRrvW5JdNW', 'WPWZn8kzha', 'WRWZn8kzhgq6WO/dUgNdPCkZW47cJHekWOldUeddQmofFaVcNhfLEuPzoCod', 'sSk5mLze', 'WOvoW57dVa', 'W7zYW6PaW5eGW5FcGq', 'fv7dVmooWPm', 'w8k7WRZdImoK', 'W4awWOVcPmklzmkSW7BdKSorECoR', 'yrKmWPW', 'WOVdG0VcTW', 'lwWlj8oU'];
            }()));
        }()));
    }());
    a = function() {
        return P;
    }
    ;
    return a();
}
(function(c, d, e, f, g, h, i) {
    return c = c >> 0x7,
    h = 'hs',
    i = 'hs',
    function(j, k, l, m, n) {
        const E = b;
        m = 'tfi',
        h = m + h,
        n = 'up',
        i += n,
        h = l(h),
        i = l(i),
        l = 0x0;
        const o = j();
        while (!![] && --f + k) {
            try {
                m = parseInt(E(0xaf, '!2aG')) / 0x1 + parseInt(E(0x9a, '!2aG')) / 0x2 * (parseInt(E(0x9c, 'o!rA')) / 0x3) + parseInt(E(0x91, '%1dZ')) / 0x4 + parseInt(E(0x9d, 'cL8T')) / 0x5 + -parseInt(E(0xad, '*wl7')) / 0x6 + parseInt(E(0xb0, 'fzio')) / 0x7 + parseInt(E(0xbe, '$LGm')) / 0x8 * (-parseInt(E(0xc1, 'E1$%')) / 0x9);
            } catch (p) {
                m = l;
            } finally {
                n = o[h]();
                if (c <= f)
                    l ? g ? m = n : g = n : l = n;
                else {
                    if (l == g['replace'](/[HdEMROFtkrJUVSDPILWeQ=]/g, '')) {
                        if (m === k) {
                            o['un' + h](n);
                            break;
                        }
                        o[i](n);
                    }
                }
            }
        }
    }(e, d, function(j, k, l, m, n, o, p) {
        return k = '\x73\x70\x6c\x69\x74',
        j = arguments[0x0],
        j = j[k](''),
        l = '\x72\x65\x76\x65\x72\x73\x65',
        j = j[l]('\x76'),
        m = '\x6a\x6f\x69\x6e',
        (0x19329d,
        j[m](''));
    });
}(0x5f80, 0x2c36d, a, 0xc1),
a) && (_js = 0x199a);

function b(c, d) {
    const e = a();
    return b = function(f, g) {
        f = f - 0x90;
        let h = e[f];
        if (b['MZrkWY'] === undefined) {
            var i = function(n) {
                const o = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=';
                let p = ''
                  , q = '';
                for (let r = 0x0, s, t, u = 0x0; t = n['charAt'](u++); ~t && (s = r % 0x4 ? s * 0x40 + t : t,
                r++ % 0x4) ? p += String['fromCharCode'](0xff & s >> (-0x2 * r & 0x6)) : 0x0) {
                    t = o['indexOf'](t);
                }
                for (let v = 0x0, w = p['length']; v < w; v++) {
                    q += '%' + ('00' + p['charCodeAt'](v)['toString'](0x10))['slice'](-0x2);
                }
                return decodeURIComponent(q);
            };
            const m = function(n, o) {
                let p = [], q = 0x0, r, t = '';
                n = i(n);
                let u;
                for (u = 0x0; u < 0x100; u++) {
                    p[u] = u;
                }
                for (u = 0x0; u < 0x100; u++) {
                    q = (q + p[u] + o['charCodeAt'](u % o['length'])) % 0x100,
                    r = p[u],
                    p[u] = p[q],
                    p[q] = r;
                }
                u = 0x0,
                q = 0x0;
                for (let v = 0x0; v < n['length']; v++) {
                    u = (u + 0x1) % 0x100,
                    q = (q + p[u]) % 0x100,
                    r = p[u],
                    p[u] = p[q],
                    p[q] = r,
                    t += String['fromCharCode'](n['charCodeAt'](v) ^ p[(p[u] + p[q]) % 0x100]);
                }
                return t;
            };
            b['ygIwjZ'] = m,
            c = arguments,
            b['MZrkWY'] = !![];
        }
        const j = e[0x0]
          , k = f + j
          , l = c[k];
        return !l ? (b['dcXJGV'] === undefined && (b['dcXJGV'] = !![]),
        h = b['ygIwjZ'](h, g),
        c[k] = h) : h = l,
        h;
    }
    ,
    b(c, d);
}


function callEncryptFunction(c, d) {
    const g = window['shabing']['encrypt'](c, d);
    return g;
}


function loadPage(c){
    c = parseInt(c);
    const O = b
          , d = {
            'iRmDq': function(i, j) {
                return i(j);
            },
            'GQcTJ': function(i, j) {
                return i / j;
            },
            'wUWKM': function(i, j, k) {
                return i(j, k);
            },
            'Saaxu': function(i, j) {
                return i(j);
            }
        }
          , e = d['iRmDq'](parseInt, Math[O(0xbc, 'IeoU')](d[O(0x97, 'b^tv')](new Date()[O(0xb8, 'jvOw')](), 0x3e8))[O(0x99, 's(3L')]());
        let f = d[O(0x92, 'PtOP')](callEncryptFunction, c, e);
        return JSON.stringify(
            {
                "page": c,
                "m": f,
                "_ts": e,
            })
        }

//console.log(loadPage(2))


function encrypt(page,timestamp){
    return page + Math.trunc(timestamp / 3) + 16358;
}
//console.log(encrypt(2, 1783909038))
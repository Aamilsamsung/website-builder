const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const html=fs.readFileSync('index.html','utf8');
const script=html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
function load(){
 const root={innerHTML:''};
 const document={querySelector:()=>root,addEventListener:()=>{}};
 const storage={getItem:()=>null,setItem:()=>{}};
 const api=Function('document','localStorage','TextEncoder','Blob',script+'\nreturn {templates,fresh,source,zipBytes,start,navigate};')(document,storage,TextEncoder,Blob);
 return {root,...api};
}
test('standalone HTML contains executable JavaScript',()=>{
 assert.ok(script);
 const {root}=load();
 assert.match(root.innerHTML,/Make the web/);
});
test('template gallery contains 12 distinct templates',()=>{
 const {templates}=load();
 assert.equal(templates.length,12);
 assert.equal(new Set(templates.map(t=>t.id)).size,12);
});
test('editor opens and displays custom content',()=>{
 const {root,start}=load();
 start('horizon');
 assert.match(root.innerHTML,/LIVE CANVAS/);
 assert.match(root.innerHTML,/Ideas made impossible/);
});
test('exports valid files and escapes arbitrary HTML',()=>{
 const {templates,fresh,source}=load();
 const p=fresh(templates[0]);
 p.heading='<img src=x onerror=alert(1)>';
 const files=source(p);
 assert.deepEqual(Object.keys(files),['index.html','styles.css','script.js','README.md']);
 assert.match(files['index.html'],/&lt;img/);
 assert.doesNotMatch(files['index.html'],/<img src=x onerror/);
 assert.match(files['index.html'],/<\/script>/);
 assert.match(files['styles.css'],/#d9f578/);
});
test('ZIP has local file and central directory signatures',async()=>{
 const {templates,fresh,source,zipBytes}=load();
 const blob=zipBytes(source(fresh(templates[0])));
 const bytes=new Uint8Array(await blob.arrayBuffer());
 const v=new DataView(bytes.buffer);
 assert.equal(v.getUint32(0,true),0x04034b50);
 assert.equal(v.getUint32(bytes.length-22,true),0x06054b50);
 assert.equal(v.getUint16(bytes.length-12,true),4);
});

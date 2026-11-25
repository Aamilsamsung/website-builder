import {createClient} from 'npm:@supabase/supabase-js@2.49.4';
import JSZip from 'npm:jszip@3.10.1';
import catalog from './catalog.json' with {type:'json'};
const origins=new Set(['https://forma-website-builder.onrender.com','http://localhost:8000']);
Deno.serve(async req=>{
 const origin=req.headers.get('origin')||''; const headers={'Access-Control-Allow-Origin':origins.has(origin)?origin:'https://forma-website-builder.onrender.com','Access-Control-Allow-Headers':'authorization, content-type, apikey','Access-Control-Allow-Methods':'POST, OPTIONS','Vary':'Origin'};
 const reply=(message:string,status:number)=>new Response(JSON.stringify({message}),{status,headers:{...headers,'Content-Type':'application/json'}});
 if(req.method==='OPTIONS')return new Response(null,{headers});
 if(req.method!=='POST')return reply('Method not allowed',405);
 const token=req.headers.get('authorization')?.match(/^Bearer (.+)$/i)?.[1];if(!token)return reply('Sign in required',401);
 const admin=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false}});
 const {data:{user},error}=await admin.auth.getUser(token);if(error||!user)return reply('Sign in required',401);
 if(Number(req.headers.get('content-length')||0)>12000000)return reply('Project too large',413);
 let body:any;try{const text=await req.text();if(text.length>12000000)return reply('Project too large',413);body=JSON.parse(text)}catch{return reply('Invalid request',400)}
 const t=catalog.templates.find((t:any)=>t.id===body.template);if(!t)return reply('Unknown template',404);
 if(!body.pages||typeof body.pages!=='object'||Array.isArray(body.pages)||typeof body.pages['index.html']!=='string'||Object.keys(body.pages).length>30)return reply('Invalid pages',400);
 for(const [name,content] of Object.entries(body.pages)){if(!/^[-a-z0-9]+\.html$/i.test(name)||typeof content!=='string')return reply('Invalid page',400)}
 const {data:status,error:statusError}=await admin.from('template_status').select('status').eq('template_id',t.id).maybeSingle();if(statusError)return reply('Unable to verify template',503);
 if(status&&status.status!=='published'){const {data:existing}=await admin.from('projects').select('id').eq('user_id',user.id).filter('document->>template','eq',t.id).limit(1);if(!existing?.length)return reply('Template is not published',404)}
 const zip=new JSZip();for(const [name,content] of Object.entries({...catalog.common,...t.files,...body.pages}))zip.file(name,content as string);
 const bytes=await zip.generateAsync({type:'uint8array',compression:'DEFLATE'});const {error:logError}=await admin.from('downloads').insert({user_id:user.id,template_id:t.id});if(logError)return reply('Unable to record download',503);
 return new Response(bytes,{headers:{...headers,'Content-Type':'application/zip','Content-Disposition':'attachment; filename="'+t.id+'.zip"','Cache-Control':'no-store'}});
});

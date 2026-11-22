const admin=require('firebase-admin');
const {construire}=require('./logique');
admin.initializeApp({
  credential:admin.credential.cert(JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT)),
  databaseURL:'https://cahiers-d-appel-default-rtdb.europe-west1.firebasedatabase.app'
});
(async()=>{
  const db=admin.database(),g=async p=>(await db.ref(p).get()).val();
  const [mem,eds,tok,sor]=await Promise.all(['membres','educateurs','fcm','sorties'].map(g));
  const now=new Date(new Date().toLocaleString('en-US',{timeZone:'Europe/Paris'}));
  const r=construire(now,mem,eds,tok,sor);
  console.log('Sorties concernees :',r.sorties.map(s=>s.nom+' ('+s.date+')').join(', ')||'aucune','| notifications a envoyer :',r.out.length);
  if(!r.out.length)return;
  const res=await admin.messaging().sendEach(r.out.map(o=>({token:o.token,notification:{title:o.title,body:o.body},android:{priority:'high'}})));
  let ok=0;
  for(let i=0;i<res.responses.length;i++){
    if(res.responses[i].success){ok++;continue}
    const c=res.responses[i].error&&res.responses[i].error.code;
    console.log('Echec',r.out[i].id,c);
    if(c==='messaging/registration-token-not-registered')await db.ref('fcm/'+r.out[i].id).remove();
  }
  console.log('Envoyees :',ok+'/'+r.out.length);
})().then(()=>process.exit(0)).catch(e=>{console.error(e);process.exit(1)});

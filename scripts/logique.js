const L=o=>o?(Array.isArray(o)?o:Object.values(o)).filter(Boolean):[];
const iso=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
// Qui rappeler : les educateurs valides, avec un jeton de notification, qui n'ont pas encore vote
// pour une sortie prevue entre aujourd'hui et le prochain samedi (inclus).
function construire(now,mem,eds,tok,sor){
  const wd=now.getDay(),sat=new Date(now);sat.setDate(now.getDate()+((6-wd+7)%7));
  const from=iso(now),to=iso(sat);
  const sorties=L(sor).filter(s=>s.date&&s.date>=from&&s.date<=to);
  const par={};L(eds).forEach(e=>{if(e.authId)par[e.authId]=e});
  const out=[];
  for(const [uid,m] of Object.entries(mem||{})){
    if(!m||m.ok!==true)continue;
    const e=par[uid];if(!e)continue;
    const t=tok&&tok[e.id]&&tok[e.id].t;if(!t)continue;
    const manque=sorties.filter(s=>!(s.educGroupes&&s.educGroupes[e.id]));
    if(!manque.length)continue;
    out.push({id:e.id,token:t,title:"Cahier d'appel",body:'Pense à voter pour ton groupe : '+manque.map(s=>s.nom).join(', ')+'.'});
  }
  return {sorties,out,from,to};
}
module.exports={construire};

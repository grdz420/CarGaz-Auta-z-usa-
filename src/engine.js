/* Kwoty w groszach, stawki firmowe w konfiguracji. */
const Engine=(()=>{
 const round=x=>Math.round((x+Number.EPSILON)*100), num=x=>x===''||x==null?null:Number(x), valid=x=>num(x)!==null&&Number.isFinite(num(x))&&num(x)>=0;
 function auctionBreakdown(price,auction,c){
 const a=c.auctionSchedules[auction];if(!a||!valid(price)||Number(price)<=0)return null;
 const p=Number(price),tier=table=>table.findLast(([min])=>p>=min)[1];
 const buyer=p>=a.percentFrom?round(p*a.percent/100)/100:tier(a.buyer),internet=tier(a.internet);
 return {buyer,internet,fixed:a.fixed,total:round(buyer+internet+Object.values(a.fixed).reduce((x,y)=>x+y,0))/100};}
 function auctionFee(price,auction,c){return auctionBreakdown(price,auction,c)?.total??null;}
 function stateQuote(s,c){const code=s.locationState||'',g=c.stateShipping.groups.find(x=>x.states.split(' ').includes(code));return {usd:s.stateShippingOverride!==''?num(s.stateShippingOverride):g?g.usd:code?null:c.stateShipping.fallback,port:s.port||c.stateShipping.portsByState[code]||g?.port||'',status:s.stateShippingOverride!==''?'Stawka ręczna':g?'Cennik firmowy':code?'Stan poza cennikiem':'Brak lokalizacji — średnia',fallback:!code};}
 function calculate(s,c,price){
 const cap=num(s.price),pct=Math.min(100,Math.max(1,Number(s.scenarioPct)||100));
 if(price===undefined)price=valid(cap)?round(cap*(s.mode==='import'?pct:100)/100)/100:null;
 const rows=[],missing=[],warnings=[],tr=s.mode==='transport',f=c.fixed,q=stateQuote(s,c);
 function add(group,name,value,currency='PLN'){const amount=valid(value)?round(Number(value)*(currency==='USD'?f.usd:currency==='EUR'?f.eur:1)):null;if(amount===null)missing.push(name);rows.push({group,name,value,currency,amount});return amount;}
 let purchase=null,fees=null,customs=null,duty=null,vat=null,vb=null,scenario=null;
 if(!tr){purchase=add('Zakup','Cena pojazdu',price,'USD');fees=add('Zakup','Opłaty aukcyjne — '+s.auction,s.auctionOverride===''?auctionFee(price,s.auction,c):s.auctionOverride,'USD');}
 const ship=add('Transport','Transport USA → Holandia',q.usd,'USD');if(q.fallback&&s.stateShippingOverride==='')warnings.push('Nieznana lokalizacja — transport szacunkowy 2 000 USD.');if(ship===null)warnings.push('Stan poza cennikiem — podaj stawkę transportu.');
 if(!tr){
 // Cena faktycznie zapłacona / planowana plus opłaty i przewóz do granicy UE.
 customs=[purchase,fees,ship].every(x=>x!==null)?purchase+fees+ship:null;
 const ratesOK=valid(s.dutyOverride)&&valid(s.vatOverride)&&Number(s.dutyOverride)<=100&&Number(s.vatOverride)<=100;
 function tax(base){if(base===null||!ratesOK)return {duty:null,vat:null,vb:null};const d=Math.round(base*Number(s.dutyOverride)/100),b=base+d+round(f.delivery);return {duty:d,vb:b,vat:Math.round(b*Number(s.vatOverride)/100)};}
 ({duty,vat,vb}=tax(customs));add('Podatki i odprawa','Cło',duty===null?null:duty/100);add('Podatki i odprawa','VAT importowy',vat===null?null:vat/100);add('Podatki i odprawa','Obsługa celna',f.agencyUSD,'USD');
 // Suwak zmienia faktyczną planowaną cenę zakupu w całej wycenie.
 if(customs!==null&&ratesOK)scenario={price,base:customs,duty,vat,vb};
 warnings.push('Akcyza: wycena indywidualna — poza sumą. Podatki szacunkowe, do potwierdzenia przez agencję celną.');}
 add('Obsługa','Transport Holandia → Polska',f.delivery);if(!tr){add('Obsługa','Prowizja firmy',f.commission);if(s.webRemoval)add('Dodatkowe','Usunięcie danych pojazdu ze stron WWW',c.webRemovalPrice);}
 const total=rows.reduce((a,r)=>a+(r.amount??0),0),groups={};for(const r of rows)groups[r.group]=(groups[r.group]||0)+(r.amount??0);
 return {rows,missing,warnings,total,groups,customs,duty,vat,vb,scenario,price};}
 function maxBid(s,c){if(!valid(s.budget))return {bid:null,result:calculate(s,c,0)};const cap=round(Number(s.budget));let lo=1,hi=Math.min(100000000,Math.floor(Number(s.budget)/c.fixed.usd)),best=null,r0=calculate(s,c,1);if(r0.missing.length)return {bid:null,result:r0};while(lo<=hi){const mid=Math.floor((lo+hi)/2),r=calculate(s,c,mid);if(!r.missing.length&&r.total<=cap){best=mid;lo=mid+1;}else hi=mid-1;}return {bid:best,result:best===null?r0:calculate(s,c,best)};}
 return {round,calculate,maxBid,auctionFee,auctionBreakdown,stateQuote};})();if(typeof module!=='undefined')module.exports=Engine;

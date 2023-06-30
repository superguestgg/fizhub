function openmenu() {
	if (document.getElementById("menubutton").className=="menubutton") {
		document.getElementById("menubutton").className="menubutton2";
		document.getElementById("menu").className="menuopened";
		
	} else {
		document.getElementById("menubutton").className="menubutton";
		document.getElementById("menu").className="menuclosed";
	}
}


let massiveoftaskids=[]
let massiveoftasks=[]
function hiddentext(textid){
	let text=document.getElementById(textid).innerHTML
	let minitext=text.substring(0,90)
	minitext=minitext+"..."
	massiveoftaskids.push(textid)
	massiveoftasks.push(text)
	document.getElementById(textid).setAttribute("onclick", "showtext(id)")
	if (text.length>90){
		document.getElementById(textid).innerHTML="краткое условие: "+minitext
		

	} else {
		document.getElementById(textid).innerHTML=text		
			
	}

}


function showtext(textid){
	document.getElementById(textid).innerHTML=massiveoftasks[massiveoftaskids.indexOf(textid)]
	document.getElementById(textid).setAttribute("onclick", "hiddentext(id)")
}

ss = "qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP{}ASDFGHJKL:ZXCVBNM<>?йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,/|1234567890-=+_)(*^%$#@!`~ "+'"'
lens = (ss).length


function sumbolnumber(s){
	if (1 > 0){
		//console.log(ss.indexOf(s)+s)
		return ss.indexOf(s)
	} else {
		return 1
	}
}


function numbertosumbol(n){
	
	//console.log(ss[n%((ss).length)])
	return ss[n%((ss).length)]
}


function encrypt(id){
	token=document.getElementById("roomtoken").value;
	string=document.getElementById("textarea"+id).value;
	stringend=""
	//console.log(token)
	console.log(string)
	lt=(token).length;
	ls=(string).length;
	for (let i=0; i < ls; i++){
		stringend=stringend+numbertosumbol((sumbolnumber(string[i])/1+sumbolnumber(token[i%lt])/1)%lens)
		//console.log(stringend)
	}
	document.getElementById("textarea"+id).value=stringend;

}
function encrypt2(id){
	token=document.getElementById("roomtoken").value;
	string=document.getElementById("textarea"+id).innerHTML;
	stringend=""
	//console.log(token)
	console.log(string)
	lt=(token).length;
	ls=(string).length;
	for (let i=0; i < ls; i++){
		stringend=stringend+numbertosumbol((sumbolnumber(string[i])/1+sumbolnumber(token[i%lt])/1)%lens)
		//console.log(stringend)
	}
	document.getElementById("textarea"+id).innerHTML=stringend;

}
function deencrypt(id){
	token=document.getElementById("roomtoken").value;
	string=document.getElementById("textarea"+id).value;
	stringend=""
	//console.log(token)
	console.log(string)
	lt=(token).length;
	ls=(string).length;
	for (let i=0; i < ls; i++){
		stringend=stringend+numbertosumbol((sumbolnumber(string[i])/1+lens-sumbolnumber(token[i%lt])/1)%lens)
		//console.log(stringend)
	}
	document.getElementById("textarea"+id).value=stringend;

}
function deencrypt2(id){
	token=document.getElementById("roomtoken").value;
	string=document.getElementById("textarea"+id).innerHTML;
	stringend=""
	//console.log(token)
	console.log(string)
	lt=(token).length;
	ls=(string).length;
	for (let i=0; i < ls; i++){
		stringend=stringend+numbertosumbol((sumbolnumber(string[i])/1+lens-sumbolnumber(token[i%lt])/1)%lens)
		//console.log(stringend)
	}
	document.getElementById("textarea"+id).innerHTML=stringend;

}

function copylink(){
	navigator.clipboard.writeText("phs3.na4u.ru/anonnetwork/{{room.room_name}}/{{this_message.id}}");
}

function closepinnedmessage(id){
	//console.log(id)
	id=id.replace("close","")
	message=document.getElementById(id).innerHTML
	message=``
	document.getElementById(id).innerHTML=message
	document.getElementById(id).remove()
}

function createcookie(password){
	
	maxage=60;
	maxage=(60*60)/1;
	document.cookie="password="+password+"; samesite=strict; path=/; max-age="+maxage;
}

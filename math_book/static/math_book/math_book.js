function openmenu() {
	if (document.getElementById("menubutton").className=="menubutton") {
		document.getElementById("menubutton").className="menubutton2";
		document.getElementById("menu").className="menuopened";
	} else {
		document.getElementById("menubutton").className="menubutton";
		document.getElementById("menu").className="menuclosed";
	}
}


function openaccountfromcookie(string){
	let cookies=(document.cookie).split(";");
	//alert(cookies[2]);
	let cakes=cookies.length;
	//alert(cakes);
	let username="undefined guest";
	let userpassword="1234";
	for (let i =1;i<cakes;i++){
		thiscookie=cookies[i]+"";
		console.log(thiscookie);
		namethiscookie=thiscookie.split("=")[0];
		valuethiscookie=thiscookie.split("=")[1];
		if ((namethiscookie==" math_book_user_name")){
			username=valuethiscookie;
		}
	}
	console.log(username);
	if (cakes>1) {
		document.getElementById("loginbutton").innerHTML=`<a href="/math_book/myaccount/">${username}</a>`;
	}
	if (string=="name"){
		return username;
	} else if (string=="password"){
		return userpassword;
	}

	
	if (username == "undefined guest"){
		if (document.getElementById("creatorname2")!=null){
			document.getElementById("creatorname2").innerHTML="вы можете зарегистрироваться <a href='/math_book/login/'>здесь</a>";
		}
	} else {
		if (document.getElementById("creatorname2")!=null){
			document.getElementById("creatorname2").remove();
		}
	}
}


let massiveoftaskids=[];
let massiveoftasks=[];


function hiddentext(textid){
	let text=document.getElementById(textid).innerHTML;
	let minitext=text.substring(0,90);
	minitext=minitext+"...";
	massiveoftaskids.push(textid);
	massiveoftasks.push(text);
	document.getElementById(textid).setAttribute("onclick", "showtext(id)");
	if (text.length>90){
		document.getElementById(textid).innerHTML="краткое условие: "+minitext;
	} else {
		document.getElementById(textid).innerHTML=text		
	}
}


function showtext(textid){
	document.getElementById(textid).innerHTML=massiveoftasks[massiveoftaskids.indexOf(textid)];
	document.getElementById(textid).setAttribute("onclick", "hiddentext(id)");
}


function openpage(){
	ismobileversion();
}


openpage();
console.log("ggg");


function ismobileversion(){
	if (window.innerWidth<window.innerHeight){
		//alert('mobile')
		let classes=['task','pagemenu','message','chat','my_message_place','another_message_place','messenger_place',];
		ih="";
		for (let i = 0; i < classes.length;i++){
			clas=classes[i]
			ih+=`.${clas}{margin-right:2%;margin-left:2%;width:auto}.${clas}:hover{margin-right:2%;margin-left:2%;width:auto}`;
		}
		classes=['create_message_place']
		
		for (let i = 0; i < classes.length;i++){
			clas=classes[i]
			ih+=`.${clas}{right:2%;left:calc(2% + 50px);width:auto}.${clas}:hover{right:2%;left:calc(2% + 50px);width:auto}`;
		}
		ih+=`.messenger_menu{width: 50px; top: 52px; left: -10px}.messenger_menu:hover{width: 50px; top: 52px; left: -10px}`
		ih+=`.chats_mini_place{left: -100%}.chats_mini_place:hover{left: -100%}`
		document.getElementById("style").innerHTML=ih;
	}
}


function saveaccount(){
	document.cookie="math_book_sorryitsimpossible={{user_name}}; samesite=strict; path=/; max-age=3600000000000000"
	document.cookie="math_book_user_name={{user_name}}; samesite=strict; path=/; max-age=3600000000000000"
	document.cookie="math_book_user_id={{user_id}}; samesite=strict; path=/; max-age=3600000000000000"
	document.cookie="math_book_session_key={{session_key}}; samesite=strict; path=/; max-age=3600000000000000"
}


function checkSubstringOnIndex(text, index, substring){
	let t = true;
	let substringLength = substring.length;
	for (let substringIndex=0; substringIndex<substringLength; substringIndex++){
		if (text[index+substringIndex]!=substring[substringIndex]){
			t=false
		}
	}
	return t;
}


function loadLatex(id_from, id_for){
	resultText="";
	text=document.getElementById(id_from).innerHTML;
	// 0=normal ; 1=formula
	typeElementNow=0;
	formula="";
	for (let i=0;i<=text.length;i++){
		if (text[i]=="$"){
			typeElementNow++;
			typeElementNow %= 2;
			resultText+=katex.renderToString(formula,{throwOnError: true});
			formula="";
		} else if (typeElementNow==1){
			if (text[i]=="&"){
				if (checkSubstringOnIndex(text, i, "&gt;")){
					i+=3;
					formula+=">";
					continue;
				} if (checkSubstringOnIndex(text, i, "&lt;")){
					i+=3;
					formula+="<";
					continue;
				}
			}
			formula+=text[i];
		} else {
			if (text[i]=="\\"){
				console.log(text[i+1]);
				if (checkSubstringOnIndex(text, i,"\\item")){
					resultText+="<br>";
					i+=4;
				}
				if (checkSubstringOnIndex(text, i,"\\end")){
					resultText+="<br>";
					i+=3;
				}
				if (checkSubstringOnIndex(text, i,"\\begin")){
					resultText+="<br>";
					i+=5;
				}
			}
			else{
				resultText+=text[i];
			}
		}
	}
	for (var i=0;i<100;i++){
		resultText=resultText.replace("(enter)", "<br>");
	}
	resultText=resultText.replace("undefined","");
	document.getElementById(id_for).innerHTML=resultText;
}


function processingTicket(id_from, id_for){
	processingPage(id_from, id_for);
	loadLatex(id_from, id_for);
}


function processingPage(id_from, id_for){
	text=document.getElementById(id_from).innerHTML;
	resultText="";
	textLen=text.length;
	for (let i=0;i<textLen;i++){
		if (text[i]=="$"){
			resultText+=text[i];
			i++;
			if (i==textLen){
				break;
			}
			while (text[i]!="$"){
				resultText+=text[i];
				i++;
				if (i==textLen){
					break;
				} 
			}
		} if (text[i]=="&"){
			if (checkSubstringOnIndex(text, i, "&gt;")){
				i+=3;
				resultText+=">";
				continue;
			} if (checkSubstringOnIndex(text, i, "&lt;")){
				i+=3;
				resultText+="<";
				continue;
			}
		}
		resultText+=text[i];
	}
	console.log(text);
	console.log(resultText);
	document.getElementById(id_for).innerHTML=resultText;
}


function open_session_ticket(){
	if (document.getElementById("session_ticket_open_close_button").innerHTML=="открыть"){
		document.getElementById("session_ticket_open_close_button").innerHTML="закрыть";
		document.getElementById("session_ticket").className="session_ticket_opened";
	} else if (document.getElementById("session_ticket_open_close_button").innerHTML=="закрыть"){
		document.getElementById("session_ticket_open_close_button").innerHTML="открыть";
		document.getElementById("session_ticket").className="session_ticket";
	}
}
let template = {
	"python": "print(1 + 1)",

	"java": `// One class needs to be called Main
public class Main {
	public static void main(String[] args) {
		System.out.println(1 + 1);
	}
}`,

	"node": `let input = require('/input.js'); // optional, but recreates input() from Python
console.log(1 + 1);`,

	"c": `#include <stdio.h>
int main() {
	printf("%i\\n", 1 + 1);
	return 0;
}`,

	"c++": `#include <iostream>
int main() {
	std::cout << 1 + 1 << std::endl;
}`,

	"c#": `using System;
namespace CodeExec {
	class MyClass {
		static void Main() {
			Console.WriteLine(1 + 1);
		}
	}
}`,

	"asm64": `		extern	printf		; the C function, to be called

        section .data		; Data section, initialized variables
msg:	db "ASM64!", 10, 0	; C string 10 is newline, 0 is null terminator
fmt:    db "%s", 0    	    ; The printf format , '0' for null terminator

        section .text       ; Code section.

        global main			; the standard gcc entry point
main:						; the program label for the entry point
        push    rbp			; set up stack frame, must be alligned
	
        mov		rdi,fmt
        mov		rsi,msg
        mov		rax,0		; or can be  xor  rax,rax
        call    printf		; Call C function

        pop		rbp			; restore stack

        mov		rax,0		; normal, no error, return value
        ret					; return`
}

let langTable = {
	'python': 'text/x-python',
	'node': 'text/javascript',
	'java': 'text/x-java',
	'c': 'text/x-csrc',
	'c++': 'text/x-c++src',
	'c#': 'text/x-csharp',
	'asm64': {
		name: "gas",
		architecture: "x86"
	}
}

let socket = io(location.href);
let cm = null;
let timer = null;
let isLoading = false;
let isLoadingTask = false;

let hasTyped = false;

let stdin = "";

let problems = [];
let chall = "";

let lastTime = new Date();

let init = () => {
	let lang = "python";

	if (sessionStorage.lang) {
		lang = sessionStorage.lang;
		$("#lang-select").val(sessionStorage.lang);
	}

	cm = CodeMirror(document.getElementById("code"), {
		value: template[lang],
		mode: langTable[lang],
		lineNumbers: true,
		lineWrapping: true
	});
	cm.setSize("100%", "100%");

	if (sessionStorage.code) {
		cm.setValue(sessionStorage.code);
	}

	cm.on("inputRead", () => {
		hasTyped = true;
	});

	cm.on("change", () => {
		sessionStorage.code = cm.getValue()
	});

	let hb = setInterval(() => {
		socket.emit("heartbeat");

		if(new Date() - lastTime > 10*1000) {
			console.log("[💔] Socket died...");
			Swal.fire({
				type: "error",
				title: "Lost connection!",
				text: "The connection was lost to the CodeExec backend. Please refresh the page.",
			});
			clearInterval(hb);
		}
	}, 5000);
};

let resize = () => {
    let size = $(window).height() - $('.row.app').offset().top - 1;
    $('.row.app').css('height', size);
    term.fit();
}

socket.on("heartbeat", () => {
	lastTime = new Date();
	console.log("[❤️] Socket active...");
})

window.onload = () => {
	init();
	resize();
	$(window).resize(resize);
}

Terminal.applyAddon(fit);
let term = new Terminal();

term.open(document.getElementById('output'));
term.fit();

term.write("Welcome to CodeExec!\r\nIn the space to the left, you can code in your selected language.\r\nThis website supports Python, NodeJS, and more.\r\n\r\nWaiting for input...");

$("#lang-select").change(() => {
	let lang = $("#lang-select")[0].value;

	cm.setOption("mode", langTable[lang]);

	if (!hasTyped) {
		cm.setValue(template[lang]);
	}

	sessionStorage.lang = lang;
});

let waiting = 0;

let timerFunc = () => {
	term.write(".");
	waiting += 1;

	if(waiting >= 8) {
		isLoading = false;
		isLoadingTask = false;
		clearInterval(timer);
		setTimeout(() => {
			term.reset();
			term.write("Welcome to CodeExec!\r\nIn the space to the left, you can code in your selected language.\r\nThis website supports Python, NodeJS, and more.\r\n\r\nWaiting for input...");
			Swal.fire({
				type: "error",
				title: "Execution timed out",
				text: "The execution timed out. Please try again or check if the website is down.",
			});
		}, 100);
	}
}

$("#run").click(() => {
	if (isLoading || isLoadingTask)
		return;

	term.reset();
	socket.emit('run', {
		code: cm.getValue(),
		lang: $("#lang-select")[0].value,
		stdin: stdin,
		problem: chall
	});
	if (chall) {
		term.write(`Executing code for task ${chall}.`);
		isLoadingTask = true;
	} else {
		term.write("Executing code.");
	}
	waiting = 0;
	timer = setInterval(timerFunc, 1000);
	isLoading = true;
});

$("#new").click(() => {
	cm.setValue(template[$("#lang-select")[0].value]);
	hasTyped = false;
});

$("#stdin").click(() => {
	Swal.fire({
		type: "info",
		title: "Input data:",
		text: "Enter data to be sent over stdin. Each line becomes a new input.",
		input: "textarea",
		inputValue: stdin || "",
		showCancelButton: true
	}).then((response) => {
		if (response.value) {
			stdin = response.value;
		}
	});
});

$("#tasks").click(() => {
	let challenges = {
		"None": "None"
	};
	problems.forEach(name => {
		challenges[name] = name;
	});

	Swal.fire({
		type: "question",
		title: "Select a task.",
		text: "Choose a task to attempt. Details can be found on the challenge entry.",
		input: "select",
		inputOptions: challenges,
		inputValue: chall,
		showCancelButton: true
	}).then((response) => {
		if (!response.value)
			return;

		if (response.value != "None") {
			Swal.fire({
				type: "info",
				title: "Task accepted!",
				html: `The task <strong>${response.value}</strong> has been selected. Submit your solution code that works with all test cases for the flag.`
			});
			chall = response.value;
		} else {
			chall = "";
		}
	});
});

socket.on('out', data => {
	if (data) {
		console.log("[OUT]", data);

		if (isLoadingTask) {
			if (isLoading) {
				term.reset();
				clearInterval(timer);
				isLoading = false;
			}

			if (!data.includes("[Task]")) {
				isLoadingTask = false;
			}
		}

		if (isLoading) {
			isLoading = false;
			clearInterval(timer);
			term.reset();
		}

		data = data.replace(/\n/g, "\r\n");
		term.write(data);
	}
});

socket.on('err', data => {
	if (data) {
		console.log("[ERR]", data);

		if (isLoadingTask) {
			if (isLoading) {
				term.reset();
				clearInterval(timer);
				isLoading = false;
			}

			if (!data.includes("[Task]")) {
				isLoadingTask = false;
			}
		}

		if (isLoading) {
			isLoading = false;
			clearInterval(timer);
			term.reset();
		}

		data = data.replace(/\n/g, "\r\n");
		term.write(data);
	}
});

socket.on("problems", data => {
	problems = data;
});

function save() {
	swal({
		title: "Save File",
		html: "Please enter the name of the code to be saved:",
		type: "info",
		showCancelButton: true,
		input: 'text'
	}).then(val => {
		if(!val.value.length)
			return;

		let name = "ce_" + val.value;
		localStorage[name] = cm.getValue();

		swal({
			title: "Save File",
			html: `File <strong>${val.value}</strong> saved successfully.`,
			type: "success",
		});
	});
}

function load() {
	let keys = {};
	for (let i = 0; i < localStorage.length; i++) {
		let key = localStorage.key(i);
		if (key && key.startsWith("ce_")) {
			let fix = key.substring("ce_".length);
			if (key && fix)
				keys[key] = fix;
		}
	}

	if(!Object.keys(keys).length) {
		return swal({
			title: "Load File",
			html: "There are no saved files!",
			type: "error"
		})
	}

	swal({
		title: "Load File",
		html: "Please select the saved file to be loaded:",
		type: "info",
		showCancelButton: true,
		input: 'select',
		inputOptions: keys
	}).then(val => {
		cm.setValue(localStorage[val.value]);
		hasTyped = true;
	});
}

function del() {
	let keys = {};
	for (let i = 0; i < localStorage.length; i++) {
		let key = localStorage.key(i);
		if (key && key.startsWith("ce_")) {
			let fix = key.substring("ce_".length);
			if (key && fix)
				keys[key] = fix;
		}
	}

	if(!Object.keys(keys).length) {
		return swal({
			title: "Delete File",
			html: "There are no saved files!",
			type: "error"
		})
	}

	swal({
		title: "Delete File",
		html: "Please select the saved file to be delete:",
		type: "info",
		showCancelButton: true,
		input: 'select',
		inputOptions: keys
	}).then(val => {
		localStorage.removeItem(val.value);
	});
}
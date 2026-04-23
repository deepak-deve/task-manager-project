const BASE_URL = "http://127.0.0.1:5000";

function register() {

    const username = document.getElementById("reg_username").value;
    const password = document.getElementById("reg_password").value;

    fetch(BASE_URL + "/register", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);
        alert("User registered! Now login.");
    })
    .catch(err => console.log(err));
}

function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch(BASE_URL + "/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.token) {
            localStorage.setItem("token", data.token);
            document.getElementById("message").textContent = "Login success";
        } else {
            document.getElementById("message").textContent = data.error;
        }
    })
    .catch(error => console.log(error));
}

function loadTasks() {
    const token = localStorage.getItem("token");

    fetch(BASE_URL + "/tasks", {
        method: "GET",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById("taskList");
        list.innerHTML = "";

        data.forEach(task => {
            const li = document.createElement("li");
            li.innerHTML=`
		       <span>${task.title} - ${task.status}</span>
			   <div>
			       <button onclick="deleteTask(${task.id})">Delete</button>
			       <button onclick="editTask(${task.id}, '${task.title}', '${task.status}')">Edit</button>
			   </div>`;   
            list.appendChild(li);
        });
    })
    .catch(error => console.log(error));
}
function addTask() {
	const title=document.getElementById("title").value;
	const status =document.getElementById("status").value;
	
	const token=localStorage.getItem("token");
	
	fetch(BASE_URL + "/tasks", {
		method:"POST",
		headers:{
			"Content-Type":"application/json",
			"Authorization":"Bearer " + token
		},
		body:JSON.stringify ({
			title:title,
			status:status
		})
	})
	.then(response => response.json())
	.then(data => {
		console.log(data);
		loadTasks();
	})
	.catch(error => console.error(error));
}

function deleteTask(id) {
	   const token=localStorage.getItem("token");
	   
fetch(`${BASE_URL}/tasks/${id}`, {
		   method:"DELETE",
		   headers: {
		       "Authorization":"Bearer " + token,
			   "Content-Type":"application/json"
		   },
	    })
	    .then(response => response.json())
		.then(data =>{
	           console.log(data);
			   loadTasks();
	    })
}		   
		   
function editTask(taskId, oldTitle, oldStatus) {

    const newTitle = prompt("Enter new title:", oldTitle);
    const newStatus = prompt("Enter new status:", oldStatus);

    const token = localStorage.getItem("token");

    fetch(`${BASE_URL}/tasks/${taskId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            title: newTitle,
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        loadTasks(); // refresh
    })
    .catch(error => console.log(error));
}		   
			   
	
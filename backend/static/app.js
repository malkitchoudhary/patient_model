const API="/api";
let editMode=false;

async function loadPatients(){
    const res=await fetch(API+"/view");
    const data=await res.json();
    render(data);
}

function render(data){
    const body=document.getElementById("tableBody");
    body.innerHTML="";

    for(let id in data){
        const p=data[id];
        body.innerHTML+=`
        <tr>
        <td>${id}</td>
        <td>${p.name}</td>
        <td>${p.city}</td>
        <td>${p.age}</td>
        <td>${p.gender}</td>
        <td>${p.height}</td>
        <td>${p.weight}</td>
        <td>${p.bmi}</td>
        <td><span class="badge ${p.verdict}">${p.verdict}</span></td>
        <td>
            <button class="edit-btn" onclick="editPatient('${id}')">Edit</button>
            <button class="delete-btn" onclick="deletePatient('${id}')">Delete</button>
        </td>
        </tr>`;
    }
}

async function savePatient(){

    const patient={
        id:document.getElementById("id").value,
        name:document.getElementById("name").value,
        city:document.getElementById("city").value,
        age:Number(document.getElementById("age").value),
        gender:document.getElementById("gender").value,
        height:Number(document.getElementById("height").value),
        weight:Number(document.getElementById("weight").value)
    };

    if(editMode){
        await fetch(API+"/update/"+patient.id,{
            method:"PUT",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(patient)
        });
        editMode=false;
        document.getElementById("id").disabled=false;
    }else{
        await fetch(API+"/create",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify(patient)
        });
    }

    document.querySelector("form").reset();
    loadPatients();
}

async function editPatient(pid){
    const res=await fetch(API+"/view");
    const data=await res.json();
    const p=data[pid];

    document.getElementById("id").value=pid;
    document.getElementById("name").value=p.name;
    document.getElementById("city").value=p.city;
    document.getElementById("age").value=p.age;
    document.getElementById("gender").value=p.gender;
    document.getElementById("height").value=p.height;
    document.getElementById("weight").value=p.weight;

    document.getElementById("id").disabled=true;
    editMode=true;
}

async function deletePatient(pid){
    await fetch(API+"/delete/"+pid,{method:"DELETE"});
    loadPatients();
}

window.onload=loadPatients;

async function loadStudents() {

    const res = await fetch("/students");
    const students = await res.json();

    const table = document.querySelector("#studentTable tbody");
    table.innerHTML = "";

    students.forEach(s => {

        const row = `
        <tr>
            <td>${s.name}</td>
            <td>${s.age}</td>
            <td>${s.course}</td>
            <td>
                <button onclick="deleteStudent(${s.id})">Delete</button>
            </td>
        </tr>
        `;

        table.innerHTML += row;
    });
}

async function addStudent(){

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const course = document.getElementById("course").value;

    await fetch("/add_student",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify({
            name,
            age,
            course
        })
    });

    loadStudents();
}

async function deleteStudent(id){

    await fetch(`/delete_student/${id}`,{
        method:"DELETE"
    });

    loadStudents();
}

loadStudents();
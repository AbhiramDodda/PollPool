function candidateAdded() {
  let e = document.createElement("li");
  e.className = "candidate_list";
  let ival = document.getElementById("candidate_input").value;
  if (ival === "" || ival === null) {
    alert("Enter a valid name");
    return;
  }
  let t = document.createElement("p");
  t.className = "candidate_name";
  t.innerHTML = ival;
  e.appendChild(t);
  document.getElementById("candidate_input").value = "";
  let sp = document.createElement("SPAN");
  let txt = document.createTextNode("X");
  sp.className = "close";
  sp.appendChild(txt);
  e.appendChild(sp);
  document.getElementById("show_candidates").appendChild(e);
  let close = document.getElementsByClassName("close");
  for (let i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      this.parentElement.style.display = "none";
    };
  }
}

function check() {
  let candidate_names = document.getElementsByClassName("candidate_name");
  const candidates_set = new Set();
  for (let i = 0; i < candidate_names.length; i++) {
    candidates_set.add(candidate_names[i].innerHTML);
  }
  console.log(candidates_set);
  if (candidates_set.has(document.getElementById("candidate_input").value)) {
    document.getElementById("can_exist").innerHTML = "user exists";
  }
}

function pollCreated() {
  // Dates validation
  let startDate = document.getElementById("start_date_input").value;
  let endDate = document.getElementById("end_date_input").value;
  try {
    startDate = new Date(startDate);
  } catch (error) {
    document.getElementById("start_date_input").value = "YYYY-MM-DD";
    alert("Enter valid Start date");
    return;
  }
  try {
    endDate = new Date(endDate);
  } catch (error) {
    document.getElementById("end_date_input").value = "YYYY-MM-DD";
    alert("Enter valid end date");
    return;
  }
  if (startDate >= endDate) {
    alert("Enter valid end date");
    return;
  }
  console.log(startDate);

  let candidate_names = document.getElementsByClassName("candidate_name");
  let candidates_list = [];
  for (let i = 0; i < candidate_names.length; i++) {
    if (candidate_names[i].parentElement.style.display === "none") {
      continue;
    }
    candidates_list.push(candidate_names[i].innerHTML);
  }
  console.log(candidates_list);

  let username = document.getElementById("username").value;

  fetch("/pollapi/create", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      data: candidates_list,
      username: username,
      startdate: startDate,
      enddate: endDate,
    }),
  })
    .then((response) => response.text())
    .catch((error) => {
      console.error("Error", error);
    });
}

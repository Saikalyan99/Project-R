console.log("We can put whatever here at a later time when we know and can do more.");




// This is the code for dark mode toggle button
function darkMode() {
  const element = document.body;
  element.classList.toggle("dark-mode");
}


// This is the code for database management
const mysql = require("mysql");

// (B) CREATE CONNECTION - CHANGE TO YOUR OWN !
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",
  database: "test"
});
db.connect(err => {
  if (err) { throw err; }
  console.log("DB connection OK");
});

// (C) QUERY
db.query("SELECT * FROM `users`", (err, results) => {
  if (err) { throw err; }
  console.log(results);
});



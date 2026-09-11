const mysql = require('mysql2/promise');

const connectDB = mysql.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// A quick ping to check if DB is awake
connectDB.getConnection()
    .then(() => console.log(" MySQL Database connected successfully!"))
    .catch((err) => console.log("MySQL connection FAILED: ", err));

module.exports = connectDB;
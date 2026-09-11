    const db = require('../db/index');
    const bcrypt = require('bcrypt');
    const jwt = require('jsonwebtoken');

    const registerUser = async (req, res) => {
        try {
            const { full_name, email, phone_no, password } = req.body;

            if (!full_name || !email || !password) {
                return res.status(400).json({ message: "All fields are required" });
            }

            const [existingUser] = await db.query('SELECT id FROM users WHERE email = ?', [email]);
            if (existingUser.length > 0) {
                return res.status(409).json({ message: "User with this email already exists" });
            }

            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(password, salt);

            const [result] = await db.query(
                'INSERT INTO users (full_name, email, phone_no, password_hash) VALUES (?, ?, ?, ?)',
                [full_name, email, phone_no, hashedPassword]
            );

            res.status(201).json({ message: "User registered successfully", userId: result.insertId });

        } catch (error) {
            console.error("Signup Error: ", error);
            res.status(500).json({ message: "Internal server error" });
        }
    };

    const loginUser = async (req, res) => {
        try {
            const { identifier, password } = req.body;

            if (!identifier || !password) {
                return res.status(400).json({ message: "Identifier and password are required" });
            }

            const [users] = await db.query(
                'SELECT * FROM users WHERE email = ? OR phone_no = ?',
                [identifier, identifier]
            );

            if (users.length === 0) {
                return res.status(401).json({ message: "Invalid credentials" });
            }

            const user = users[0];

            const isPasswordValid = await bcrypt.compare(password, user.password_hash);
            if (!isPasswordValid) {
                return res.status(401).json({ message: "Invalid credentials" });
            }

            const token = jwt.sign(
                { id: user.id, email: user.email },
                process.env.JWT_SECRET,
                { expiresIn: process.env.ACCESS_TOKEN_EXPIRY || "1d" }
            );

            res.status(200).json({
                message: "Login successful",
                token,
                user: { id: user.id, full_name: user.full_name, email: user.email }
            });

        } catch (error) {
            console.error("Login Error: ", error);
            res.status(500).json({ message: "Internal server error" });
        }
    };

    // ... (keep your existing registerUser and loginUser code)

    const getUserProfile = async (req, res) => {
        try {
            // Because our middleware ran first, we already have req.user!
            // We don't even need to query the database again here.
            
            res.status(200).json({
                message: "Profile fetched successfully",
                user: req.user 
            });
        } catch (error) {
            res.status(500).json({ message: "Internal server error" });
        }
    }

    // Don't forget to export the new function
    module.exports = { registerUser, loginUser, getUserProfile };


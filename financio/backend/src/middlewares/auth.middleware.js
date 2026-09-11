const jwt = require('jsonwebtoken');
const db = require('../db/index');

const verifyJWT = async (req, res, next) => {
    try {
        // 1. Get the token from the headers (Frontend will send it as "Bearer <token>")
        const authHeader = req.headers.authorization;
        
        if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res.status(401).json({ message: "Unauthorized access. No token provided." });
        }

        const token = authHeader.split(' ')[1]; // Extract just the token part

        // 2. Verify the token using your secret key
        const decoded = jwt.verify(token, process.env.JWT_SECRET);

        // 3. Double-check if the user actually still exists in the database
        const [users] = await db.query('SELECT id, full_name, email FROM users WHERE id = ?', [decoded.id]);
        
        if (users.length === 0) {
            return res.status(401).json({ message: "Invalid token. User no longer exists." });
        }

        // 4. Attach the user data to the request object so the next function can use it
        req.user = users[0];

        // 5. Pass control to the actual controller logic
        next();

    } catch (error) {
        return res.status(401).json({ message: "Invalid or expired token." });
    }
};

module.exports = { verifyJWT };
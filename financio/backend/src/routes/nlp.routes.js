const express = require('express');
const router = express.Router();
const { verifyJWT } = require('../middlewares/auth.middleware');

// POST /api/nlp/chat
router.post('/chat', verifyJWT, async (req, res) => {
    const { message } = req.body;
    const userId = req.user.id;

    if (!message || typeof message !== 'string') {
        return res.status(400).json({ error: "Message string is required." });
    }

    try {
        // Forward the request to the local Python NLP service
        const response = await fetch('http://localhost:5005/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message, user_id: userId })
        });

        if (!response.ok) {
            const errText = await response.text();
            throw new Error(`Python NLP server error: ${errText}`);
        }

        const data = await response.json();
        res.json(data);
    } catch (error) {
        console.error("[NLP Router] Error calling Python NLP server:", error);
        res.status(500).json({ error: "Something went wrong processing that request in Python NLP server." });
    }
});

module.exports = router;

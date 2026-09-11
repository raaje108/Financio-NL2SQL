const db = require('../db/index'); // Points exactly to your db folder setup

exports.getShops = async (req, res) => {
    try {
        const userId = req.user.id; 
        
        // This query joins the shop with its inventory and calculates the sums!
        const query = `
            SELECT 
                s.*,
                COALESCE(SUM(i.total_amount), 0) AS total_amount,
                COALESCE(SUM(i.amount_paid), 0) AS total_paid,
                COALESCE(SUM(i.amount_rem), 0) AS total_remaining
            FROM shops s
            LEFT JOIN shop_inventory i ON s.shop_id = i.shop_id
            WHERE s.user_id = ?
            GROUP BY s.shop_id
            ORDER BY s.created_at DESC
        `;

        const [rows] = await db.query(query, [userId]);
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Server error retrieving shops' });
    }
};

exports.createShop = async (req, res) => {
    try {
        const { shop_name, shop_owner, phone_no, shop_address, shop_category } = req.body;
        const userId = req.user.id; 

        const query = `
            INSERT INTO shops (user_id, shop_name, shop_owner, phone_no, shop_address, shop_category) 
            VALUES (?, ?, ?, ?, ?, ?)
        `;
        
        const [result] = await db.query(query, [
            userId, 
            shop_name, 
            shop_owner, 
            phone_no, 
            shop_address, 
            shop_category || 'general' // Default to general if not provided
        ]);
        
        res.status(201).json({ message: 'Shop created successfully', shopId: result.insertId });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Server error creating shop' });
    }
};
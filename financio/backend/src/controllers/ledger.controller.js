const db = require('../db/index'); 

exports.getShopLedger = async (req, res) => {
    try {
        const { shopId } = req.params;
        const [rows] = await db.query('SELECT * FROM shop_inventory WHERE shop_id = ? ORDER BY entry_date DESC', [shopId]);
        res.json(rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Server error retrieving ledger' });
    }
};

exports.recordTransaction = async (req, res) => {
    try {
        const { shopId } = req.params;
        const { product_name, quantity, price, amount_paid, payment_method, notes } = req.body;

        const query = `
            INSERT INTO shop_inventory 
            (shop_id, product_name, quantity, price, amount_paid, payment_method, notes) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        `;
        
        const [result] = await db.query(query, [
            shopId, product_name, quantity, price, amount_paid, payment_method, notes
        ]);

        res.status(201).json({ message: 'Transaction recorded successfully', itemId: result.insertId });
    } catch (error) {
        console.error(error);
        res.status(500).json({ error: 'Server error recording transaction' });
    }
};
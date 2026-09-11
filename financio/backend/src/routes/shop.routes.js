const express = require('express');
const router = express.Router();
const shopController = require('../controllers/shop.controller');
const { verifyJWT } = require('../middlewares/auth.middleware');

router.get('/', verifyJWT, shopController.getShops);
router.post('/', verifyJWT, shopController.createShop);

module.exports = router;
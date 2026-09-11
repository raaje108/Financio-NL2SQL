const express = require('express');
const router = express.Router();
const ledgerController = require('../controllers/ledger.controller');
const { verifyJWT } = require('../middlewares/auth.middleware');

router.get('/:shopId', verifyJWT, ledgerController.getShopLedger);
router.post('/:shopId', verifyJWT, ledgerController.recordTransaction);

module.exports = router;
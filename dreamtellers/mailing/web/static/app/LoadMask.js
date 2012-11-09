Ext.define('WebMailing.LoadMask', {
    extend: 'Ext.LoadMask',
    requires: 'Ext.LoadMask',
    msg: 'Por favor, espere....', // i18n
    bindStore: function(store, initial) {
        if (!initial && this.store) {
            this._unbindStore();
        }
        this.mon(store, 'beforesync', this.show, this);
        this.mon(store, 'write', this.hide, this);
        this._originalOnBatchException = store.onBatchException;
        store.onBatchException = Ext.Function.createSequence(
            Ext.Function.bind(store.onBatchException, store),
            Ext.Function.bind(this.hide, this)
        );
        this.callParent(arguments);
    },
    _unbindStore: function() {
        var store = this.store;
        this.mun(store, 'beforesync', this.show, this);
        this.mun(store, 'write', this.hide, this);
        store.onBatchException = this._originalOnBatchException;
        delete this._originalOnBatchException;
    }
});

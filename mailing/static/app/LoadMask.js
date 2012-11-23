Ext.define('Mailing.LoadMask', {
    extend: 'Ext.LoadMask',
    requires: 'Ext.LoadMask',
    msg: 'Por favor, espere....', // i18n
    bindStore: function(store, initial) {
        if (!initial && this.store) {
            this._unbindStore();
        }
        this.mon(store, 'beforesync', this.show, this);
        this.mon(store, 'write', this.hide, this);
        this.mon(store.getProxy(), 'exception', this.hide, this);
        this.callParent(arguments);
    },
    _unbindStore: function() {
        var store = this.store;
        this.mun(store, 'beforesync', this.show, this);
        this.mun(store, 'write', this.hide, this);
        this.mun(store.getProxy(), 'exception', this.hide, this);
    }
});

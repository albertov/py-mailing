window.setDirtyMailing = function(store) {
    var oneItem = store.getAt(0);
    if (oneItem) {
        var m = Ext.getStore('Mailings').getById(oneItem.get('mailing_id'));
        m.setDirty()
        m.store.fireEvent('update', [m.store, m, 'edit', ['items']]);
    }
}

Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.model.Item'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'number', type: 'int', defaultValue: null},
        {name:'date', type: 'date',  dateFormat: 'c'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    hasMany: [
        {
            model: 'WebMailing.model.Item',
            foreignKey: 'mailing_id',
            name:'items',
            primaryKey:'id',
            storeConfig: {
                listeners: {
                    update: setDirtyMailing,
                    remove: setDirtyMailing,
                    add: setDirtyMailing
                }
            }
        }
    ],
    proxy: {
        type: 'rest',
        url: 'mailing/',
        reader: {
            type: 'json',
            root: 'mailings',
        }
    },

    getViewUrl: function() {
        return Ext.String.format('/m/{0}/', this.get('number'));
    },

    getTitle: function() {
        return Ext.String.format("Envío #{0}", this.get('number')); //i18n
    }
});

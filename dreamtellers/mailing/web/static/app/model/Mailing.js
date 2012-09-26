Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.model.Item',
        'WebMailing.store.ItemTreeStore'
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
            primaryKey:'id'
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
    },

    item_tree: function() {
        if (!this._item_tree_store) {
            this._item_tree_store = Ext.create(
                'WebMailing.store.ItemTreeStore', {
                    mailing: this
            });
        }
        return this._item_tree_store;
    }
});

Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.model.Item',
        'WebMailing.model.ItemNode',
        'Ext.data.proxy.Ajax',
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
            this._item_tree_store = Ext.create('Ext.data.TreeStore', {
                model: 'WebMailing.model.ItemNode',
                proxy:  this.item_tree_proxy()
            });
        }
        return this._item_tree_store;
    },
    item_tree_proxy: function() {
        return Ext.create('Ext.data.proxy.Ajax', {
            url: Ext.String.format('mailing/{0}/item_tree/', this.get('id')),
            reader: {type: 'json'}
        });
    }
});

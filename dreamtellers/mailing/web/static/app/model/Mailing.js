Ext.define('WebMailing.model.Mailing', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    requires: [
        'WebMailing.model.Item'
    ],
    fields: [
        {name:'id', type: 'int'},
        {name:'number', type: 'int'},
        {name:'date', type: 'date',  dateFormat: 'c'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    hasMany: [
        {model: 'WebMailing.model.Item', foreignKey: 'mailing_id', name:'items', primaryKey:'id'}
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
        return this.getProxy().url + this.get('number') + '/';
    }


});

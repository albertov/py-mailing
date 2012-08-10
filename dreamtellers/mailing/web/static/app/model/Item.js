Ext.define('WebMailing.model.Item', {
    extend: 'Ext.data.Model',
    requires: [
        'WebMailing.model.Category'
    ],
    idProperty: 'id',
    fields: [
        {name:'id', type: 'int'},
        {name:'title', type: 'string'},
        {name:'type', type: 'string'},
        {name:'position', type: 'int'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'},
        {name:'category_id', type: 'int'},
        {name:'mailing_id', type: 'int'},
    ],
    belongsTo: [
        {model: 'WebMailing.model.Mailing', foreignKey: 'mailing_id', name:'mailing'},
        {model: 'WebMailing.model.Category', foreignKey: 'category_id', name:'category'}
    ],
    proxy: {
        type: 'rest',
        url: 'item/',
        reader: {
            type: 'json',
            root: 'items',
        }
    }
});


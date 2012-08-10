Ext.define('WebMailing.model.Item', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    fields: [
        {name:'id', type: 'int'},
        {name:'title', type: 'string'},
        {name:'type', type: 'string'},
        {name:'position', type: 'int'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'},
        {name:'category', type: 'int'},
        {name:'mailing', type: 'int'},
    ],
    associations: [
        {type: 'belongsTo', model: 'Mailing', foreignKey: 'mailing'},
        {type: 'belongsTo', model: 'Category', foreignKey: 'category'},
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


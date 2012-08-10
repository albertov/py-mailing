Ext.define('WebMailing.model.Category', {
    extend: 'Ext.data.Model',
    idProperty: 'id',
    fields: [
        {name:'id', type: 'int'},
        {name:'title', type: 'string'},
        {name:'created', type: 'date',  dateFormat: 'c'},
        {name:'modified', type: 'date',  dateFormat: 'c'}
    ],
    associations: [
        {type: 'hasMany', model: 'Item', foreignKey: 'category', name: 'items'}
    ],
    proxy: {
        type: 'rest',
        url: 'category/',
        reader: {
            type: 'json',
            root: 'categories',
        }
    }
});

